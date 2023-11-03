from typing import Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from embedchain.chunkers.base_chunker import BaseChunker
from embedchain.config.add_config import ChunkerConfig
from embedchain.helper.json_serializable import register_deserializable
@register_deserializable
class TextChunker(BaseChunker):
    """
    Chunker for text. Inherits from BaseChunker.

    This class is used to split text into smaller chunks based on a given configuration.
    """

    def __init__(self, config: Optional[ChunkerConfig]=None):
        """
        Initializes a new instance of the TextChunker class.

        :param config: The configuration for the chunker. If None, a default configuration will be used.
        :type config: Optional[ChunkerConfig]
        """
        if config is None:
            config = ChunkerConfig(chunk_size=300, chunk_overlap=0, length_function=len)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=config.chunk_size if config else None, chunk_overlap=config.chunk_overlap if config else None, length_function=config.length_function if config else None)
        super().__init__(text_splitter)