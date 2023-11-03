import os
import shutil
from unittest.mock import patch
import pytest
from chromadb.config import Settings
from embedchain import App
from embedchain.config import AppConfig, ChromaDbConfig
from embedchain.vectordb.chroma import ChromaDB
os.environ['OPENAI_API_KEY'] = 'test-api-key'
@pytest.fixture
def chroma_db():
    return ChromaDB(config=ChromaDbConfig(host='test-host', port='1234'))
@pytest.fixture
def app_with_settings():
    chroma_config = ChromaDbConfig(allow_reset=True, dir='test-db')
    app_config = AppConfig(collect_metrics=False)
    return App(config=app_config, db_config=chroma_config)
@pytest.fixture(scope='session', autouse=True)
def cleanup_db():
    yield
    try:
        shutil.rmtree('test-db')
    except OSError as e:
        print('Error: %s - %s.' % (e.filename, e.strerror))
def test_chroma_db_init_with_host_and_port(chroma_db):
    settings = chroma_db.client.get_settings()
    assert settings.chroma_server_host == 'test-host'
    assert settings.chroma_server_http_port == '1234'
def test_chroma_db_init_with_basic_auth():
    chroma_config = {'host': 'test-host', 'port': '1234', 'chroma_settings': {'chroma_client_auth_provider': 'chromadb.auth.basic.BasicAuthClientProvider', 'chroma_client_auth_credentials': 'admin:admin'}}
    db = ChromaDB(config=ChromaDbConfig(**chroma_config))
    settings = db.client.get_settings()
    assert settings.chroma_server_host == 'test-host'
    assert settings.chroma_server_http_port == '1234'
    assert settings.chroma_client_auth_provider == chroma_config['chroma_settings']['chroma_client_auth_provider']
    assert settings.chroma_client_auth_credentials == chroma_config['chroma_settings']['chroma_client_auth_credentials']
@patch('embedchain.vectordb.chroma.chromadb.Client')
def test_app_init_with_host_and_port(mock_client):
    host = 'test-host'
    port = '1234'
    config = AppConfig(collect_metrics=False)
    db_config = ChromaDbConfig(host=host, port=port)
    _app = App(config, db_config=db_config)
    called_settings: Settings = mock_client.call_args[0][0]
    assert called_settings.chroma_server_host == host
    assert called_settings.chroma_server_http_port == port
@patch('embedchain.vectordb.chroma.chromadb.Client')
def test_app_init_with_host_and_port_none(mock_client):
    _app = App(config=AppConfig(collect_metrics=False), db_config=ChromaDbConfig(allow_reset=True, dir='test-db'))
    called_settings: Settings = mock_client.call_args[0][0]
    assert called_settings.chroma_server_host is None
    assert called_settings.chroma_server_http_port is None
def test_chroma_db_duplicates_throw_warning(caplog):
    app = App(config=AppConfig(collect_metrics=False), db_config=ChromaDbConfig(allow_reset=True, dir='test-db'))
    app.db.collection.add(embeddings=[[0, 0, 0]], ids=['0'])
    app.db.collection.add(embeddings=[[0, 0, 0]], ids=['0'])
    assert 'Insert of existing embedding ID: 0' in caplog.text
    assert 'Add of existing embedding ID: 0' in caplog.text
    app.db.reset()
def test_chroma_db_duplicates_collections_no_warning(caplog):
    app = App(config=AppConfig(collect_metrics=False), db_config=ChromaDbConfig(allow_reset=True, dir='test-db'))
    app.set_collection_name('test_collection_1')
    app.db.collection.add(embeddings=[[0, 0, 0]], ids=['0'])
    app.set_collection_name('test_collection_2')
    app.db.collection.add(embeddings=[[0, 0, 0]], ids=['0'])
    assert 'Insert of existing embedding ID: 0' not in caplog.text
    assert 'Add of existing embedding ID: 0' not in caplog.text
    app.db.reset()
    app.set_collection_name('test_collection_1')
    app.db.reset()
def test_chroma_db_collection_init_with_default_collection():
    app = App(config=AppConfig(collect_metrics=False), db_config=ChromaDbConfig(allow_reset=True, dir='test-db'))
    assert app.db.collection.name == 'embedchain_store'
def test_chroma_db_collection_init_with_custom_collection():
    """
    Tests the initialization of chroma db collection with a custom collection name.

    This test function asserts that the collection name of the database in the app instance is set to 'test_collection'
    when the set_collection_name method is called with 'test_collection' as the argument.
    """
    app = App(config=AppConfig(collect_metrics=False), db_config=ChromaDbConfig(allow_reset=True, dir='test-db'))
    app.set_collection_name(name='test_collection')
    assert app.db.collection.name == 'test_collection'
def test_chroma_db_collection_set_collection_name():
    """
    Test case for the set_collection_name method of the App class.
    This test case checks if the method correctly sets the name of the collection in the database.
    """
    app = App(config=AppConfig(collect_metrics=False), db_config=ChromaDbConfig(allow_reset=True, dir='test-db'))
    app.set_collection_name('test_collection')
    assert app.db.collection.name == 'test_collection'
def test_chroma_db_collection_changes_encapsulated():
    """
    Test to ensure that changes to the Chroma DB collection are encapsulated.
    This test creates an App instance, sets the collection name, adds an embedding,
    changes the collection name, and verifies that the count of embeddings in each
    collection is as expected after each operation. It also tests the reset functionality.
    """
    app = App(config=AppConfig(collect_metrics=False), db_config=ChromaDbConfig(allow_reset=True, dir='test-db'))
    app.set_collection_name('test_collection_1')
    assert app.db.count() == 0
    app.db.collection.add(embeddings=[0, 0, 0], ids=['0'])
    assert app.db.count() == 1
    app.set_collection_name('test_collection_2')
    assert app.db.count() == 0
    app.db.collection.add(embeddings=[0, 0, 0], ids=['0'])
    app.set_collection_name('test_collection_1')
    assert app.db.count() == 1
    app.db.reset()
    app.set_collection_name('test_collection_2')
    app.db.reset()
def test_chroma_db_collection_add_with_skip_embedding(app_with_settings):
    """
    Test function for the 'add' method of the ChromaDB class with 'skip_embedding' set to True.
    
    This function tests the following:
    - The database is initially empty.
    - After adding an entry with 'skip_embedding' set to True, the database count increases by 1.
    - The added entry can be retrieved correctly and its 'embeddings' field is None.
    - The 'query' method works correctly with 'skip_embedding' set to True.

    :param app_with_settings: An instance of the application with settings configured.
    :type app_with_settings: fixture
    """
    app_with_settings.db.reset()
    assert app_with_settings.db.count() == 0
    app_with_settings.db.add(embeddings=[[0, 0, 0]], documents=['document'], metadatas=[{'url': 'url_1', 'doc_id': 'doc_id_1'}], ids=['id'], skip_embedding=True)
    assert app_with_settings.db.count() == 1
    data = app_with_settings.db.get(['id'], limit=1)
    expected_value = {'documents': ['document'], 'embeddings': None, 'ids': ['id'], 'metadatas': [{'url': 'url_1', 'doc_id': 'doc_id_1'}]}
    assert data == expected_value
    data_without_citations = app_with_settings.db.query(input_query=[0, 0, 0], where={}, n_results=1, skip_embedding=True)
    expected_value_without_citations = ['document']
    assert data_without_citations == expected_value_without_citations
    app_with_settings.db.reset()
def test_chroma_db_collection_add_with_invalid_inputs(app_with_settings):
    """
    Test case for the method 'add' of the 'db' attribute of the 'app_with_settings' object.
    This test case checks the behavior of the 'add' method when invalid inputs are provided.

    :param app_with_settings: The application object with settings, which includes a 'db' attribute.
    :type app_with_settings: object
    """
    app_with_settings.db.reset()
    assert app_with_settings.db.count() == 0
    with pytest.raises(ValueError):
        app_with_settings.db.add(embeddings=[[0, 0, 0]], documents=['document', 'document2'], metadatas=[{'value': 'somevalue'}], ids=['id'], skip_embedding=True)
    assert app_with_settings.db.count() == 0
    with pytest.raises(ValueError):
        app_with_settings.db.add(embeddings=None, documents=['document', 'document2'], metadatas=[{'value': 'somevalue'}], ids=['id'], skip_embedding=True)
    assert app_with_settings.db.count() == 0
    app_with_settings.db.reset()
def test_chroma_db_collection_collections_are_persistent():
    """
    Test to ensure that collections in the Chroma DB are persistent.
    This test checks if an item added to a collection still exists after the app is deleted and recreated.
    """
    app = App(config=AppConfig(collect_metrics=False), db_config=ChromaDbConfig(allow_reset=True, dir='test-db'))
    app.set_collection_name('test_collection_1')
    app.db.collection.add(embeddings=[[0, 0, 0]], ids=['0'])
    del app
    app = App(config=AppConfig(collect_metrics=False), db_config=ChromaDbConfig(allow_reset=True, dir='test-db'))
    app.set_collection_name('test_collection_1')
    assert app.db.count() == 1
    app.db.reset()
def test_chroma_db_collection_parallel_collections():
    """
    This function tests the parallel collections in ChromaDB. It creates two apps with different collections and checks the count of items in each collection.
    It also tests the functionality of resetting the DB and changing the collection name.
    """
    app1 = App(AppConfig(collection_name='test_collection_1', collect_metrics=False), db_config=ChromaDbConfig(allow_reset=True, dir='test-db'))
    app2 = App(AppConfig(collection_name='test_collection_2', collect_metrics=False), db_config=ChromaDbConfig(allow_reset=True, dir='test-db'))
    app1.db.reset()
    app2.db.reset()
    app1.db.collection.add(embeddings=[0, 0, 0], ids=['0'])
    assert app1.db.count() == 1
    assert app2.db.count() == 0
    app1.db.collection.add(embeddings=[[0, 0, 0], [1, 1, 1]], ids=['1', '2'])
    app2.db.collection.add(embeddings=[0, 0, 0], ids=['0'])
    app1.set_collection_name('test_collection_2')
    assert app1.db.count() == 1
    app2.set_collection_name('test_collection_1')
    assert app2.db.count() == 3
    app1.db.reset()
    app2.db.reset()
def test_chroma_db_collection_ids_share_collections():
    """
    Test case to check if two different apps sharing the same collection name 
    in the database have their data reflected in each other's collections.

    The test involves creating two apps with different IDs but the same collection name.
    Then, embeddings are added to both collections. The count of embeddings is checked 
    after each addition to ensure that the data is reflected in both collections.
    Finally, the collections are reset to ensure no data remains after the test.
    """
    app1 = App(AppConfig(id='new_app_id_1', collect_metrics=False), db_config=ChromaDbConfig(allow_reset=True, dir='test-db'))
    app1.set_collection_name('one_collection')
    app2 = App(AppConfig(id='new_app_id_2', collect_metrics=False), db_config=ChromaDbConfig(allow_reset=True, dir='test-db'))
    app2.set_collection_name('one_collection')
    app1.db.collection.add(embeddings=[[0, 0, 0], [1, 1, 1]], ids=['0', '1'])
    app2.db.collection.add(embeddings=[0, 0, 0], ids=['2'])
    assert app1.db.count() == 3
    assert app2.db.count() == 3
    app1.db.reset()
    app2.db.reset()
def test_chroma_db_collection_reset():
    """
    Tests the reset functionality of the ChromaDB collection. 
    The test creates four apps with different collections and adds an embedding to each. 
    It then resets the collection for each app and checks if the count of embeddings in each collection is as expected.
    """
    app1 = App(AppConfig(id='new_app_id_1', collect_metrics=False), db_config=ChromaDbConfig(allow_reset=True, dir='test-db'))
    app1.set_collection_name('one_collection')
    app2 = App(AppConfig(id='new_app_id_2', collect_metrics=False), db_config=ChromaDbConfig(allow_reset=True, dir='test-db'))
    app2.set_collection_name('two_collection')
    app3 = App(AppConfig(id='new_app_id_1', collect_metrics=False), db_config=ChromaDbConfig(allow_reset=True, dir='test-db'))
    app3.set_collection_name('three_collection')
    app4 = App(AppConfig(id='new_app_id_4', collect_metrics=False), db_config=ChromaDbConfig(allow_reset=True, dir='test-db'))
    app4.set_collection_name('four_collection')
    app1.db.collection.add(embeddings=[0, 0, 0], ids=['1'])
    app2.db.collection.add(embeddings=[0, 0, 0], ids=['2'])
    app3.db.collection.add(embeddings=[0, 0, 0], ids=['3'])
    app4.db.collection.add(embeddings=[0, 0, 0], ids=['4'])
    app1.db.reset()
    assert app1.db.count() == 0
    assert app2.db.count() == 1
    assert app3.db.count() == 1
    assert app4.db.count() == 1
    app2.db.reset()
    app3.db.reset()
    app4.db.reset()
def test_chroma_db_collection_query(app_with_settings):
    """
    Test the query functionality of the chroma db collection.

    This function tests the following:
    - The db collection count increases as items are added
    - The db collection can be queried correctly without citations
    - The db collection can be queried correctly with citations

    :param app_with_settings: The application with settings to test.
    """
    app_with_settings.db.reset()
    assert app_with_settings.db.count() == 0
    app_with_settings.db.add(embeddings=[[0, 0, 0]], documents=['document'], metadatas=[{'url': 'url_1', 'doc_id': 'doc_id_1'}], ids=['id'], skip_embedding=True)
    assert app_with_settings.db.count() == 1
    app_with_settings.db.add(embeddings=[[0, 1, 0]], documents=['document2'], metadatas=[{'url': 'url_2', 'doc_id': 'doc_id_2'}], ids=['id2'], skip_embedding=True)
    assert app_with_settings.db.count() == 2
    data_without_citations = app_with_settings.db.query(input_query=[0, 0, 0], where={}, n_results=2, skip_embedding=True)
    expected_value_without_citations = ['document', 'document2']
    assert data_without_citations == expected_value_without_citations
    data_with_citations = app_with_settings.db.query(input_query=[0, 0, 0], where={}, n_results=2, skip_embedding=True, citations=True)
    expected_value_with_citations = [('document', 'url_1', 'doc_id_1'), ('document2', 'url_2', 'doc_id_2')]
    assert data_with_citations == expected_value_with_citations
    app_with_settings.db.reset()