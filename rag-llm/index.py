from dotenv import load_dotenv
import os
import pandas as pd
import json
import logging
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




logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

load_dotenv()

Settings.llm = OpenAI(model="gpt-3.5-turbo")
embed_model = OpenAIEmbedding(model="text-embedding-3-small",embed_batch_size=10)
Settings.embed_model = embed_model

BATCH_SIZE = 2


reader = SimpleDirectoryReader("./data/files")
docs = reader.load_data()
logging.info(f"Loaded {len(docs)} documents.")

index_dir = "./data/text-embedding-3-small-index"
# remove docs from alread indexed files
indexed_files_log = './logs/text-embedding-3-small-indexed.txt'
if os.path.exists(indexed_files_log):
    with open(indexed_files_log, "r") as f:
        indexed_files_list = f.read().splitlines()
        indexed_files_list = [f.strip() for f in indexed_files_list]
    orignal_docs = docs.copy()
    for doc in orignal_docs:
        if doc.metadata['file_name'] in indexed_files_list:
            docs.remove(doc)
logging.info(f"Removed {len(indexed_files_list)} already indexed files.")
logging.info(f"Remaining {len(docs)} documents to index.")

# if len(docs) == 0:
#     logging.info("No new documents to index.")
#     exit()

if not os.path.exists(index_dir):
    index = VectorStoreIndex.from_documents([])
    # save index to disk
    index.set_index_id("text-embedding-3-small")
    index.storage_context.persist(index_dir)
else:
    # Rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir=index_dir)
    # Load index
    index = load_index_from_storage(storage_context, index_id="text-embedding-3-small")    

# Insert new documents by batch
for i in range(0, len(docs), BATCH_SIZE):
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

# try chaining basic prompts
# https://docs.llamaindex.ai/en/stable/examples/pipeline/query_pipeline/
phenotype_list = ["abnormality otitis"]
phenotypes = ','.join(phenotype_list)
prompt_str = f"Give top 10 genes likely caused the following phenotypes {phenotypes}. Output format example, [GENE1, GENE2, GENE3, ...]"
# prompt_tmpl = PromptTemplate(prompt_str)

llm = OpenAI(model="gpt-3.5-turbo")
query_engine = index.as_query_engine(llm=llm, similarity_top_k=5)
response = query_engine.query(prompt_str)
print(str(response))



