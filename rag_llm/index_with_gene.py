from dotenv import load_dotenv
import os
import pandas as pd
import json
import logging
from tqdm import tqdm
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
    PromptTemplate,
    Settings
)
from llama_index.core.query_pipeline import QueryPipeline
from llama_index.core import PromptTemplate
from llama_index.agent.openai import OpenAIAssistantAgent
from llama_index.core.agent import ReActAgent

from argparse import ArgumentParser
import logging

parser = ArgumentParser()
parser.add_argument("--batch_size", type=int, default=1000)
parser.add_argument("--model", type=str, default="text-embedding-3-small")
args = parser.parse_args()




logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

load_dotenv()

BATCH_SIZE = args.batch_size
MODEL = args.model

Settings.llm = OpenAI(model="gpt-3.5-turbo")
embed_model = OpenAIEmbedding(model=f"{MODEL}",embed_batch_size=1000)
Settings.embed_model = embed_model
Settings.chunk_size = 1028
Settings.chunk_overlap = 100


reader = SimpleDirectoryReader("./data/files/genes")
docs = reader.load_data()
logging.info(f"Loaded {len(docs)} documents.")

# define index directory
index_dir = f"./data/{MODEL}-index-gene"
# remove docs from alread indexed files
indexed_files_list = []
indexed_files_log = f'./logs/{MODEL}-indexed.txt'
if os.path.exists(indexed_files_log):
    with open(indexed_files_log, "r") as f:
        # this log file contains all the previously indexed files
        indexed_files_list = f.read().splitlines()
        indexed_files_list = [f.strip() for f in indexed_files_list]
    orignal_docs = docs.copy()
    for doc in orignal_docs:
        if doc.metadata['file_name'] in indexed_files_list:
            docs.remove(doc)
else:
    # if folder not exist create one
    if not os.path.exists('./logs'):
        os.mkdir('./logs')
logging.info(f"Removed {len(indexed_files_list)} already indexed files.")
logging.info(f"Remaining {len(docs)} documents to index.")

if len(docs) == 0:
    logging.info("No new documents to index.")
    exit()

if not os.path.exists(index_dir):
    index = VectorStoreIndex.from_documents([])
    # save index to disk
    index.set_index_id(f"{MODEL}")
    index.storage_context.persist(index_dir)
else:
    # Rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir=index_dir)
    # Load index
    index = load_index_from_storage(storage_context, index_id=f"{MODEL}")    

# Insert new documents by batch
for i in tqdm(range(0, len(docs), BATCH_SIZE)):
    start = i
    end = min(i + BATCH_SIZE, len(docs))
    batch_docs = docs[start:end]
    # Parse documents into nodes
    parser = SimpleNodeParser()
    new_nodes = parser.get_nodes_from_documents(batch_docs)
    # Add nodes to the existing index
    try:
        index.insert_nodes(new_nodes)
        # if success, add to indexed_files_list
        indexed_files_list.extend([doc.metadata['file_name'] for doc in batch_docs])
        logging.info(f"Adding new nodes to the existing index... {start} to {end}")
    except Exception as e:
        logging.error(f"Error adding nodes to index... {start} to {end}")
        logging.error(e)
    # Persist the index after inserting the new document
    index.storage_context.persist(index_dir)
    # save indexed_files_list to logs
    with open(indexed_files_log, "w") as f:
        f.write('\n'.join(indexed_files_list))






