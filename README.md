# DataChallenge2-Group17

YouTube Data Analysis (youtube.py)

The youtube.py script leverages the YouTube API to analyze public sentiment regarding the London Metropolitan Police. It collects videos based on specific keywords related to policing in London, extracting key metrics like view counts, likes, and the number of comments to gauge public engagement.

Key Features:

Sentiment Analysis: Utilizes TextBlob to analyze the sentiment of comments, classifying them into positive, negative, or neutral categories.

Categorical Analysis: Sorts comments into predefined themes (similar to those used for news analysis) such as violence, policy changes, and police-community interactions.

Engagement Metrics: Analyzes engagement through likes, views, and comment counts to assess the public’s reaction to the content.

How to Use:

API Key Configuration: Ensure you have a valid YouTube API key configured in the script.

Run the Script: Execute the script to start collecting and analyzing data. The results will provide insights into public sentiment and help identify trends over time.
######
borough_coordinates_list.py : Processes geographical data for London's boroughs to compute and convert bounding box coordinates from the UK National Grid to WGS84 format. The geographical data is obtained from the london datasore under the name ''London Boroughs'' The output is saved as a CSV file containing latitude and longitude information for each borough.

How to use: Ensure the London_Boroughs.gpkg file is available at the specified path.
Run the script to generate lat-long_new.csv.

######

demographics_correlation.py : This script reads demographic data from a CSV file, aggregates the data by borough, and calculates the correlation matrix between boroughs based on numeric features. It also generates a heatmap of the correlation matrix and saves it as an image.

How to use:Ensure the demographic data CSV file is available at the specified path.
Run the script to generate borough_correlation_matrix.csv and borough_correlation_matrix.png.


######

gdelt_google_cloud_15-19.py : This script queries the GDELT database using Google BigQuery to collect articles related to events involving the police and London. Google Biqquery has limitied free credits hence, it should be run carefully.It processes the articles to categorize them by event type and aggregates the data weekly. The results are saved as CSV files.

How to use: Set up Google Cloud credentials and ensure the JSON key file is available at the specified path.
Run the script to generate articles.json and 15-19_data_weekly.csv.

######

article_per_borough.py : This script is similar to gdelt_google_cloud_15-19.py but focuses on querying and processing articles specific to each borough given their coordinates.For this project each borough's coordinates were written manually hence, the code is just an example of one borough. It categorizes events and aggregates the data weekly, saving the results as a CSV file.

How to use: Set up Google Cloud credentials and ensure the JSON key file is available at the specified path.
Run the script to generate Barking_and_Dagenham_weekly.csv.

