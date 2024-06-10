### Dataset for Evaluation

- `HPO_input.zip` contains HPO-based input dataset collected from the Phen2Gene paper
    - After unziped, there are two folders, `HPO_names` contains input represented using HPO names. `Original_data` contains input represented using HPO IDs. There is a `probe_info` file contains final diagnsed gene for each case.
- `free_text_pmid_input.csv` contains free-text based input manually collected from publications before 2021
- `new_free_text_pmid_input.csv` contains free-text based input manually collected from publications after 2023. We intentionally added some genes which is overlapped with previous collection in order to avoid biases introduced by different genes.
