# DNA Methylation Analysis Dataset

## Executive Summary
DNA methylation plays a vital role in the regulation of gene expression and is implicated in cancer progression. This dataset and analysis focus on comparing methylation profiles between non-invasive and invasive breast cancer subtypes, with the goal of identifying epigenetic markers for early detection and therapeutic intervention.

### Motivation
- Improve understanding of epigenetic changes driving the transition from non-invasive to invasive breast cancer.
- Aid in the development of diagnostic and prognostic tools for personalized cancer treatment.

### Potential Applications
- Biomarker discovery for early detection.
- Epigenetic therapeutic target identification.
- Advancement of precision oncology through methylation-based profiling.

---

## Description of Data
This dataset contains DNA methylation beta values (the ratio of methylated to unmethylated CpG sites) derived from patient samples categorized into two subsets:

Non-Progressing Subset:
File: non_progressing_subset.csv

Contains methylation beta values for CpG sites in samples classified as non-progressing (e.g., patients with non-invasive cases).
Includes metadata such as sample IDs, group labels.

Progressing Subset:
File: progressing_subset.csv

Contains methylation beta values for CpG sites in samples classified as progressing (e.g., patients with advancing conditions or invasive cases).

---

## Data Collection

The dataset was curated from the following sources:

NCBI DNA Methylation Database: Publicly available DNA methylation data was downloaded from the National Center for Biotechnology Information (NCBI).

Web Scraping Tool: A custom web scraping tool was developed to gather additional sample metadata from relevant online sources. The tool scraps patient information and maps the metadata back to the DNA methylation data, enabling a more comprehensive analysis.

The scripts for data scraping and mapping are included in this repository under the file webScrappingProcessing.py.

---

## Power Analysis
A power analysis was conducted to determine the minimum sample size required to detect significant methylation differences between groups:
- **Effect Size**: Medium (Cohen’s d = 0.5).
- **Significance Level (α)**: 0.05.
- **Power (1-β)**: 0.8.

The required sample size per group was calculated using the TTestIndPower module from statsmodels. 

Required sample size per group: 63.77

The results confirmed that the dataset size is sufficient to detect biologically meaningful differences in methylation levels with statistical confidence.

---

## Exploratory Data Analysis (EDA)

Exploratory data analysis revealed key insights into the methylation profiles:

the CpG sites associated with the genes PRAC2, TDRD10, and TMEM132C have been highlighted for their diagnostic and prognostic relevance in breast cancer. Specifically, the CpG sites cg12374721 (PRAC2), cg18081940 (TDRD10), and cg04475027 (TMEM132C) have shown promise as biomarkers.
Reference: https://rdcu.be/d1vq6

Statistical Comparison: Key CpG sites were analyzed, including cg12374721, cg18081940, and cg04475027.


For each CpG site, the mean and variance of methylation levels were calculated for progressing and non-progressing samples.

Box Plots:
The box plots below compare the methylation levels of progressing and non-progressing samples for significant CpG sites:


Comparison of cg12374721 between progressing and non-progressing samples
![Image Description](https://drive.google.com/uc?export=view&id=1Ropvx-1XLfDMqsBY6Q2jjR3rKuwkFU7s)


Comparison of cg18081940 between progressing and non-progressing samples
![Image Description](https://drive.google.com/uc?export=view&id=1A8buRelY2yVvd13-kTXDcgvN2ioEvnSY)

Comparison of cg04475027 between progressing and non-progressing samples
![Image Description](https://drive.google.com/uc?export=view&id=1S0tMThM3sVe8sLPpuK9RNNTnKJomlEqf)

Statistical Results:
Summary statistics and p-values for the differential methylation analysis are included in the file cpg_sites_statistical_results.csv.

| **CpG Site**   | **T-Statistic**       | **P-Value**            |
|----------------|-----------------------|------------------------|
| cg12374721     | -1.3929              | 0.1661                |
| cg18081940     | -1.6760              | 0.0962                |
| cg04475027     | -0.1902              | 0.8494                |

Observations:
CpG site cg18081940 shows the most promising difference between progressing and non-progressing groups, with a p-value close to the threshold for significance (p = 0.0962).
Other CpG sites (cg12374721 and cg04475027) did not show statistically significant differences at α = 0.05.

Code for EDA: The analysis code is included in the repository as eda.py.

---

## Data Sourcing Code
The data sourcing and processing code are publicly available in the following repository:
[\[**Public Data Sourcing Code Repository**\].](https://github.com/kz110AIPI/aipi510Project.git)

This repository contains:
- Scripts for raw data acquisition from public databases.
- Pipelines for data preprocessing, normalization, and feature extraction.

## Please run code with this order:

1. webScrappingProcessing.py
2. ncbiDataProcessing.py
3. dataMerging.py
4. subsetting.py
5. eda.py

---

## Ethics Statement
This project complies with strict ethical standards to ensure the responsible use of biomedical data:
- **Privacy**: All patient data is anonymized in accordance with HIPAA and GDPR requirements.
- **Consent**: Datasets originate from studies with proper informed consent protocols.
- **Bias Mitigation**: Efforts were made to ensure representation across diverse populations.
- **Research Integrity**: Findings are intended for academic research and not direct clinical application.

---

## License
This dataset and code are licensed under the **MIT License**. 

MIT License

Copyright (c) 2024 Kai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


---

