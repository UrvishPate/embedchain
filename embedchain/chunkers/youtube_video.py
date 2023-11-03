from typing import Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from embedchain.chunkers.base_chunker import BaseChunker
from embedchain.config.add_config import ChunkerConfig
from embedchain.helper.json_serializable import register_deserializable
@register_deserializable
class YoutubeVideoChunker(BaseChunker):
    """
    A class used to chunk Youtube videos. It inherits from the BaseChunker class.

    Attributes
    ----------
    config : ChunkerConfig, optional
        Configuration for the chunker (default is None, which sets chunk_size=2000, chunk_overlap=0, length_function=len)
    text_splitter : RecursiveCharacterTextSplitter
        A RecursiveCharacterTextSplitter object used for splitting text.

    Methods
    -------
    __init__(self, config: Optional[ChunkerConfig]=None)
        Constructs all the necessary attributes for the YoutubeVideoChunker object.
    """

    def __init__(self, config: Optional[ChunkerConfig]=None):
        """
        Constructs all the necessary attributes for the YoutubeVideoChunker object.

        Parameters
        ----------
            config : ChunkerConfig, optional
                Configuration for the chunker (default is None, which sets chunk_size=2000, chunk_overlap=0, length_function=len)
        """
        if config is None:
            config = ChunkerConfig(chunk_size=2000, chunk_overlap=0, length_function=len)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=config.chunk_size, chunk_overlap=config.chunk_overlap, length_function=config.length_function)
        super().__init__(text_splitter)