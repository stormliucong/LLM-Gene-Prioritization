import os
import pandas as pd
# nload genes_to_phenotype.txt from HPO website and put it under data/raw
hpo_annotation_path = os.path.join(os.path.dirname(__file__), 'data/raw/genes_to_phenotype.txt')

# If not exist folder 'data/files'
if not os.path.exists(os.path.join(os.path.dirname(__file__), 'data/files')):
    os.mkdir(os.path.join(os.path.dirname(__file__), 'data/files'))
hpo_annotation_df = pd.read_csv(hpo_annotation_path, sep='\t')
# Group By gene_symbol and pu hpo_name
hpo_annotation_df = hpo_annotation_df[['hpo_name','hpo_id','gene_symbol']].drop_duplicates()
hpo_annotation_df = hpo_annotation_df[hpo_annotation_df['gene_symbol']!= "-"]
hpo_annotation_df = hpo_annotation_df.groupby(['hpo_name','hpo_id'])['gene_symbol'].apply(lambda x: ','.join(x)).reset_index()
# gene symbol match words

# Save each phenotype to a file
for hpo_id in hpo_annotation_df['hpo_id'].tolist():
    gene_df = hpo_annotation_df[hpo_annotation_df['hpo_id']==hpo_id]
    hpo_name = gene_df['hpo_name'].values[0]
    # replace ':' to '_'
    hpo_id = hpo_id.replace(':', '_')
    file_name = f'genes_associated_with_{hpo_id}.txt'
    # if file not exist
    if os.path.exists(os.path.join(os.path.dirname(__file__), f'data/files/{file_name}')):
        continue
    file_content = f"The phenotype {hpo_name} is associated with the following genes {gene_df['gene_symbol'].values[0]}"
    with open(os.path.join(os.path.dirname(__file__), f'data/files/{file_name}'), 'w') as f:
        f.write(file_content)