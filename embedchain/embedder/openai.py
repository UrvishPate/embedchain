import os
from typing import Optional
from langchain.embeddings import OpenAIEmbeddings
from embedchain.config import BaseEmbedderConfig
from embedchain.embedder.base import BaseEmbedder
from embedchain.models import VectorDimensions
try:
    from chromadb.utils import embedding_functions
except ImportError:
    from embedchain.utils import use_pysqlite3
    use_pysqlite3()
    from chromadb.utils import embedding_functions
class OpenAIEmbedder(BaseEmbedder):
    """
    A class used to represent an OpenAI Embedder. It is a subclass of BaseEmbedder.

    ...

    Attributes
    ----------
    config : BaseEmbedderConfig, optional
        Configuration settings for the embedder.

    Methods
    -------
    __init__(config=None)
        Initializes the OpenAIEmbedder with the given configuration.
    """

    def __init__(self, config: Optional[BaseEmbedderConfig]=None):
        """
        Initializes the OpenAIEmbedder with the given configuration.

        If no model is specified in the configuration, the default model 'text-embedding-ada-002' is used.
        If a deployment name is specified, an OpenAIEmbeddings object is created with the deployment name.
        If no deployment name is specified, an OpenAIEmbeddingFunction is created with the OPENAI_API_KEY and OPENAI_ORGANIZATION environment variables.

        Parameters
        ----------
        config : BaseEmbedderConfig, optional
            The configuration settings for the embedder. If not provided, default settings are used.
        """
        super().__init__(config=config)
        if self.config.model is None:
            self.config.model = 'text-embedding-ada-002'
        if self.config.deployment_name:
            embeddings = OpenAIEmbeddings(deployment=self.config.deployment_name)
            embedding_fn = BaseEmbedder._langchain_default_concept(embeddings)
        else:
            if os.getenv('OPENAI_API_KEY') is None and os.getenv('OPENAI_ORGANIZATION') is None:
                raise ValueError('OPENAI_API_KEY or OPENAI_ORGANIZATION environment variables not provided')
            embedding_fn = embedding_functions.OpenAIEmbeddingFunction(api_key=os.getenv('OPENAI_API_KEY'), organization_id=os.getenv('OPENAI_ORGANIZATION'), model_name=self.config.model)
        self.set_embedding_fn(embedding_fn=embedding_fn)
        self.set_vector_dimension(vector_dimension=VectorDimensions.OPENAI.value)