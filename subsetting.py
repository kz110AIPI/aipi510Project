import pandas as pd
#this is a program designed to create two subset datasets from meta dataset.
#one is progressing and the other one is non-progressing
def extract_progressing_and_non_progressing_chunks(input_file, progressing_file, non_progressing_file, n_samples=64, chunksize=10000):

    # Initialize empty lists to hold samples
    progressing_samples = []
    non_progressing_samples = []
    
    # Process the dataset in chunks
    for chunk in pd.read_csv(input_file, chunksize=chunksize):
        # Filter for progressing and non-progressing samples
        progressing_chunk = chunk[chunk['case_control'] == 'Progressor']
        non_progressing_chunk = chunk[chunk['case_control'] == 'Non-progressor']
        
        # Append samples to the respective lists
        progressing_samples.append(progressing_chunk)
        non_progressing_samples.append(non_progressing_chunk)
        
        # Check if we've reached the required number of samples
        if sum(len(df) for df in progressing_samples) >= n_samples and sum(len(df) for df in non_progressing_samples) >= n_samples:
            break

    # Concatenate collected chunks and take the first n_samples
    progressing = pd.concat(progressing_samples).head(n_samples)
    non_progressing = pd.concat(non_progressing_samples).head(n_samples)
    
    # Save subsets to respective files
    progressing.to_csv(progressing_file, index=False)
    non_progressing.to_csv(non_progressing_file, index=False)
    
    return progressing, non_progressing

# Example usage
progressing_df, non_progressing_df = extract_progressing_and_non_progressing_chunks(
    input_file='dcis_progressingDataset_kz.csv',
    progressing_file='progressing_subset.csv',
    non_progressing_file='non_progressing_subset.csv',
    n_samples=64,
    chunksize=20  
)
print("CSV files for progressing and non-progressing subsets created and saved.")
