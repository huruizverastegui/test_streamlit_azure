import streamlit as st
import os
import openai
import llama_index
from llama_index.llms.openai import OpenAI
try:
  from llama_index import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
except ImportError:
  from llama_index.core import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader

from azure.storage.blob import BlobServiceClient
from io import BytesIO

from llama_index.core.extractors import (
    TitleExtractor,
    QuestionsAnsweredExtractor,
)
from llama_index.core.node_parser import TokenTextSplitter
from helpers.azhelpers import upload_to_azure_storage, list_all_containers, list_all_files, delete_all_files, create_new_container


azure_storage_account_name = str.encode(os.environ["AZURE_STORAGE_ACCOUNT_NAME"])
azure_storage_account_key = str.encode(os.environ["AZURE_STORAGE_ACCOUNT_KEY"])
connection_string_blob = str.encode(os.environ["CONNECTION_STRING_BLOB"])
container_name = None

st.write(azure_storage_account_name)
