from typing import Any
from embedchain import App
from embedchain.config import AddConfig, AppConfig, BaseLlmConfig
from embedchain.embedder.openai import OpenAIEmbedder
from embedchain.helper.json_serializable import JSONSerializable, register_deserializable
from embedchain.llm.openai import OpenAILlm
from embedchain.vectordb.chroma import ChromaDB
@register_deserializable
class BaseBot(JSONSerializable):
    """
    Base class for a bot. This class is JSON serializable and can be registered as deserializable.
    The bot has an application that can add data and perform queries.
    """

    def __init__(self):
        """
        Initialize the bot with an application.
        The application is configured with an AppConfig, OpenAILlm, ChromaDB, and OpenAIEmbedder.
        """
        self.app = App(config=AppConfig(), llm=OpenAILlm(), db=ChromaDB(), embedder=OpenAIEmbedder())

    def add(self, data: Any, config: AddConfig=None):
        """
        Add data to the bot (to the vector database).
        Auto-dectects type only, so some data types might not be usable.

        :param data: data to embed
        :type data: Any
        :param config: configuration class instance, defaults to None
        :type config: AddConfig, optional
        """
        config = config if config else AddConfig()
        self.app.add(data, config=config)

    def query(self, query: str, config: BaseLlmConfig=None) -> str:
        """
        Query the bot

        :param query: the user query
        :type query: str
        :param config: configuration class instance, defaults to None
        :type config: BaseLlmConfig, optional
        :return: Answer
        :rtype: str
        """
        config = config if config else BaseLlmConfig()
        return self.app.query(query, config=config)

    def start(self):
        """
        Start the bot's functionality.
        This method should be implemented in subclasses.
        """
        raise NotImplementedError('Subclasses must implement the start method.')