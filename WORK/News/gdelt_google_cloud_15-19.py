from google.cloud import bigquery
import json
import pandas as pd
from datetime import datetime, timedelta
import os

# Set up Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'C:\Users\20224781\Downloads\dblnew-f81055718ded.json'



def query_london():
    client = bigquery.Client(project='dblnew')
    query = """
    SELECT GlobalEventID, SQLDATE, MonthYear, Actor1Name, Actor2Name, Actor1CountryCode, Actor2CountryCode,
           EventCode, NumMentions, NumSources, NumArticles, AvgTone, SOURCEURL
    FROM `gdelt-bq.gdeltv2.events`
    WHERE (Actor1Name LIKE '%POLICE%' AND Actor2Name LIKE '%LONDON%' OR
           Actor1Name LIKE '%LONDON%' AND Actor2Name LIKE '%POLICE%')
          AND (Actor1CountryCode = 'GBR' OR Actor2CountryCode = 'GBR')
          AND SOURCEURL LIKE '%.uk%'
          AND SQLDATE BETWEEN 20150101 AND 20191231
    ORDER BY SQLDATE DESC;
    """

    query_job = client.query(query)
    results = query_job.result()

    articles = []
    for row in results:
        article = {
            'event_id': row['GlobalEventID'],
            'date': row['SQLDATE'],
            'actor1': row['Actor1Name'],
            'actor2': row['Actor2Name'],
            'event_code': row['EventCode'],
            'num_mentions': row['NumMentions'],
            'num_sources': row['NumSources'],
            'num_articles': row['NumArticles'],
            'avg_tone': row['AvgTone'],
            'source_url': row['SOURCEURL']
        }
        articles.append(article)
        print(f"Added article with ID: {row['GlobalEventID']}")

    print(f"Total articles collected: {len(articles)}")
    return articles

def categorize_event(url, categories):
    for category, keywords in categories.items():
        if any(keyword in url.lower() for keyword in keywords):
            return category
    return 'other'

def process_articles(articles):
    categories = {
        "protest": ['protest', 'rally', 'strike'],
        "terrorism": ['terrorism', 'terrorist', 'terror attack', 'cyberterrorism', 'civilian targets', 'police targeted'],
        "violence": ['violence', 'assault', 'attack', 'conflict'],
        "drugs": ['drug', 'narcotic', 'dealer'],
        "firearm": ['firearm', 'gun', 'shooting', 'weapon', 'rifle', 'shootout'],
        "illegal immigration": ['illegal immigration', 'human trafficking', 'visa overstay', 'unauthorized entry'],
        'theft': ['thief', 'hijacking', 'stolen', 'thieves', 'larceny', 'robbery', 'robber', 'burglary', 'shoplifting', 'pickpocketing', 'mugging', 'trespass']
    }

    df = pd.DataFrame(articles)
    df['Category'] = df['source_url'].apply(lambda x: categorize_event(x, categories))
    df['Date'] = pd.to_datetime(df['date'].astype(str), format='%Y%m%d')
    df['Week'] = df['Date'].apply(lambda x: x - timedelta(days=x.weekday()))

    results = []
    for category in categories:
        category_data = df[df['Category'] == category]
        weekly_data = category_data.groupby('Week').agg(
            num_articles=('event_id', 'count'),
            avg_sentiment=('avg_tone', 'mean'),
            num_mentions=('num_mentions', 'sum')
        ).reset_index()

        weekly_data['Category'] = category
        results.append(weekly_data)

    final_results = pd.concat(results)
    pivot_results = final_results.pivot_table(
        index='Week',
        columns='Category',
        values=['num_articles', 'avg_sentiment', 'num_mentions'],
        fill_value=0
    )

    return pivot_results

def save_articles_to_file(articles, filename):
    with open(filename, 'w') as file:
        json.dump(articles, file)
    print(f"Articles saved to {filename}")

if __name__ == "__main__":
    articles = query_london()
    save_articles_to_file(articles, 'articles.json')

    processed_df = process_articles(articles)
    processed_df.to_csv('15-19_data_weekly.csv')
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print(processed_df)

