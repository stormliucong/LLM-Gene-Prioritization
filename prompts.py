from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
import os
from dotenv import load_dotenv
load_dotenv()
from llama_index.core import (
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.core import Settings


class RagQuery:
    def __init__(self, emb_model, llm_model):
        if emb_model == "text-embedding-3-small":
            index_dir = "./rag_llm/data/text-embedding-3-small-index"
            index_id = "text-embedding-3-small"
        if emb_model == "text-embedding-3-large":
            index_dir = "./rag_llm/data/text-embedding-3-large-index"
            index_id = "text-embedding-3-large"
        
        llm = OpenAI(model=llm_model)
        # Load Index
        if not os.path.exists(index_dir):
            raise Exception(f"Index directory {index_dir} does not exist.")
        else:
            # Rebuild storage context
            storage_context = StorageContext.from_defaults(persist_dir=index_dir)
            # Load index
            embed_model = OpenAIEmbedding(model=emb_model,embed_batch_size=1000)
            index = load_index_from_storage(storage_context, index_id=index_id)  
        
        self.query_engine = index.as_query_engine(llm=llm, embed_model = embed_model, chunk_size=1028, chunk_overlap=100, similarity_top_k=10)

        
    def query_rag(self, prompt):
        response = self.query_engine.query(prompt)
        return (str(response))

if __name__ == "__main__":
    top_n = 10
    clinical_description = 'The patient is a 45-year, with the following symptoms: shortness of breath, fatigue, and chest pain. The patient has a history of heart disease in the family.'
    content = f'Consider you are a genetic counselor. The phenotype description of the patient is {clinical_description}. Can you suggest a list of {top_n} possible genes to test? Please consider the phenotype gene relationship, and use the knowledge you have trained on. No need to access the real-time database to generate outcomes. Please return gene symbols as a comma-separated list. Example: "ABC1, BRAC2, BRAC1" or "Not Applicable" if you can not provide the result.'
    large_index = RagQuery(emb_model="text-embedding-3-small", llm_model="gpt-4")
    response = large_index.query_rag(content)
    print(response)