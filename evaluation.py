import os
import requests
import re
import pandas as pd
import logging
import json
import argparse



def evaluate_completeness(gpt_response, all_symbol_list, top_n):
  '''
  Try to grep a GENE SYMBOL (using regular expression)
  [A-Z0-9]+
  '''
  logging.debug('gpt_response: {}'.format(gpt_response))
  pattern = r'[ ,.!?\n]+'
  tokens = re.split(pattern, gpt_response)
  tokens = [token.strip() for token in tokens if len(token) > 1]
  logging.debug('tokens: {}'.format(tokens))
  
  overlapped_genes = set(tokens) & set(all_symbol_list)
  logging.debug('overlapped_genes: {}'.format(overlapped_genes))
  
  if len(overlapped_genes) > int(int(top_n)/2):
    return 1
  else:
    return 0

def evaluate_accuracy(gpt_response, true_gene_alias):
  '''
  Match greped GENE SYMBOL with true_gene_symbol
  '''
  logging.debug('gpt_response: {}'.format(gpt_response))
  pattern = r'[ ,.!?\n]+'
  tokens = re.split(pattern, gpt_response)
  tokens = [token.strip() for token in tokens if len(token) > 1]
  logging.debug('tokens: {}'.format(tokens))
  for true_gene_symbol in true_gene_alias:
    logging.debug('true_gene_symbol: {}'.format(true_gene_symbol))
    if true_gene_symbol in set(tokens):
      return 1
  return 0

def evaluate_fulfillment(gpt_response, top_n):
  '''
  Try to match predifined JSON (using regular expression)
  \{"gene_list"\s*:\s*"(?:[A-Z0-9]+(?:\s*,\s*[A-Z0-9]+)*)"\}
  '''
  na_regex = re.compile(re.escape("not applicable"), re.IGNORECASE)
  na_m = re.findall(na_regex, gpt_response)
  if len(na_m) == 0:
    is_na_format = False
  else:
    is_na_format = True
      
  gene_regex = rf'[\w|-]+(?:,\s*[\w|-]+)+'

  gene_list = re.findall(gene_regex, gpt_response)
  if len(gene_list) == 0:
    is_gene_list_format = False
  else:
    longest_m = max(gene_list, key=len)
    is_gene_list_format = (len(longest_m.split(',')) == int(top_n))
  if is_gene_list_format or is_na_format:
    return 1
  else:
    return 0

def get_gpt_response(file):
  with open(file, 'r') as f:
    text = f.read() 
    return text
  
def get_hgnc_complete_list(symbol_json_file='./hgnc_complete_set_2020-10-01.json'):
  # read json from url 
  if not os.path.exists(symbol_json_file):
    logging.info('Downloading HGNC complete list')
    url = "https://ftp.ebi.ac.uk/pub/databases/genenames/hgnc/archive/quarterly/json/hgnc_complete_set_2020-10-01.json"
    gene_list_json = requests.get(url).json()['response']['docs']
    symbol_list = []
    for item in gene_list_json:
      
      symbol = item.get("symbol", "").upper().replace(" ", "")
      alias_symbol = item.get("alias_symbol", [])
      alias_symbol = [alias.upper().replace(" ", "") for alias in alias_symbol]
      prev_symbol = item.get("prev_symbol", [])
      prev_symbol = [prev.upper().replace(" ", "") for prev in prev_symbol]      
      if symbol != '': 
        symbol_list.append({"symbol": symbol, "other": symbol})
        for alias in alias_symbol:
          symbol_list.append({"symbol": symbol, "other": alias})
        for prev in prev_symbol:
          symbol_list.append({"symbol": symbol, "other": prev})
    logging.info('HGNC complete list downloaded')
    logging.info('length of HGNC complete list: {}'.format(len(symbol_list)))
    with open(symbol_json_file, 'w') as f:
      json.dump(symbol_list, f)
  else:
    with open(symbol_json_file, 'r') as f:
      logging.info('Reading HGNC complete list from local file')
      symbol_list = json.load(f)
      logging.info('length of HGNC complete list: {}'.format(len(symbol_list)))
  return symbol_list


if __name__ == '__main__':
  
  # parse argument
  parser = argparse.ArgumentParser()
  parser.add_argument('--input_dir', type=str, help='input directory. output directory from experiment_*.py')
  parser.add_argument('--output_file', type=str, help='output file')
  parser.add_argument('--log_file_name', type=str, default='evaluation.log', help='log file name')
  args = parser.parse_args()
  
  print(args.log_file_name)
   
  # add time stamp to logging
  logging.basicConfig(level=logging.INFO,
                    filename=args.log_file_name,
                    format='%(asctime)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
  
  output_dir = args.input_dir
  hgnc_complete_list = get_hgnc_complete_list()
  hgnc_complete_df = pd.DataFrame(hgnc_complete_list)
  
  mega_table_list = [["sample_id", "true_gene", "top_n", "prompt", "gpt_version", "input_type", "iteration", "gpt_response_error", "completeness", "accuracy", "structural_compliance"]]
  for file in os.listdir(output_dir):
    error, c, a, f = None, None, None, None
    if file.endswith('.response') or file.endswith('.response.err'):
      logging.debug(file.split('__'))
      m = re.match(r'(.+?)\.(.+?).response*', file)
      sample_id, true_gene, top_n, prompt, gpt_version, input_type, iteration = m.group(1).split('__')
      true_gene = true_gene.upper()
      true_gene = true_gene.replace(" ", "")
      # special case. fix some bugs due to the unofficial gene name used in collecting data.
      if true_gene == 'R566X':
        true_gene = 'SCNN1B'
      if true_gene == 'NPR-C':
        true_gene = 'NPR3' 
      if (true_gene not in hgnc_complete_df['symbol'].values) and (true_gene not in hgnc_complete_df['other'].values):
        logging.error('true_gene: {} not in HGNC complete list'.format(true_gene))
        continue
      else:
        true_gene_symbol = hgnc_complete_df[hgnc_complete_df['other'] == true_gene]['symbol'].values[0]
        true_gene_alias = hgnc_complete_df[hgnc_complete_df['symbol'] == true_gene_symbol]['other'].values
          
      if file.endswith('.response'):
        error = 0
        gpt_response = get_gpt_response(os.path.join(output_dir,file))
        all_symbol_list = list(set(hgnc_complete_df['other'].values))
        c = evaluate_completeness(gpt_response, all_symbol_list, top_n)
        if c == 1:
          a = evaluate_accuracy(gpt_response, true_gene_alias)
        f = evaluate_fulfillment(gpt_response, top_n)
      else:
        error = 1     
    else:
      logging.error(file)    
    mega_table_list.append([sample_id, true_gene_symbol, top_n, prompt, gpt_version, input_type, iteration, error, c, a, f])
  mega_df = pd.DataFrame(mega_table_list)
  mega_df.to_csv(args.output_file, index=False, header=False) # change this to your output file name
