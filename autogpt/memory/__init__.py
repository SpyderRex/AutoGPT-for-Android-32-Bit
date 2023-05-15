from autogpt.logs import logger
from autogpt.memory.local import LocalCache
from autogpt.memory.pinecone import PineconeMemory


supported_memory = ["local", "pinecone"]

def get_memory(cfg, init=False):
    memory = None
    if cfg.memory_backend == "pinecone":
        if not PineconeMemory:
            logger.warn(
                "Error: Pinecone is not installed. Please install pinecone"
                " to use Pinecone as a memory backend."
            )
        else:
            memory = LocalCache(cfg)
            if init:
                memory.clear()
        memory = PineconeMemory(cfg)
    return memory


def get_supported_memory_backends():
    return supported_memory


__all__ = [
    "get_memory",
    "LocalCache",
    "PineconeMemory",
]
