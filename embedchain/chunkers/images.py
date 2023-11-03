import hashlib
from typing import Optional
from langchain.text_splitter import RecursiveCharacterTextSplitter
from embedchain.chunkers.base_chunker import BaseChunker
from embedchain.config.add_config import ChunkerConfig
class ImagesChunker(BaseChunker):
    """
    A class used to chunk an Image. It extends the BaseChunker.

    ...

    Attributes
    ----------
    config : ChunkerConfig, optional
        a configuration object for chunking

    Methods
    -------
    __init__(config=None)
        Constructs all the necessary attributes for the ImagesChunker object.
    create_chunks(loader, src, app_id=None)
        Loads the image(s), and creates their corresponding embedding. This creates one chunk for each image.
    get_word_count(documents)
        Returns the number of chunks and the corresponding word count for an image.
    """

    def __init__(self, config: Optional[ChunkerConfig]=None):
        """
        Constructs all the necessary attributes for the ImagesChunker object.

        Parameters
        ----------
            config : ChunkerConfig, optional
                a configuration object for chunking
        """
        if config is None:
            config = ChunkerConfig(chunk_size=300, chunk_overlap=0, length_function=len)
        image_splitter = RecursiveCharacterTextSplitter(chunk_size=config.chunk_size, chunk_overlap=config.chunk_overlap, length_function=config.length_function)
        super().__init__(image_splitter)

    def create_chunks(self, loader, src, app_id=None):
        """
        Loads the image(s), and creates their corresponding embedding. This creates one chunk for each image

        Parameters
        ----------
            loader : Loader
                The loader whose `load_data` method is used to create the raw data.
            src : str
                The data to be handled by the loader. Can be a URL for remote sources or local content for local loaders.
            app_id : str, optional
                The application id.
        """
        documents = []
        embeddings = []
        ids = []
        data_result = loader.load_data(src)
        data_records = data_result['data']
        doc_id = data_result['doc_id']
        doc_id = f'{app_id}--{doc_id}' if app_id is not None else doc_id
        metadatas = []
        for data in data_records:
            meta_data = data['meta_data']
            meta_data['data_type'] = self.data_type.value
            chunk_id = hashlib.sha256(meta_data['url'].encode()).hexdigest()
            ids.append(chunk_id)
            documents.append(data['content'])
            embeddings.append(data['embedding'])
            meta_data['doc_id'] = doc_id
            metadatas.append(meta_data)
        return {'documents': documents, 'embeddings': embeddings, 'ids': ids, 'metadatas': metadatas, 'doc_id': doc_id}

    def get_word_count(self, documents):
        """
        The number of chunks and the corresponding word count for an image is fixed to 1, as 1 embedding is created for
        each image

        Parameters
        ----------
            documents : list
                List of documents.
        """
        return 1