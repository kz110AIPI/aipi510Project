
import requests
import gzip
import shutil
import os
import csv
import pandas as pd

def download_file(url, output_file):
    """Downloads a file from a URL."""
    try:
        print(f"Downloading {url} ...")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(output_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        print(f"Download completed: {output_file}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        raise

def unzip_file(gz_file, output_file):
    """Unzips a gzipped file."""
    try:
        with gzip.open(gz_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        print(f"Unzipped file: {output_file}")
    except Exception as e:
        print(f"Error unzipping file: {e}")
        raise

def txt_to_csv(txt_file, csv_file, delimiter=','):
    """Converts a txt file to csv."""
    try:
        with open(txt_file, 'r') as infile, open(csv_file, 'w', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=delimiter)
            for line in infile:
                row = line.strip().split(delimiter)  # Split based on delimiter
                writer.writerow(row)
        print(f"Converted {txt_file} to {csv_file}")
    except Exception as e:
        print(f"Error converting TXT to CSV: {e}")
        raise

def swap_rows_columns(input_csv, output_csv):
    """Swaps rows and columns of a dataset."""
    try:
        # Read the CSV into a Pandas DataFrame
        df = pd.read_csv(input_csv, sep="\t", header=None)

        
        # Transpose the DataFrame
        swapped_df = df.transpose()
        
        # Save the swapped DataFrame to a new CSV
        swapped_df.to_csv(output_csv, index=False, header=False)
        print(f"Swapped CSV saved to {output_csv}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    
    url = "https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE281307&format=file&file=GSE281307%5FDCISmethData%2Etxt%2Egz"
    gz_file = "GSE281307_DCISmethData.txt.gz"
    txt_file = "GSE281307_DCISmethData.txt"
    csv_file = "GSE281307_DCISmethData.csv"
    swapped_csv = "swapped_dataset.csv"

    # Step 1: Download the file
    download_file(url, gz_file)

    # Step 2: Unzip the downloaded file
    unzip_file(gz_file, txt_file)

    # Step 3: Convert TXT to CSV
    txt_to_csv(txt_file, csv_file, delimiter='	')

    # Step 4: Perform dataset transformation, swapping GSE281307_DCISmethData.csv into swapped_dataset.csv
    swap_rows_columns(csv_file, swapped_csv)

