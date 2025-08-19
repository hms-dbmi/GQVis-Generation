#!/usr/bin/env python3
"""
Combine multiple CSV data sources into one large dataset.
This simplifies the downstream processing by having all query templates in one place.
"""

import pandas as pd
import json
import sys

def combine_csv_files():
    """Combine multistepinput.csv and newinput.csv into one large combined_input.csv file."""
    combined_df = pd.DataFrame()
    
    # List of input files to combine
    input_files = [
        'newinput.csv',
        'newoutput.csv',
    ]
    
    for file_path in input_files:
        try:
            df = pd.read_csv(file_path)
            print(f"Loaded {len(df)} records from {file_path}")
            
            # Add source column to track where data came from
                        
        except FileNotFoundError:
            print(f"Warning: {file_path} not found, skipping...")
        except Exception as e:
            print(f"Error loading {file_path}: {str(e)}")
    
    if not combined_df.empty:
        
        
        # Save combined dataset
        output_path = 'combined_input.csv'
        combined_df.to_csv(output_path, index=False)
        print(f"Combined dataset saved to {output_path}")
        
        # Print summary statistics
        print(f"\nSUMMARY:")
        print(f"Total records: {len(combined_df)}")
        
        if 'query_template' in combined_df.columns:
            unique_templates = combined_df['query_template'].nunique()
            print(f"Unique query templates: {unique_templates}")
            
            
        return combined_df
    else:
        print("No data found to combine!")
        return pd.DataFrame()

def main():
    """Main function to combine data sources."""
    print("=== COMBINING DATA SOURCES ===")
    combined_df = combine_csv_files()
    
    if not combined_df.empty:
        print("Data combination completed successfully!")
    else:
        print("No data to combine.")
        sys.exit(1)

if __name__ == "__main__":
    main()
