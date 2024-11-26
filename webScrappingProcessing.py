import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# URL of the main page with all sample information
main_page_url = "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE281307"

# Function to extract sample links from the main page
def get_sample_links(main_page_url):
    response = requests.get(main_page_url)
    if response.status_code != 200:
        print("Failed to fetch the main page")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    sample_links = []
    for link in soup.find_all("a", href=True):
        if "GSM" in link.text:
            sample_links.append({
                "sample_id": link.text.strip(),
                "url": "https://www.ncbi.nlm.nih.gov" + link["href"]
            })
    return sample_links

# Function to extract sample data
def extract_sample_data(sample_link):
    sample_url = sample_link["url"]
    response = requests.get(sample_url)
    if response.status_code != 200:
        print(f"Failed to fetch sample page: {sample_link['sample_id']}")
        return {"id_ref": "N/A", "case_control": "N/A"}

    soup = BeautifulSoup(response.text, "html.parser")
    title_tag = soup.find("td", string="Title")
    sample_id = title_tag.find_next_sibling("td").text.strip() if title_tag else "N/A"

    characteristics_section = soup.find("td", string="Characteristics")
    case_control = "N/A"
    if characteristics_section and characteristics_section.find_next_sibling("td"):
        characteristics_text = characteristics_section.find_next_sibling("td").get_text(separator="|", strip=True)
        for line in characteristics_text.split("|"):
            if "case_control:" in line:
                case_control = line.split(":", 1)[1].strip()
                break

    return {"id_ref": sample_id, "case_control": case_control}

# Function to update CSV file with mapped values
def update_csv_file(input_file, output_file):
    mapping = {"Case": "Progressor", "Control": "Non-progressor", "Normal": "Benign"}
    df = pd.read_csv(input_file)
    df['case_control'] = df['case_control'].map(mapping)
    df.to_csv(output_file, index=False)

# Main workflow
def main():
    print("Fetching sample links...")
    sample_links = get_sample_links(main_page_url)

    print(f"Found {len(sample_links)} samples. Extracting data...")
    sample_data = []
    for i, sample_link in enumerate(sample_links, 1):
        print(f"Processing {i}/{len(sample_links)}: {sample_link['sample_id']}")
        sample_data.append(extract_sample_data(sample_link))
        time.sleep(0.5)

    input_file = "samples_case_control.csv"
    output_file = "updated_samples_case_control.csv"
    pd.DataFrame(sample_data).to_csv(input_file, index=False)
    print(f"CSV file created: {input_file}")

    print("Updating CSV with mapped values...")
    update_csv_file(input_file, output_file)
    print(f"Updated CSV file created: {output_file}")

if __name__ == "__main__":
    main()
