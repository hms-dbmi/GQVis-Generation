#combine the single and follow up questions into one large dataset
import pandas as pd
import json
import sys

def combine_csv_files():
    df = pd.DataFrame()
    input_files = [
        #input files
    ]
    for file_path in input_files:
        df = pd.read_csv(file_path)
          
    output_path = 'combined_input.csv'
    df.to_csv(output_path, index=False)
    return combined_df


if __name__ == "__main__":
    combined_df = combine_csv_files()