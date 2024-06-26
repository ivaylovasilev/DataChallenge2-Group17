# Data Challenge 2 - Group 17

## Overview
This repository contains scripts developed by Group 17 for analyzing various aspects of public sentiment and demographic correlations in relation to the London Metropolitan Police. The analyses cover YouTube comments, geographical data processing, demographic correlations, and news article analysis using the GDELT database.

## Scripts Description

### YouTube Data Analysis (`youtube.py`)
**Description:** Analyzes public sentiment regarding the London Metropolitan Police using the YouTube API. It collects videos based on specific keywords and extracts metrics like view counts, likes, and comments.

**Key Features:**
- **Sentiment Analysis:** Utilizes TextBlob to classify the sentiment of comments into positive, negative, or neutral categories.
- **Categorical Analysis:** Sorts comments into predefined themes such as violence, policy changes, and police-community interactions.
- **Engagement Metrics:** Measures public engagement through likes, views, and comment counts.

**Usage:**
1. Configure your YouTube API key in the script.
2. Run the script to collect and analyze data, which will help identify public sentiment trends over time.

### Borough Coordinates List (`borough_coordinates_list.py`)
**Description:** Processes geographical data for London's boroughs, converting UK National Grid coordinates to WGS84 format.

**Usage:**
1. Ensure the `London_Boroughs.gpkg` file is accessible.
2. Run the script to generate `lat-long_new.csv` containing latitude and longitude information for each borough.

### Demographics Correlation Analysis (`demographics_correlation.py`)
**Description:** Reads demographic data, aggregates it by borough, and calculates correlation matrices. Also generates a heatmap of these correlations.

**Usage:**
1. Ensure the demographic data CSV file is accessible.
2. Run the script to generate `borough_correlation_matrix.csv` and `borough_correlation_matrix.png`.

### GDELT Article Processing for 2015-2019 (`gdelt_google_cloud_15-19.py`)
**Description:** Queries the GDELT database to collect and categorize news articles related to the London police from 2015 to 2019.

**Usage:**
1. Set up Google Cloud credentials and ensure the JSON key file is accessible.
2. Run the script carefully due to potential costs associated with Google BigQuery. Generates `articles.json` and `15-19_data_weekly.csv`.

### Article Processing Per Borough (`article_per_borough.py`)
**Description:** Focuses on querying and processing articles for each borough based on manually specified coordinates.

**Usage:**
1. Set up Google Cloud credentials and ensure the JSON key file is accessible.
2. Run the script to generate `Barking_and_Dagenham_weekly.csv` for the specified borough.

## Additional Information
- Ensure you have the necessary permissions and access rights to use the data and APIs required by these scripts.
- Each script's dependencies are listed at the top of the file, and it is assumed that the user has an appropriate Python environment set up to run the scripts.

## FILE SPECIFICATION:
Main:
- DataMerging: Merging of News and YouTube datasets (according to date)
- DemographicsNotebook: Creating the file containing all useful and interpolated demographic variables
- RunningRegression: Running of (nearly) all models used
- PresentingData: used to format parts of Granular PAS Dataset, particulary convert encoded date
- Untitled: Used to determine Restorative Justice + Bodycam conclusion, as well as Q62C's predictive power of other questions

Supplementary:
- Hierarchical: Evaluation of Hierarchical Time Series Model from Google BigCloud
- GranularData: Exploratory Analysis

## SUPPLEMENTARY DATASETS USED:
Demographic datasets obtained from:
- 2021 London Census: https://www.nomisweb.co.uk/sources/census_2021_bulk
- 2011 London Census: https://data.london.gov.uk/census/2021-ward-and-lsoa-estimates/

- The following tables were used: 004, 006, 009, 015, 019, 021, 029, 030, 044, 051, 059, 063, 065, 066, 067, 068, 077

**Usage:**
1. Download the tables from the 2021 Census and place them in a folder named 'CensusCSV' in the same directory as the 'Demographics Notebook'
2. Do the same for the 2011 Census, but name the folder 'Census2011' instead 
