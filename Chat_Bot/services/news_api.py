import requests
import random



def fetch_random_news(api_key, country="us", category=None, language="en"):
    # URL for the News API endpoint
    url = f"https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}&language={language}"

    if category:
        # If category is provided, add it to the URL
        url += f"&category={category}"

    try:
        # Send GET request to News API
        response = requests.get(url)
        
        # Check if the response is successful (HTTP status code 200)
        if response.status_code == 200:
            data = response.json()  # Parse the JSON response
            articles = data.get('articles', [])
            
            # Check if there are articles in the response
            if articles:
                # Randomly pick one article from the list
                article = random.choice(articles)
                return f"Headline: {article['title']}"
                # print(f"Description: {article['description']}")
                # print(f"URL: {article['url']}")
            else:
                return "No articles found."
        else:
            return f"Error: Unable to fetch news. Status code {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Request error: {e}"
    

# api_key = "f5e28cedb4f54e23a37e762df0e86b92"
