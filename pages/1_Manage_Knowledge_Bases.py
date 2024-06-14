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

blob_service_client = BlobServiceClient.from_connection_string(f"DefaultEndpointsProtocol=https;AccountName={azure_storage_account_name};AccountKey={azure_storage_account_key}")

with st.expander("Create a new Knowledge Base", expanded=False):
    new_container_name = st.text_input("Name your new Knowledge Base")
    create_container = st.button("Create", type='primary')
    if create_container:
        created_container_name = create_new_container(new_container_name)
        st.success(f"Created new Knowledge Base: {new_container_name}")
        container_name = created_container_name


container_list = list()
containers = blob_service_client.list_containers()
for container in containers:
    if "genai-" in container.name:
        container_list.append(container.name)
    
st.write(list_all_containers())
