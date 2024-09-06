import json
import os
import requests
from langchain.tools import tool

class SearchTools():

    @staticmethod
    @tool("Search internet")
    def search_internet(query):
        """Useful to search the internet about a given topic and return relevant results."""
        return SearchTools.search(query)

    @staticmethod
    @tool("Search instagram")
    def search_instagram(query):
        """Useful to search for instagram posts about a given topic and return relevant results."""
        query = f"site:instagram.com {query}"
        return SearchTools.search(query)

    @staticmethod
    @tool("Search linkedin")
    def search_linkedin(query):
        """Useful to search for LinkedIn posts about a given topic and return relevant results."""
        query = f"site:linkedin.com {query}"
        return SearchTools.search(query)

    @staticmethod
    @tool("Search facebook")
    def search_facebook(query):
        """Useful to search for Facebook posts about a given topic and return relevant results."""
        query = f"site:facebook.com {query}"
        return SearchTools.search(query)

    @staticmethod
    @tool("Search pinterest")
    def search_pinterest(query):
        """Useful to search for Pinterest posts about a given topic and return relevant results."""
        query = f"site:pinterest.com {query}"
        return SearchTools.search(query)

    @staticmethod
    def search(query, n_results=5):
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            'content-type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        results = response.json()['organic']
        results = [result for result in results if 'link' in result and 'title' in result]
        results = results[:n_results]
        content = '\n'.join([
            f"Title: {result['title']}\nLink: {result['link']}\nSnippet: {result.get('snippet', 'N/A')}\n"
            for result in results
        ])
        return f"\nSearch result: \n{content}\n"
