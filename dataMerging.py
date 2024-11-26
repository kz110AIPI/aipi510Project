import pandas as pd
import os

# Define file paths
main_dataset_file = 'swapped_dataset.csv'
case_control_mapping_file = 'updated_samples_case_control.csv'
merged_output_file = 'dcis_progressingDataset_kz.csv'
progressing_file = 'progressing_subset.csv'
non_progressing_file = 'non_progressing_subset.csv'

# Define the CpG sites of interest
cpg_sites = ['id_ref', 'cg12374721', 'cg18081940', 'cg04475027']

# Load the case control mapping file
case_control_mapping = pd.read_csv(case_control_mapping_file)

# Normalize column names and values
case_control_mapping.columns = case_control_mapping.columns.str.lower()
case_control_mapping['id_ref'] = case_control_mapping['id_ref'].str.strip().str.lower()

# Create a dictionary for quick mapping
mapping_dict = dict(zip(case_control_mapping['id_ref'], case_control_mapping['case_control']))
if not mapping_dict:
    raise ValueError("Mapping dictionary is empty. Check if the 'id_ref' column matches between files.")

# Remove the merged output file if it exists
if os.path.exists(merged_output_file):
    os.remove(merged_output_file)
    print(f"Removed existing file: {merged_output_file}")

# Processing Parameters
chunk_size = 20  # Adjust based on memory and dataset size
print(f"Processing the main dataset in chunks of {chunk_size} rows...")

# Initialize flag to track the first chunk
is_first_chunk = True

# Process dataset in chunks
with open(merged_output_file, 'a') as f:
    for i, chunk in enumerate(pd.read_csv(main_dataset_file, chunksize=chunk_size, low_memory=True)):
        print(f"Processing chunk {i + 1} with {len(chunk)} rows...")

        # Normalize `id_ref` and filter CpG sites
        chunk.columns = chunk.columns.str.lower()
        chunk['id_ref'] = chunk['id_ref'].str.strip().str.lower()
        filtered_chunk = chunk.loc[:, chunk.columns.isin(cpg_sites)].copy()

        # Map `case_control` directly to a new column
        filtered_chunk.loc[:, 'case_control'] = (
            filtered_chunk['id_ref']
            .str.split('.detectionpval')
            .str[0]
            .map(mapping_dict)
            .fillna('Unknown')
        )

        # Write processed data to the output file
        filtered_chunk.to_csv(f, index=False, mode='a', header=is_first_chunk)
        is_first_chunk = False

        # Clear chunk from memory
        del chunk

        print(f"Chunk {i + 1} processed and saved.")

print(f"Updated dataset with CpG sites saved as '{merged_output_file}'")

# Subsetting Function
def extract_progressing_and_non_progressing(input_file, progressing_file, non_progressing_file, n_samples=64, chunksize=10000):
    """
    Extract subsets for progressing and non-progressing cases.
    """
    progressing_samples = []
    non_progressing_samples = []
    
    for chunk in pd.read_csv(input_file, chunksize=chunksize):
        progressing_samples.append(chunk[chunk['case_control'] == 'Progressor'])
        non_progressing_samples.append(chunk[chunk['case_control'] == 'Non-progressor'])
        
        if sum(len(df) for df in progressing_samples) >= n_samples and sum(len(df) for df in non_progressing_samples) >= n_samples:
            break

    progressing = pd.concat(progressing_samples).head(n_samples)
    non_progressing = pd.concat(non_progressing_samples).head(n_samples)
    
    progressing.to_csv(progressing_file, index=False)
    non_progressing.to_csv(non_progressing_file, index=False)

    print(f"Progressing and non-progressing subsets saved: {progressing_file}, {non_progressing_file}")

# Perform subsetting
extract_progressing_and_non_progressing(merged_output_file, progressing_file, non_progressing_file, n_samples=64, chunksize=20)
