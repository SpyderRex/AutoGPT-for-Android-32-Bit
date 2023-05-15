
import pinecone
import openai

from autogpt.memory.base import MemoryProviderSingleton


def get_ada_embedding(text: str) -> list:
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model="text-embedding-ada-002")["data"][0]["embedding"]


def get_text_from_embedding(embedding: list) -> str:
    return openai.Embedding.retrieve(embedding, model="text-embedding-ada-002")["data"][0]["text"]


class PineconeMemory(MemoryProviderSingleton):
    def __init__(self, cfg):
        pinecone_api_key = cfg.pinecone_api_key
        pinecone_region = cfg.pinecone_region
        pinecone.init(api_key=pinecone_api_key, environment=pinecone_region)
        dimension = 1536
        metric = "cosine"
        pod_type = "p1"
        table_name = "auto-gpt"
        self.vec_num = 0

        if table_name not in pinecone.list_indexes():
            pinecone.create_index(table_name, dimension=dimension, metric=metric, pod_type=pod_type)

        self.index = pinecone.Index(table_name)

    def add(self, data: str) -> str:
        vector = get_ada_embedding(data)
        resp = self.index.upsert([(str(self.vec_num), vector, {"raw_text": data})])
        _text = f"Inserting data into memory at index: {self.vec_num}:\n data: {data}"
        self.vec_num += 1
        return _text

    def get(self, data: str) -> list:
        return self.get_relevant(data, 1)

    def clear(self) -> str:
        self.index.delete(deleteAll=True)
        return "Obliviated"

    def get_relevant(self, data: str, num_relevant: int = 5) -> list:
        query_embedding = get_ada_embedding(data)
        results = self.index.query(query_embedding, top_k=num_relevant, include_metadata=True)
        sorted_results = sorted(results.matches, key=lambda x: x.score)
        return [str(item['metadata']["raw_text"]) for item in sorted_results]

    def get_stats(self) -> dict:
        return self.index.describe_index_stats()
