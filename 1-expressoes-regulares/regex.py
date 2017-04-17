import re

patterns = {
  'num': r'[0-9]+', 
  'data': r'[0-3]?[0-9]/[0-1]?[0-9]/[0-9]{2,4}',
  'endereco': r'[rR]ua \w+, \d+',
  'telefone': r'(\(\d{2}\))?\s*\d?\s*\d{4}\s*-?\s*\d{4}'
}

text = raw_input()

while text:
    text = re.sub(patterns['data'], '_DATA_', text)
    text = re.sub(patterns['telefone'], '_TELEFONE_', text)
    text = re.sub(patterns['endereco'], '_ENDERECO_', text)
    text = re.sub(patterns['num'], '_NUM_', text)
    
    print(text)
    
    text = raw_input()