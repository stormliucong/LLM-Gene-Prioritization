import os
import pandas as pd
# nload genes_to_phenotype.txt from HPO website and put it under data/raw
hpo_annotation_path = os.path.join(os.path.dirname(__file__), 'data/raw/genes_to_phenotype.txt')

# If not exist folder 'data/files'
if not os.path.exists(os.path.join(os.path.dirname(__file__), 'data/files')):
    os.mkdir(os.path.join(os.path.dirname(__file__), 'data/files'))
hpo_annotation_df = pd.read_csv(hpo_annotation_path, sep='\t')
# Group By gene_symbol and pu hpo_name
hpo_annotation_df = hpo_annotation_df[['hpo_name','gene_symbol']].drop_duplicates()
hpo_annotation_df = hpo_annotation_df.groupby(['gene_symbol'])['hpo_name'].apply(lambda x: ','.join(x)).reset_index()
# gene symbol match words
hpo_annotation_df = hpo_annotation_df[hpo_annotation_df['gene_symbol']!= "-"]

# Save each gene to a file
for gene in hpo_annotation_df['gene_symbol'].tolist():
    file_name = f'phenotypes_associated_with_{gene}.txt'
    # if file not exist
    if os.path.exists(os.path.join(os.path.dirname(__file__), f'data/files/{file_name}')):
        continue
    gene_df = hpo_annotation_df[hpo_annotation_df['gene_symbol']==gene]
    file_content = f"The phenotypes associated with gene {gene} including {gene_df['hpo_name'].values[0]}"
    with open(os.path.join(os.path.dirname(__file__), f'data/files/{file_name}'), 'w') as f:
        f.write(file_content)