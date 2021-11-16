from newsapi import NewsApiClient
import praw

news_api = NewsApiClient('02bf0c8cb0a24d64bb1550fe4150b9fe')

reddit_api = praw.Reddit(client_id = 'QhNpcMeqHZYk_RsE_90Npg',
                        client_secret = 'uvQnC85T2YBmEubA-wevfe1n7_2ikw',
                        user_agent= 'rashid')

def fetch_reddit_api(query):
    """Calls reddit API. Gets search results on the given query from the news section.
    If no keyword (query) is provided it just gets "hot" news articles.

    Args:
        query (str): a keyword to search in reddit. can be NULL.

    Returns:
        list: returns a list of dictionaries, where each dictionary contains details about a seperate searched news article.
    """    
    try:

        output=[]

        if query == None:
            subreddit = reddit_api.subreddit('news').hot()
        else:
            subreddit = reddit_api.subreddit('news').search(query)
        
        for subs in subreddit:
            reddit_news = {'headline':subs.title,
                            'link':subs.url,
                            'source':'reddit'}
            output.append(reddit_news)
        
        return output

    except Exception as e:
        print(e)

def fetch_news_api(query):
    """Calls reddit API. Gets search results on the given query from the top headlines in general category.
    If no keyword (query) is provided it just gets "top" news articles from general category.

    Args:
        query (str): a keyword to search in newsapi. can be NULL.

    Returns:
        list: returns a list of dictionaries, where each dictionary contains details about a seperate searched news article.
    """    
    try:

        output=[]

        newsapi_news = news_api.get_top_headlines(q=query,category='general')

        for news in newsapi_news['articles']:
            top_news = {"headline":news["title"],
                    "link": news["url"],
                    "source":"newsapi"}
            output.append(top_news)

        return output

    except Exception as e:
        print(e)
    

def get_news(query):
    """calls the third party api functions above (fetch_news_api & fetch_reddit_api).
    concatenates the details of news articles from all the third party applications.
    

    Args:
        query (str): a keyword to search in third party news APIs. can be NULL.

    Returns:
        list: returns a list of dictionaries, where each dictionary contains details about a seperate searched news article.
    """    

    try:
        return fetch_reddit_api(query) + fetch_news_api(query)
        
    except Exception as e:
        print(e)
    
