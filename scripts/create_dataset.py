import pandas as pd
import os
import numpy as np

def get_file_info():
    num_files = int(input("How many files do you want to load? "))
    file_paths = []
    for i in range(num_files):
        file_name = input(f"Enter the name of file {i+1} with its extension: ")
        directory = input(f"Enter the directory path where file {i+1} is located: ")
        full_path = os.path.abspath(os.path.join('..', directory, file_name))
        file_paths.append(full_path)
    
    return file_paths

def load_file_to_dataframe(file_path):
    # Extract the file extension
    _, extension = os.path.splitext(file_path)

    # Load the file based on its extension
    if extension.lower() == '.csv':
        df = pd.read_csv(file_path)
    elif extension.lower() in ['.xls', '.xlsx']:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file extension. Only CSV and Excel (.xls, .xlsx) files are supported.")
    
    # Assert that the loaded object is indeed a DataFrame
    assert isinstance(df, pd.DataFrame), "The loaded data is not a DataFrame."
    
    # Assert that the DataFrame is not empty
    assert not df.empty, "The DataFrame is empty."

    return df

def remove_rows_with_empty_id(dataframes):
    # Remove rows where 'id' column is NaN
    cleaned_dataframes = []
    for df in dataframes:
        if 'id' in df.columns:
            df = df.dropna(subset=['id'])
        cleaned_dataframes.append(df)
    return cleaned_dataframes

def merge_dataframes_with_continuous_id(dataframes):
    # Find the set of all columns across all DataFrames
    all_columns = set(col for df in dataframes for col in df.columns)
    
    # Reindex each DataFrame to include all columns, filling missing columns with NaN
    reindexed_dfs = []
    for df in dataframes:
        reindexed_df = df.reindex(columns=all_columns)
        reindexed_dfs.append(reindexed_df)
    
    # Adjust the 'id' column to maintain continuity across all DataFrames
    max_id = 0
    for i, df in enumerate(reindexed_dfs):
        if 'id' in df.columns:
            df['id'] = df['id'].astype(float).fillna(0).astype(int)  # Ensure 'id' is an integer and fill NaN with 0
            df['id'] += max_id  # Increase current 'id' values by the maximum 'id' from the previous DataFrame
            max_id = df['id'].max()  # Update the maximum 'id' for the next DataFrame

    # Concatenate all DataFrames into one
    merged_df = pd.concat(reindexed_dfs, ignore_index=True)
    
    return merged_df

def save_dataframe(df):
    save_format = input("In which format would you like to save the file? (csv/xlsx): ").lower()
    file_name = input("Enter the name of the file to save (without extension): ")
    
    if save_format == 'csv':
        file_path = f"{file_name}.csv"
        df.to_csv(file_path, index=False)
        print(f"DataFrame saved as {file_path}")
    elif save_format == 'xlsx':
        file_path = f"{file_name}.xlsx"
        df.to_excel(file_path, index=False)
        print(f"DataFrame saved as {file_path}")
    else:
        print("Unsupported file format. Please choose either 'csv' or 'xlsx'.")

# Example usage
file_paths = get_file_info()
try:
    dataframes = [load_file_to_dataframe(file_path) for file_path in file_paths]
    
    # Remove rows with empty 'id'
    cleaned_dataframes = remove_rows_with_empty_id(dataframes)
    
    if len(cleaned_dataframes) > 1:
        merged_dataframe = merge_dataframes_with_continuous_id(cleaned_dataframes)
        print("The files have been successfully merged with continuous 'id' values.")
        print(merged_dataframe.head())  # Display the first few rows of the merged DataFrame
        save_dataframe(merged_dataframe)  # Save the merged DataFrame
    else:
        print("Only one file was loaded:")
        print(cleaned_dataframes[0].head())
        save_dataframe(cleaned_dataframes[0])  # Save the single DataFrame
except Exception as e:
    print(f"Error: {e}")