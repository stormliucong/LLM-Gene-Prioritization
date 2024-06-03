from llama_index.llms.openai import OpenAI
import os

index_dir = "./data/text-embedding-3-small-index"

from llama_index.core import (
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)

# Load Index
if not os.path.exists(index_dir):
   raise Exception(f"Index directory {index_dir} does not exist.")
else:
    # Rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir=index_dir)
    # Load index
    index = load_index_from_storage(storage_context, index_id="text-embedding-3-small")  
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


    