from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
from datetime import datetime
from textblob import TextBlob

# Load sentiment analysis model
# sentiment_pipeline = pipeline("sentiment-analysis")

borough_keywords = {
    'Westminster': ['Westminster', 'Paddington', 'Maida Vale', 'Bayswater', 'Soho', 'Covent Garden', 'Hyde Park', 'Marylebone', 'Mayfair', 'St James\'s', 'St John\'s Wood', 'Victoria', 'West End', 'Westbourne Green'],
    'Camden': ['Camden', 'Bloomsbury', 'Euston', 'Hampstead', 'Holborn', 'Kentish Town', 'King\'s Cross', 'Regent\'s Park', 'Somers Town', 'Swiss Cottage', 'West Hampstead'],
    'Islington': ['Islington', 'Angel', 'Archway', 'Barnsbury', 'Canonbury', 'Clerkenwell', 'Farringdon', 'Finsbury', 'Highbury', 'Holloway', 'Tufnell Park'],
    'Hackney': ['Hackney', 'Dalston', 'Hoxton', 'Shoreditch', 'Stamford Hill', 'Homerton', 'Hackney Wick', 'Clapton'],
    'Tower Hamlets': ['Tower Hamlets', 'Bethnal Green', 'Bow', 'Canary Wharf', 'Limehouse', 'Mile End', 'Poplar', 'Stepney', 'Whitechapel'],
    'Greenwich': ['Greenwich', 'Abbey Wood', 'Blackheath', 'Charlton', 'Eltham', 'Kidbrooke', 'Plumstead', 'Woolwich'],
    'Lewisham': ['Lewisham', 'Blackheath', 'Brockley', 'Catford', 'Deptford', 'Forest Hill', 'Hither Green', 'New Cross', 'Sydenham'],
    'Southwark': ['Southwark', 'Bermondsey', 'Camberwell', 'Dulwich', 'Elephant and Castle', 'Peckham', 'Rotherhithe', 'Surrey Quays', 'Walworth'],
    'Lambeth': ['Lambeth', 'Brixton', 'Clapham', 'Kennington', 'Stockwell', 'Streatham', 'Vauxhall', 'West Norwood'],
    'Wandsworth': ['Wandsworth', 'Balham', 'Battersea', 'Earlsfield', 'Furzedown', 'Putney', 'Roehampton', 'Southfields', 'Tooting', 'Wandsworth Common'],
    'Hammersmith and Fulham': ['Hammersmith', 'Fulham', 'Barons Court', 'West Kensington', 'Shepherd\'s Bush', 'White City'],
    'Kensington and Chelsea': ['Kensington', 'Chelsea', 'Earls Court', 'Holland Park', 'North Kensington', 'Notting Hill', 'South Kensington'],
    'Haringey': ['Haringey', 'Crouch End', 'Finsbury Park', 'Highgate', 'Hornsey', 'Muswell Hill', 'Seven Sisters', 'Tottenham', 'Wood Green'],
    'Enfield': ['Enfield', 'Edmonton', 'Enfield Town', 'Palmers Green', 'Southgate', 'Winchmore Hill'],
    'Barnet': ['Barnet', 'Chipping Barnet', 'Edgware', 'Finchley', 'Golders Green', 'Hendon', 'Mill Hill'],
    'Harrow': ['Harrow', 'Harrow on the Hill', 'Pinner', 'Stanmore', 'Wealdstone'],
    'Brent': ['Brent', 'Kilburn', 'Wembley', 'Neasden', 'Harlesden', 'Kingsbury'],
    'Ealing': ['Ealing', 'Acton', 'Greenford', 'Hanwell', 'Northolt', 'Southall'],
    'Hillingdon': ['Hillingdon', 'Hayes', 'Ruislip', 'Uxbridge', 'Yiewsley'],
    'Hounslow': ['Hounslow', 'Brentford', 'Chiswick', 'Feltham', 'Isleworth'],
    'Richmond upon Thames': ['Richmond', 'Twickenham', 'Teddington', 'Barnes', 'Hampton', 'Kew'],
    'Kingston upon Thames': ['Kingston', 'Chessington', 'New Malden', 'Surbiton'],
    'Merton': ['Merton', 'Mitcham', 'Morden', 'Wimbledon'],
    'Sutton': ['Sutton', 'Cheam', 'Worcester Park', 'Carshalton', 'Wallington'],
    'Croydon': ['Croydon', 'Addiscombe', 'Purley', 'South Norwood', 'Thornton Heath'],
    'Bromley': ['Bromley', 'Beckenham', 'Orpington', 'Penge', 'West Wickham'],
    'Bexley': ['Bexley', 'Crayford', 'Erith', 'Sidcup', 'Welling'],
    'Havering': ['Havering', 'Romford', 'Hornchurch', 'Upminster', 'Rainham'],
    'Redbridge': ['Redbridge', 'Ilford', 'Wanstead', 'Woodford'],
    'Newham': ['Newham', 'East Ham', 'Forest Gate', 'Plaistow', 'Stratford', 'Upton Park'],
    'Waltham Forest': ['Waltham Forest', 'Chingford', 'Leyton', 'Walthamstow'],
    'Barking and Dagenham': ['Barking', 'Dagenham']
}

boroughs = {
    'Westminster': ['Westminster', 'Paddington', 'Maida Vale', 'Bayswater', 'Soho', 'Covent Garden', 'Hyde Park', 'Marylebone', 'Mayfair', 'St James\'s', 'St John\'s Wood', 'Victoria', 'West End', 'Westbourne Green'],
    'Camden': ['Camden', 'Bloomsbury', 'Euston', 'Hampstead', 'Holborn', 'Kentish Town', 'King\'s Cross', 'Regent\'s Park', 'Somers Town', 'Swiss Cottage', 'West Hampstead'],
    'Islington': ['Islington', 'Angel', 'Archway', 'Barnsbury', 'Canonbury', 'Clerkenwell', 'Farringdon', 'Finsbury', 'Highbury', 'Holloway', 'Tufnell Park'],
    'Hackney': ['Hackney', 'Dalston', 'Hoxton', 'Shoreditch', 'Stamford Hill', 'Homerton', 'Hackney Wick', 'Clapton'],
    'Tower Hamlets': ['Tower Hamlets', 'Bethnal Green', 'Bow', 'Canary Wharf', 'Limehouse', 'Mile End', 'Poplar', 'Stepney', 'Whitechapel'],
    'Greenwich': ['Greenwich', 'Abbey Wood', 'Blackheath', 'Charlton', 'Eltham', 'Kidbrooke', 'Plumstead', 'Woolwich'],
    'Lewisham': ['Lewisham', 'Blackheath', 'Brockley', 'Catford', 'Deptford', 'Forest Hill', 'Hither Green', 'New Cross', 'Sydenham'],
    'Southwark': ['Southwark', 'Bermondsey', 'Camberwell', 'Dulwich', 'Elephant and Castle', 'Peckham', 'Rotherhithe', 'Surrey Quays', 'Walworth'],
    'Lambeth': ['Lambeth', 'Brixton', 'Clapham', 'Kennington', 'Stockwell', 'Streatham', 'Vauxhall', 'West Norwood'],
    'Wandsworth': ['Wandsworth', 'Balham', 'Battersea', 'Earlsfield', 'Furzedown', 'Putney', 'Roehampton', 'Southfields', 'Tooting', 'Wandsworth Common'],
    'Hammersmith and Fulham': ['Hammersmith', 'Fulham', 'Barons Court', 'West Kensington', 'Shepherd\'s Bush', 'White City'],
    'Kensington and Chelsea': ['Kensington', 'Chelsea', 'Earls Court', 'Holland Park', 'North Kensington', 'Notting Hill', 'South Kensington'],
    'Haringey': ['Haringey', 'Crouch End', 'Finsbury Park', 'Highgate', 'Hornsey', 'Muswell Hill', 'Seven Sisters', 'Tottenham', 'Wood Green'],
    'Enfield': ['Enfield', 'Edmonton', 'Enfield Town', 'Palmers Green', 'Southgate', 'Winchmore Hill'],
    'Barnet': ['Barnet', 'Chipping Barnet', 'Edgware', 'Finchley', 'Golders Green', 'Hendon', 'Mill Hill'],
    'Harrow': ['Harrow', 'Harrow on the Hill', 'Pinner', 'Stanmore', 'Wealdstone'],
    'Brent': ['Brent', 'Kilburn', 'Wembley', 'Neasden', 'Harlesden', 'Kingsbury'],
    'Ealing': ['Ealing', 'Acton', 'Greenford', 'Hanwell', 'Northolt', 'Southall'],
    'Hillingdon': ['Hillingdon', 'Hayes', 'Ruislip', 'Uxbridge', 'Yiewsley'],
    'Hounslow': ['Hounslow', 'Brentford', 'Chiswick', 'Feltham', 'Isleworth'],
    'Richmond upon Thames': ['Richmond', 'Twickenham', 'Teddington', 'Barnes', 'Hampton', 'Kew'],
    'Kingston upon Thames': ['Kingston', 'Chessington', 'New Malden', 'Surbiton'],
    'Merton': ['Merton', 'Mitcham', 'Morden', 'Wimbledon'],
    'Sutton': ['Sutton', 'Cheam', 'Worcester Park', 'Carshalton', 'Wallington'],
    'Croydon': ['Croydon', 'Addiscombe', 'Purley', 'South Norwood', 'Thornton Heath'],
    'Bromley': ['Bromley', 'Beckenham', 'Orpington', 'Penge', 'West Wickham'],
    'Bexley': ['Bexley', 'Crayford', 'Erith', 'Sidcup', 'Welling'],
    'Havering': ['Havering', 'Romford', 'Hornchurch', 'Upminster', 'Rainham'],
    'Redbridge': ['Redbridge', 'Ilford', 'Wanstead', 'Woodford'],
    'Newham': ['Newham', 'East Ham', 'Forest Gate', 'Plaistow', 'Stratford', 'Upton Park'],
    'Waltham Forest': ['Waltham Forest', 'Chingford', 'Leyton', 'Walthamstow'],
    'Barking and Dagenham': ['Barking', 'Dagenham']
}

# categories = {
#         "protest": ["protest", "rally", "strike", "demonstration", "march"],
#         "terrorism": ["terrorism", "terrorist", "terror attack", "cyberterrorism", "extremism", "radicalism"],
#         "violence": ["violence", "assault", "attack", "conflict", "clash", "altercation", "physical violence"],
#         "drugs": ["drug", "narcotic", "dealer", "drug trade", "narcotics trafficking"],
#         "firearm": ["firearm", "gun", "shooting", "weapon", "rifle", "shootout", "armed", "gun violence"],
#         "illegal immigration": ["illegal immigration", "undocumented", "human trafficking", "visa overstay",
#                                 "smuggling"],
#         "theft": ["theft", "thief", "hijacking", "stolen", "thieves", "larceny", "robbery", "robber", "burglary",
#                   "stealing"],
#         "police accountability": ["police accountability", "police misconduct", "internal affairs",
#                                   "police corruption"],
#         "community relations": ["community policing", "police community relations", "public engagement",
#                                 "community outreach"],
#         "legal and policy": ["legal proceedings", "policing policy", "law enforcement legislation", "jurisdiction",
#                              "legal reform"]
#     }

categories = {
    "protest": [
        "protest", "rally", "strike", "demonstration", "march", "protester", "demonstrator", "picketing",
        "civil disobedience", "sit-in", "walkout", "boycott", "public protest", "mass protest"
    ],
    "terrorism": [
        "terrorism", "terrorist", "terror attack", "bomber", "extremism", "radicalism", "jihad", "suicide bombing",
        "militant", "insurgency", "guerrilla warfare", "extremist", "radical", "jihadist", "terror cell"
    ],
    "violence": [
        "violence", "assault", "attack", "conflict", "clash", "altercation", "physical violence", "brutality",
        "fistfight", "melee", "brawl", "abuse", "aggression", "violent act", "battery", "violent confrontation"
    ],
    "drugs": [
        "drug", "narcotic", "dealer", "drug trade", "narcotics trafficking", "drug trafficking", "substance abuse",
        "drug abuse", "opiates", "amphetamines", "cannabis", "heroin", "cocaine", "methamphetamine"
    ],
    "firearm": [
        "firearm", "gun", "shooting", "weapon", "rifle", "shootout", "armed", "gun violence", "gunman",
        "shooter", "firearm possession", "gun control", "gun rights", "firearm safety", "assault rifle"
    ],
    "illegal immigration": [
        "illegal immigration", "undocumented", "human trafficking", "visa overstay", "smuggling", "border crossing",
        "unauthorized entry", "illegal migrant", "undocumented migrant", "immigration enforcement", "deportation"
    ],
    "theft": [
        "theft", "thief", "hijacking", "stolen", "thieves", "larceny", "robbery", "robber", "burglary",
        "stealing", "shoplifting", "pickpocketing", "burglar", "break-in", "mugging", "armed robbery"
    ],
    "police accountability": [
        "police accountability", "police misconduct", "internal affairs", "police corruption", "law enforcement misconduct",
        "police brutality", "excessive force", "officer involved shooting", "civil rights violation", "police reform"
    ],
    "community relations": [
        "community policing", "police community relations", "public engagement", "community outreach",
        "neighborhood watch", "community safety", "police officer", "law enforcement interaction", "public safety"
    ],
    "legal and policy": [
        "legal proceedings", "policing policy", "law enforcement legislation", "jurisdiction", "legal reform",
        "court ruling", "legislation", "judicial decision", "policy change", "regulatory standards"
    ]
}


def initialize_youtube(api_key):
    """Initialize the YouTube API client."""
    return build('youtube', 'v3', developerKey=api_key)


def get_week_of_year(date_string):
    """Returns the week number and year of the given date."""
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    date_obj = datetime.strptime(date_string, date_format)
    week_number = date_obj.isocalendar()[1]
    year = date_obj.isocalendar()[0]
    return week_number, year


def construct_queries():
    queries = []
    # Add general queries related to UK policing
    general_queries = [
        "UK police", "British law enforcement", "police in the UK",
        "UK police reforms", "national police service UK"
    ]
    queries.extend(general_queries)

    # Add major cities and regions
    major_cities_and_regions = [
        "Manchester police", "Birmingham police", "Glasgow police",
        "Edinburgh police", "Liverpool police", "Cardiff police",
        "Belfast police", "Bristol police", "Newcastle police",
        "Leeds police", "Sheffield police", "Nottingham police",
        "Southampton police", "Wales police", "Scotland police"
    ]
    queries.extend(major_cities_and_regions)

    london_queries = [
        "London Metropolitan Police", "London policing", "London law enforcement",
        "Metropolitan police UK"
    ]
    queries.extend(london_queries)

    return queries



def extract_borough(description, title):
    found_keywords = []
    description_lower = description.lower()  # Convert to lower once to optimize
    title_lower = title.lower()

    for borough, keywords in boroughs.items():
        for keyword in keywords:
            if keyword.lower() in description_lower or keyword.lower() in title_lower:
                found_keywords.append((keyword, borough))  # Capture what is being matched
                return borough

    return "Unknown"



def is_video_relevant(title, description, boroughs):
    content = title.lower() + " " + description.lower()

    # Check for general UK police relevance
    if "police" in content or "law enforcement" in content:
        return True

    # Enhanced checks for specific keywords related to broader UK policing issues
    uk_keywords = [
        "metropolitan", "constabulary", "police station", "police service",
        "bobby", "sergeant", "inspector", "constable", "uk crime", "british law"
    ]
    if any(keyword in content for keyword in uk_keywords):
        return True

    # Regional relevance check, maintaining original borough checks as part of broader filtering
    for borough, keywords in boroughs.items():
        borough_present = any(keyword.lower() in content for keyword in keywords)
        police_present = "police" in content or "law enforcement" in content
        if borough_present and police_present:
            return True

    return False


def fetch_videos(youtube, query, published_after, published_before):
    videos = []
    page_token = None
    while True:
        try:
            request = youtube.search().list(
                part="snippet",
                q=query,
                type="video",
                maxResults=50,
                pageToken=page_token,
                publishedAfter=published_after,
                publishedBefore=published_before
            )

            response = request.execute()
            for item in response.get('items', []):
                video_id = item['id']['videoId']
                video_request = youtube.videos().list(
                    part="snippet,statistics",
                    id=video_id
                )
                video_response = video_request.execute()

                if 'items' in video_response and video_response['items']:
                    statistics = video_response['items'][0].get('statistics', {})
                    view_count = int(statistics.get('viewCount', 0))
                    if view_count < 10000:  # Skip videos with less than 10k views
                        continue
                    likes_count = int(statistics.get('likeCount', 0))  # Fetch the number of likes

                    videos.append({
                        'videoId': video_id,
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'borough': extract_borough(item['snippet']['description'], item['snippet']['title']),
                        'week': get_week_of_year(item['snippet']['publishedAt']),
                        'num_mentions': 0,
                        'avg_sentiment': 0,
                        'weighted_sentiment': 0,
                        'total_weights': 0,
                        'category': None,
                        'num_comments': int(statistics.get('commentCount', 0)),
                        'views': view_count,
                        'likes': likes_count  # Store the number of likes in the dictionary
                    })
            page_token = response.get('nextPageToken')
            if not page_token:
                break
        except HttpError as e:
            print(f"An HTTP error occurred: {e.resp.status} - {e.content}")
            break
    return videos


def filter_videos(videos):
    filtered_videos = []
    for video in videos:
        if is_video_relevant(video['title'], video['description'], boroughs):
            filtered_videos.append(video)
    return filtered_videos


def fetch_comments(youtube, video_ids, max_results=100):
    comments = []
    for video_id in video_ids:
        try:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=max_results
            )
            response = request.execute()
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'videoId': video_id,
                    'text': comment['textDisplay'],
                    'likes': comment['likeCount']
                })
        except HttpError as e:
            print(f"An HTTP error occurred: {e.resp.status} - {e.content}")
    return comments


def determine_category(title, description, comments, categories):
    """
    Determine the most relevant category for a video based on the content of its title,
    description, and comments.
    """
    content = title.lower() + " " + description.lower()
    content += " ".join(comment['text'].lower() for comment in comments)

    category_scores = {category: 0 for category in categories}

    for category, keywords in categories.items():
        for keyword in keywords:
            category_scores[category] += content.count(keyword.lower())

    # Assign the category with the highest score
    assigned_category = max(category_scores, key=category_scores.get)
    return assigned_category if category_scores[assigned_category] > 0 else None


def analyze_comments(videos, comments, categories):
    """Analyze comments and update video statistics based on content and sentiment."""
    for video in videos:
        video_comments = [c for c in comments if c['videoId'] == video['videoId']]
        total_sentiment = 0
        for comment in video_comments:
            sentiment = TextBlob(comment['text']).sentiment.polarity
            total_sentiment += sentiment
            video['num_mentions'] += 1
            video['weighted_sentiment'] += sentiment * (comment['likes'] + 1)
            video['total_weights'] += (comment['likes'] + 1)

        # Calculate title sentiment
        title_sentiment = TextBlob(video['title']).sentiment.polarity
        # Calculate description sentiment
        description_sentiment = TextBlob(video['description']).sentiment.polarity

        # Update video dictionary with title and description sentiments
        video['title_sentiment'] = title_sentiment
        video['description_sentiment'] = description_sentiment

        if video_comments:
            video['avg_sentiment'] = total_sentiment / len(video_comments)
        if video['total_weights'] > 0:
            video['weighted_sentiment'] /= video['total_weights']




def main():
    api_key = 'AIzaSyBe4w7KPESzuJBwGnHL_89GYxdI_58oJr8'
    youtube = initialize_youtube(api_key)
    queries = construct_queries()
    published_after = '2015-01-01T00:00:00Z'
    published_before = '2019-12-31T23:59:59Z'
    all_videos = []
    for query in queries:
        videos = fetch_videos(youtube, query, published_after, published_before)
        all_videos.extend(videos)
    filtered_videos = filter_videos(all_videos)
    video_ids = [video['videoId'] for video in filtered_videos]
    comments = fetch_comments(youtube, video_ids)
    analyze_comments(filtered_videos, comments, categories)

    # Sort comments by likes and get top-10 comments for each video
    for video in filtered_videos:
        video_comments = [comment for comment in comments if comment['videoId'] == video['videoId']]
        if not video_comments or all(comment['likes'] == 0 for comment in video_comments):
            # Include all comments if there are no comments or if none have likes
            video['top_comments'] = video_comments
        else:
            sorted_comments = sorted(video_comments, key=lambda x: x['likes'], reverse=True)
            video['top_comments'] = sorted_comments[:10]

    for video in filtered_videos:
        video['category'] = determine_category(video['title'], video['description'], video['top_comments'], categories)

    print(f"Found {len(filtered_videos)} videos.")

    # Save data to JSON for further analysis
    with open('youtube_videos_filtered.json', 'w') as file:
        json.dump(filtered_videos, file, indent=4)

if __name__ == "__main__":
    main()
