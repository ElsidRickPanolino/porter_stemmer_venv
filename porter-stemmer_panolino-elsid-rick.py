
import pandas as pd
import os
from functions import stemPhrase

data = pd.read_csv('4-cols_15k-rows.csv')
output_file = 'stemmed-dataset_15k-rows_Panolino-ElsidRick.csv'


data = data.apply(stemPhrase, axis=1)

if os.path.exists(output_file):
    os.remove(output_file)
    print(f"Deleted existing {output_file}")
    
data.to_csv(output_file, index=False, encoding='utf-8')
print("done")



    




    
     
