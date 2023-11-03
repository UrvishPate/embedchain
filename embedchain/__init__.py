import importlib.metadata
__version__ = importlib.metadata.version(__package__ or __name__)
from embedchain.apps.app import App
from embedchain.client import Client
from embedchain.pipeline import Pipeline
from embedchain.vectordb.chroma import ChromaDB