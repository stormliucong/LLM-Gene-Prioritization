# LLM-Gene-Prioritization
Assessing the Utility of Large Language Models for Phenotype-Driven Gene Prioritization in Rare Genetic Disorder Diagnosis

### Features
- We evaluated different zero-short prompts for phenotypic-driven gene ranking tasks using ChatGPT 
- ChatGPT3.5-turbo, ChatGPT4, LLama2-Chat-7B, LLama2-Chat-13B, LLama2-Chat-70B were evaluated
- Different input clinical features - HPO names and free-text were evaluated
- Top 10 and Top 50 results were evaluated
- We evaluated the variablity of ChatGPT by repeating the experiment three times
- Multiple prompts were evaluated
- Additional evaluations:
    - evaluated with few-shot prompts
    - evaluated with RAG methods using Llama-index.
    - evaluated with new dataset after 2023

### Get started

#### Set up env
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir data
mkdir data/raw
```
#### Create OpenAI API key file
- Create a `.env` file 
```sh
OPENAI_API_KEY=sk-inputyouropenaiapikeyhere
```

#### Execute experiements
- `experiment_*.py`.Run llm experiements. Check usage and `data/input` and `data/llm_response` for details
    - `experiment_gpt.py` is outdated due to openai API update; we intentionally keep it not updated because the original experiment was conducted using the old API specs.
    - Before execute `experiment_rag.py`, make sure the index is created. Check `rag_llm` for details.
- `evaluations.py. Run evaluation for llm responses. Check usage and `data/evaluation` for details.
    
