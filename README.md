# CompStak Coverage Analysis

**Author:** William Clinton Co  
**Affiliation:** Department of Economics, University of British Columbia  
**Date:** April 2025

## Overview

This project evaluates the **CompStak** commercial property dataset to assess its coverage, classification consistency, and geographic representativeness across the United States. By benchmarking CompStak against the **DOE Commercial Building Inventory** (sourced from CoStar), we quantify how much of the U.S. commercial property market CompStak captures and identify systematic biases in that coverage.

### Key Findings

- **~35% national coverage** of U.S. commercial properties (using DOE as the benchmark total)
- **Property Type** fields are well-populated (95-99% fill rate), but **Property Subtype** has up to 28% missing values
- Property IDs are stable across time, with classification inconsistencies in <0.02% of 759,623 unique properties
- Coverage is **non-uniform**: strong western/West Coast bias (California reaches ~70% coverage vs. ~35% national average)
- **Increasing returns to scale**: states with more commercial properties tend to have higher coverage rates, suggesting fixed costs in data collection
- Industrial, office, and retail sectors are well-represented; land and multi-family are significantly undercovered

## Project Structure

```
compstak-analysis/
├── Data/
│   ├── compstak.csv              # CompStak property data (Property Type, Subtype, ID, State)
│   ├── compstak_mapped.csv       # CompStak data with standardized category mappings
│   ├── DOE.csv                   # DOE Commercial Building Inventory (statecode, property type/subtype)
│   ├── DOE_mapped.csv            # DOE data with standardized category mappings
│   └── data_dictionary.csv       # CompStak field definitions (standard & premium feeds)
├── src/
│   ├── exploration_1.ipynb                        # Initial field review and column profiling
│   ├── exploration_2-5_(industry_category_study)  # Industry classification deep-dives
│   ├── exploration_6-9_(geography/industry_study) # Geographic coverage and state-level analysis
│   ├── DOE_data_analysis.ipynb                    # DOE dataset loading and initial comparison
│   ├── DOE_data_analysis_1-11.ipynb               # Iterative DOE-CompStak mapping and coverage analysis
│   ├── DOE_Exploration_data_analysis_1.ipynb      # DOE exploratory data analysis
│   ├── dataset_creator.ipynb                      # Dataset preparation pipeline
│   ├── dataset_creator_2-6.ipynb                  # Iterative dataset construction and refinement
│   ├── summarize_compstak.py                      # Property subtype summarization and geographic coverage plots
│   └── app.py                                     # Streamlit field definitions viewer prototype
├── Images/                       # Visualizations from initial analysis
│   └── Corrected Data/           # Revised visualizations after DOE mapping corrections
├── Sunburst/                     # Sunburst charts (regular and standard/premium breakdown)
├── article/                      # Quarto article template (article.qmd)
├── jasa/                         # JASA journal template for formal write-up
├── jasa 1/                       # JASA template (alternate version)
├── Comsptak Progress (1).pdf     # Part 1 progress report
├── Compstak Progress Part 2 (1).pdf  # Part 2 progress report (standalone)
└── Notes.txt                     # Working notes on category mapping decisions
```

## Methodology

### 1. Field Review & Data Quality

Each CompStak field was individually reviewed. The analysis focuses on **Property Type** (8 categories) and **Property Subtype** (56 categories), as NAICS/SIC codes are premium add-ons not available in our data. Key quality metrics:

| Dataset | Field | Fill Rate | Unique Values |
|---------|-------|-----------|---------------|
| Sales | Property Type | 95% | 8 |
| Leases | Property Type | 99% | 8 |
| Sales | Property Subtype | 75% | 56 |
| Leases | Property Subtype | 66% | 56 |

### 2. Category Mapping (CompStak to DOE)

The DOE dataset has 11 property types while CompStak has 8. To enable comparison, both datasets were mapped to **6 standardized categories**: Hotel, Industrial, Multi-Family, Office, Other, Retail.

The mapping uses a two-step approach:

- **Direct mapping** for categories with the same name across datasets (e.g., Industrial, Office, Retail)
- **Subtype-based mapping** for ambiguous DOE categories (Flex, Health Care, Specialty, Sports & Entertainment, Unknown) where the subcategory determines the standardized assignment

CompStak's "Land" and "Mixed-Use" types were similarly resolved using their subtypes. Entries with no category or NaN values default to "Other", which introduces overestimation bias for that category.

### 3. Coverage Analysis

Coverage rate is defined as:

> **Coverage Rate** = (CompStak property count) / (DOE property count)

This is computed at national, state, and category levels to identify geographic and sectoral biases.

## Data Sources

| Source | Description |
|--------|-------------|
| **CompStak** | Commercial lease and sales comp data (property-level) from CompStak via UBC academic license |
| **DOE Commercial Building Inventory** | U.S. Department of Energy estimates of commercial building counts by state and property type (sourced from CoStar) |
| **CoStar Glossary** | Reference for DOE/CoStar category definitions used in mapping |

## Tools & Dependencies

- **Python**: pandas, numpy, geopandas, matplotlib, plotly
- **Streamlit**: Interactive field viewer prototype (`src/app.py`)
- **Quarto + LaTeX**: Academic write-up (`article/`, `jasa/`)
- **Jupyter Notebooks**: All analysis conducted in iterative notebook workflows

## Progress Reports

The two PDF reports document the analysis in detail:

1. **Part 1** — Initial field review, property ID consistency checks, coverage estimation using unverified internet-sourced U.S. property counts, state-level coverage analysis, and identification of increasing returns to scale in data collection
2. **Part 2** (standalone) — Introduces the DOE dataset as a verified benchmark, details the two-step category mapping methodology, produces coverage rates by category and state, and documents western/size bias with heatmap visualizations
