import pandas as pd
import os
from functions import stemPhrase

# Read the input CSV file
input_file = '4-cols_15k-rows.csv'
data = pd.read_csv(input_file)

# stem each column of a row

# columns:
# instruction,context,response,category

def stem_and_concatenate(row):
    stemmed_instruction = stemPhrase(row['instruction'])
    stemmed_context = stemPhrase(row['context'])
    stemmed_response = stemPhrase(row['response'])
    stemmed_category = stemPhrase(row['category'])

    
    return pd.Series([stemmed_instruction, stemmed_context, stemmed_response, row['category']])

# iterate to each row and apply the stemming function above
data = data.apply(stem_and_concatenate, axis=1)

# applying the changes into new csv
data.columns = ['instruction', 'context', 'response', 'category']
output_file = 'stemmed-dataset_15k-rows_Panolino-ElsidRick.csv'
# expected_output_file = 'stemmed-dataset_15k-rows_tilaon-antonin.csv'

# delete file if existing
if os.path.exists(output_file):
    os.remove(output_file)
    print(f"Deleted existing {output_file}")


data.to_csv(output_file, index=False, encoding='utf-8')
print("done")


#print datasets
# output_file = 'stemmed-dataset_15k-rows_Panolino-ElsidRick.csv'
# output_data = pd.read_csv(output_file)
# print(output_data)

# expected_output_file = 'stemmed-dataset_15k-rows_tilaon-antonin.csv'
# expected_output_data = data = pd.read_csv(expected_output_file)
# print(expected_output_data)
