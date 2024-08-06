import pandas as pd
import os

def load_file_to_dataframe():
    file_name = input("Enter the name of the file with its extension (e.g., data.csv or data.xlsx): ")
    directory = input("Enter the directory path where the file is located: ")
    full_path = os.path.abspath(os.path.join('..', directory, file_name))
    
    # Extract the file extension
    _, extension = os.path.splitext(full_path)
    
    # Load the file based on its extension
    if extension.lower() == '.csv':
        df = pd.read_csv(full_path)
    elif extension.lower() in ['.xls', '.xlsx']:
        df = pd.read_excel(full_path)
    else:
        raise ValueError("Unsupported file extension. Only CSV and Excel (.xls, .xlsx) files are supported.")
    
    return df

def print_column_nan_info(df):
    nan_info = df.isna().mean() * 100  # Calculate the percentage of NaNs in each column
    for column, percentage in nan_info.items():
        print(f"Column '{column}': {percentage:.2f}% NaN values")

def select_columns(df):
    print("Available columns in the DataFrame:")
    print(list(df.columns))
    
    # Display options
    print("\nOptions:")
    print("1. Custom selection (Enter the columns you want to keep, separated by commas)")
    print("2. All columns ")
    print("3. Option 1: ('id', 'cl', 'si','sa', 'qr', 'sr','k')")
    print("4. Option 2: ('id', 'cl', 'si','sa', 'qr', 'sr','k','n', 'ro_d')")
    print("5. Option 3: ('id', 'cl', 'si','sa', 'qr', 'sr','k','n', 'ro_d', 'lam_s')")

    selection = input("\nSelect an option (1, 2, 3, 4, 5): ")

    if selection == 'all':
        selected_columns = list(df.columns)
    elif selection == '1':
        selected_columns = input("Enter the columns you want to keep, separated by commas: ").split(',')
        selected_columns = [col.strip() for col in selected_columns]  # Remove any extra spaces
    elif selection == '2':
        selected_columns = list(df.columns)
    elif selection == '3':
        selected_columns = ['id', 'cl', 'si','sa', 'qr', 'sr','k']  # Replace with your custom columns
    elif selection == '4':
        selected_columns = ['id', 'cl', 'si','sa', 'qr', 'sr','k','n', 'ro_d']  # Replace with your custom columns
    elif selection == '5':
        selected_columns = ['id', 'cl', 'si','sa', 'qr', 'sr','k','n', 'ro_d', 'lam_s']  # Replace with your custom columns
    else:
        raise ValueError("Invalid selection. Please choose a valid option.")
    
    if not all(col in df.columns for col in selected_columns):
        raise ValueError("One or more selected columns do not exist in the DataFrame.")
    
    df = df[selected_columns]
    return df

def save_dataframe(df):
    save_format = input("In which format would you like to save the file? (csv/xlsx): ").lower()
    file_name = input("Enter the name of the file to save (without extension): ")
    save_directory = input("Enter the directory where you want to save the file (relative to the parent directory): ")

    # Construct the full path for saving the file
    full_save_path = os.path.abspath(os.path.join('..', save_directory, f"{file_name}.{save_format}"))
    
    if save_format == 'csv':
        df.to_csv(full_save_path, index=False)
        print(f"DataFrame saved as {full_save_path}")
    elif save_format == 'xlsx':
        df.to_excel(full_save_path, index=False)
        print(f"DataFrame saved as {full_save_path}")
    else:
        print("Unsupported file format. Please choose either 'csv' or 'xlsx'.")

def vectorize_data(df):
    # Group by 'id' and aggregate 'k' and 'sr' into lists
    vectorized_df = df.groupby('id').agg({
        'k': lambda x: list(x),
        'sr': lambda x: list(x),
        **{col: 'first' for col in df.columns if col not in ['id', 'k', 'sr']}
    }).reset_index()
    
    return vectorized_df

# Main function to execute the script
def main():
    try:
        df = load_file_to_dataframe()
        print_column_nan_info(df)
        df = select_columns(df)
        save_dataframe(df)
        
        vectorize = input("Would you like to vectorize the data? (yes/no): ").strip().lower()
        if vectorize == 'yes':
            df = vectorize_data(df)
            save_dataframe(df)
            print("Data has been vectorized and saved.")
        else:
            print("Data has not been vectorized.")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()