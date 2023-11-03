from typing import Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from embedchain.chunkers.base_chunker import BaseChunker
from embedchain.config.add_config import ChunkerConfig
from embedchain.helper.json_serializable import register_deserializable
@register_deserializable
class XmlChunker(BaseChunker):
    """
    A class used to chunk XML files.

    Attributes
    ----------
    text_splitter : RecursiveCharacterTextSplitter
        The text splitter used to split the XML file into chunks.

    Methods
    -------
    __init__(config: Optional[ChunkerConfig]=None)
        Initializes the XmlChunker with the provided config. If no config is provided, a default one is used.
    """

    def __init__(self, config: Optional[ChunkerConfig]=None):
        """
        Initializes the XmlChunker with the provided config. If no config is provided, a default one is used.

        Parameters
        ----------
        config : ChunkerConfig, optional
            The configuration to use for chunking. If not provided, a default configuration is used.
        """
        if config is None:
            config = ChunkerConfig(chunk_size=500, chunk_overlap=50, length_function=len)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=config.chunk_size, chunk_overlap=config.chunk_overlap, length_function=config.length_function)
        super().__init__(text_splitter)