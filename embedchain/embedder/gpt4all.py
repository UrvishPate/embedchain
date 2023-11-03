from typing import Optional
from embedchain.config import BaseEmbedderConfig
from embedchain.embedder.base import BaseEmbedder
from embedchain.models import VectorDimensions
class GPT4AllEmbedder(BaseEmbedder):
    """
    A class that represents a GPT4All Embedder. It is a child class of BaseEmbedder.
    """

    def __init__(self, config: Optional[BaseEmbedderConfig]=None):
        """
        Initializes the GPT4AllEmbedder with the given configuration.

        :param config: The configuration for the GPT4AllEmbedder. If None, a default configuration is used.
        :type config: Optional[BaseEmbedderConfig]
        """
        super().__init__(config=config)
        from embedchain.embeddings import GPT4AllEmbeddings as LangchainGPT4AllEmbeddings
        embeddings = LangchainGPT4AllEmbeddings()
        embedding_fn = BaseEmbedder._langchain_default_concept(embeddings)
        self.set_embedding_fn(embedding_fn=embedding_fn)
        vector_dimension = VectorDimensions.GPT4ALL.value
        self.set_vector_dimension(vector_dimension=vector_dimension)