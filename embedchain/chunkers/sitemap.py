from typing import Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from embedchain.chunkers.base_chunker import BaseChunker
from embedchain.config.add_config import ChunkerConfig
from embedchain.helper.json_serializable import register_deserializable
@register_deserializable
class SitemapChunker(BaseChunker):
    """
    A Chunker for sitemap. It extends the BaseChunker class.

    Attributes
    ----------
    config : ChunkerConfig, optional
        Configuration for the chunker, by default None
    """

    def __init__(self, config: Optional[ChunkerConfig]=None):
        """
        Constructs all the necessary attributes for the SitemapChunker object.

        Parameters
        ----------
            config : ChunkerConfig, optional
                Configuration for the chunker, by default None
        """
        if config is None:
            config = ChunkerConfig(chunk_size=500, chunk_overlap=0, length_function=len)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=config.chunk_size, chunk_overlap=config.chunk_overlap, length_function=config.length_function)
        super().__init__(text_splitter)