### Dataset for Evaluation

- `HPO_input.zip` contains HPO-based input dataset collected from the Phen2Gene paper
    - After unziped, there are two folders, `HPO_names` contains input represented using HPO names. `Original_data` contains input represented using HPO IDs. There is a `probe_info` file contains final diagnsed gene for each case.
- `free_text_pmid_input.csv` contains free-text based input manually collected from publications before 2021
- `new_free_text_pmid_input.csv` contains both previously free-text based input and free-text based input manually collected from publications after 2023. We intentionally added some genes which is overlapped with previous collection in order to avoid biases introduced by different genes.

### Dataset Access & Citation
- Original (Pre-2021) dataset is from Phen2Gene paper (https://academic.oup.com/nargab/article/2/2/lqaa032/5843800?login=false#442686434) and all the PMIDs are included in the csv files.
- TAF1 dataset (14 cases): Phen2Gene reference number 35
- Columbia U dataset (27 cases): Phen2Gene reference number 13
- DGD dataset (85 cases): Phen2Gene reference number 36
- CSH dataset (72 cases): Phen2Gene reference number 37 - 97
- AJHG dataset (83 cases): Phen2Gene reference number 98 - 111
- Other (4 cases): The PMID is in the 'free_text_pmid_input.csv'
- Post-2023 dataset can be traced by PMIDs in the `new_free_text_pmid_input.csv`
