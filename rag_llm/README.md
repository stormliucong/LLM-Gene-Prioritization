## RAG program for RAG experiement



### How to run index

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

#### Download hpo annotation
- Download GENES_TO_PHENOTYPES [from hpo website](https://hpo.jax.org/data/annotations)
- Upload `genes_to_phenotype.txt` to `./data/raw`

#### Create files
```sh
python break_files_by_gene.py
python break_files_by_phenotype.py
```


#### Index files 
```sh
python index_with_gene.py
python index_with_phenotype.py
```
- Run this repeately until see `No new documents to index.` message.

