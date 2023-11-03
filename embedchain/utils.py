import logging
import os
import re
import string
from typing import Any
from embedchain.models.data_type import DataType
def clean_string(text):
    """
    This function takes in a string and performs a series of text cleaning operations.

    Args:
        text (str): The text to be cleaned. This is expected to be a string.

    Returns:
        cleaned_text (str): The cleaned text after all the cleaning operations
        have been performed.
    """
    text = text.replace('\n', ' ')
    cleaned_text = re.sub('\\s+', ' ', text.strip())
    cleaned_text = cleaned_text.replace('\\', '')
    cleaned_text = cleaned_text.replace('#', ' ')
    cleaned_text = re.sub('([^\\w\\s])\\1*', '\\1', cleaned_text)
    return cleaned_text
def is_readable(s):
    """
    Heuristic to determine if a string is "readable" (mostly contains printable characters and forms meaningful words)

    :param s: string
    :return: True if the string is more than 95% printable.
    """
    try:
        printable_ratio = sum((c in string.printable for c in s)) / len(s)
    except ZeroDivisionError:
        logging.warning('Empty string processed as unreadable')
        printable_ratio = 0
    return printable_ratio > 0.95
def use_pysqlite3():
    """
    Swap std-lib sqlite3 with pysqlite3.
    """
    import platform
    import sqlite3
    if platform.system() == 'Linux' and sqlite3.sqlite_version_info < (3, 35, 0):
        try:
            import datetime
            import subprocess
            import sys
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pysqlite3-binary', '--quiet', '--disable-pip-version-check'])
            __import__('pysqlite3')
            sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
            print(f'{current_time} [embedchain] [INFO]', 'Swapped std-lib sqlite3 with pysqlite3 for ChromaDb compatibility.', f'Your original version was {sqlite3.sqlite_version}.')
        except Exception as e:
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]
            print(f'{current_time} [embedchain] [ERROR]', 'Failed to swap std-lib sqlite3 with pysqlite3 for ChromaDb compatibility.', 'Error:', e)
def format_source(source: str, limit: int=20) -> str:
    """
    Format a string to only take the first x and last x letters.
    This makes it easier to display a URL, keeping familiarity while ensuring a consistent length.
    If the string is too short, it is not sliced.
    """
    if len(source) > 2 * limit:
        return source[:limit] + '...' + source[-limit:]
    return source
def detect_datatype(source: Any) -> DataType:
    """
    Automatically detect the datatype of the given source.

    :param source: the source to base the detection on
    :return: data_type string
    """
    from urllib.parse import urlparse
    import requests
    import yaml

    def is_openapi_yaml(yaml_content):
        return 'openapi' in yaml_content and 'info' in yaml_content
    try:
        if not isinstance(source, str):
            raise ValueError('Source is not a string and thus cannot be a URL.')
        url = urlparse(source)
        if not all([url.scheme, url.netloc]) and url.scheme != 'file':
            raise ValueError('Not a valid URL.')
    except ValueError:
        url = False
    formatted_source = format_source(str(source), 30)
    if url:
        from langchain.document_loaders.youtube import ALLOWED_NETLOCK as YOUTUBE_ALLOWED_NETLOCS
        if url.netloc in YOUTUBE_ALLOWED_NETLOCS:
            logging.debug(f'Source of `{formatted_source}` detected as `youtube_video`.')
            return DataType.YOUTUBE_VIDEO
        if url.netloc in {'notion.so', 'notion.site'}:
            logging.debug(f'Source of `{formatted_source}` detected as `notion`.')
            return DataType.NOTION
        if url.path.endswith('.pdf'):
            logging.debug(f'Source of `{formatted_source}` detected as `pdf_file`.')
            return DataType.PDF_FILE
        if url.path.endswith('.xml'):
            logging.debug(f'Source of `{formatted_source}` detected as `sitemap`.')
            return DataType.SITEMAP
        if url.path.endswith('.csv'):
            logging.debug(f'Source of `{formatted_source}` detected as `csv`.')
            return DataType.CSV
        if url.path.endswith('.docx'):
            logging.debug(f'Source of `{formatted_source}` detected as `docx`.')
            return DataType.DOCX
        if url.path.endswith('.yaml'):
            try:
                response = requests.get(source)
                response.raise_for_status()
                try:
                    yaml_content = yaml.safe_load(response.text)
                except yaml.YAMLError as exc:
                    logging.error(f'Error parsing YAML: {exc}')
                    raise TypeError(f'Not a valid data type. Error loading YAML: {exc}')
                if is_openapi_yaml(yaml_content):
                    logging.debug(f'Source of `{formatted_source}` detected as `openapi`.')
                    return DataType.OPENAPI
                else:
                    logging.error(f"Source of `{formatted_source}` does not contain all the required                         fields of OpenAPI yaml. Check 'https://spec.openapis.org/oas/v3.1.0'")
                    raise TypeError("Not a valid data type. Check 'https://spec.openapis.org/oas/v3.1.0',                         make sure you have all the required fields in YAML config data")
            except requests.exceptions.RequestException as e:
                logging.error(f'Error fetching URL {formatted_source}: {e}')
        if url.path.endswith('.json'):
            logging.debug(f'Source of `{formatted_source}` detected as `json_file`.')
            return DataType.JSON
        if 'docs' in url.netloc or ('docs' in url.path and url.scheme != 'file'):
            logging.debug(f'Source of `{formatted_source}` detected as `docs_site`.')
            return DataType.DOCS_SITE
        logging.debug(f'Source of `{formatted_source}` detected as `web_page`.')
        return DataType.WEB_PAGE
    elif not isinstance(source, str):
        if isinstance(source, tuple) and len(source) == 2 and isinstance(source[0], str) and isinstance(source[1], str):
            logging.debug(f'Source of `{formatted_source}` detected as `qna_pair`.')
            return DataType.QNA_PAIR
        raise TypeError("Source is not a string and a valid non-string type could not be detected. If you want to embed it, please stringify it, for instance by using `str(source)` or `(', ').join(source)`.")
    elif os.path.isfile(source):
        if source.endswith('.docx'):
            logging.debug(f'Source of `{formatted_source}` detected as `docx`.')
            return DataType.DOCX
        if source.endswith('.csv'):
            logging.debug(f'Source of `{formatted_source}` detected as `csv`.')
            return DataType.CSV
        if source.endswith('.xml'):
            logging.debug(f'Source of `{formatted_source}` detected as `xml`.')
            return DataType.XML
        if source.endswith('.yaml'):
            with open(source, 'r') as file:
                yaml_content = yaml.safe_load(file)
                if is_openapi_yaml(yaml_content):
                    logging.debug(f'Source of `{formatted_source}` detected as `openapi`.')
                    return DataType.OPENAPI
                else:
                    logging.error(f"Source of `{formatted_source}` does not contain all the required                                   fields of OpenAPI yaml. Check 'https://spec.openapis.org/oas/v3.1.0'")
                    raise ValueError("Invalid YAML data. Check 'https://spec.openapis.org/oas/v3.1.0',                         make sure to add all the required params")
        if source.endswith('.json'):
            logging.debug(f'Source of `{formatted_source}` detected as `json`.')
            return DataType.JSON
        raise ValueError('Source points to a valid file, but based on the filename, no `data_type` can be detected. Please be aware, that not all data_types allow conventional file references, some require the use of the `file URI scheme`. Please refer to the embedchain documentation (https://docs.embedchain.ai/advanced/data_types#remote-data-types).')
    else:
        logging.debug(f'Source of `{formatted_source}` detected as `text`.')
        return DataType.TEXT