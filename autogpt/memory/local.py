
from __future__ import annotations

import dataclasses
import json
from pathlib import Path
from typing import Any, List

from autogpt.llm import get_ada_embedding
from autogpt.memory.base import MemoryProviderSingleton

EMBED_DIM = 1536


def create_default_embeddings():
    return [[0.0 for _ in range(EMBED_DIM)] for _ in range(0)]


@dataclasses.dataclass
class CacheContent:
    texts: List[str] = dataclasses.field(default_factory=list)
    embeddings: List[List[float]] = dataclasses.field(default_factory=create_default_embeddings)


class LocalCache(MemoryProviderSingleton):
    def __init__(self, cfg) -> None:
        workspace_path = Path(cfg.workspace_path)
        self.filename = workspace_path / f"{cfg.memory_index}.json"

        self.filename.touch(exist_ok=True)

        file_content = b"{}"
        with self.filename.open("w+b") as f:
            f.write(file_content)

        self.data = CacheContent()

    def add(self, text: str):
        if "Command Error:" in text:
            return ""
        self.data.texts.append(text)

        embedding = get_ada_embedding(text)

        vector = [float(val) for val in embedding]
        self.data.embeddings.append(vector)

        with open(self.filename, "w") as f:
            out = json.dumps(self.data, default=dataclasses.asdict)
            f.write(out)
        return text

    def clear(self) -> str:
        self.data = CacheContent()
        return "Obliviated"

    def get(self, data: str) -> list[Any] | None:
        return self.get_relevant(data, 1)

    def get_relevant(self, text: str, k: int) -> list[Any]:
        embedding = get_ada_embedding(text)

        scores = [sum(a * b for a, b in zip(row, embedding)) for row in self.data.embeddings]

        top_k_indices = sorted(range(len(scores)), key=lambda i: scores[i])[-k:][::-1]

        return [self.data.texts[i] for i in top_k_indices]

    def get_stats(self) -> tuple[int, tuple[int, ...]]:
        return len(self.data.texts), (len(self.data.embeddings), len(self.data.embeddings[0]) if self.data.embeddings else 0)