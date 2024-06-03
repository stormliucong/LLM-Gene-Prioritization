### How to run

#### Set up env
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdir data
mkdir data/raw
```

#### Download hpo annotation
- Download GENES_TO_PHENOTYPES [from hpo website](https://hpo.jax.org/data/annotations)
- Upload `genes_to_phenotype.txt` to `./data/raw`

#### Create files
```sh
python break_files_by_gene.py
```

#### Index files 
```sh
python index.py
```
- Run this repeately until see `No new documents to index.` message.
