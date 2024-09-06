import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

def scrape_website(url):
    # Initialize an empty dictionary to store data
    scraped_data = {}

    # Send a GET request to the website
    response = requests.get(url)
    
    # Parse HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all links on the website
    links = soup.find_all('a', href=True)
    
    # Extract data from each link
    for link in links:
        # Get the URL of the link
        link_url = link['href']
        
        # Check if the URL is relative
        if not link_url.startswith('http'):
            # Construct absolute URL
            link_url = urljoin(url, link_url)
        
        try:
            # Send a GET request to the link URL
            link_response = requests.get(link_url)
            
            # Parse HTML content of the link URL
            link_soup = BeautifulSoup(link_response.content, 'html.parser')
            
            # Extract text data from the link URL
            text_data = link_soup.get_text()
            
            # Store the text data in the scraped_data dictionary
            scraped_data[link_url] = text_data
        except Exception as e:
            print(f"Error scraping {link_url}: {e}")
            continue

    return scraped_data

def create_dataframes(scraped_data):
    dataframes = []
    for url, text_data in scraped_data.items():
        # Create a dataframe with URL as column name and text data as values
        df = pd.DataFrame({url: [text_data]})
        dataframes.append(df)
    return dataframes

if __name__ == "__main__":
    # Input the URL of the website you want to scrape
    website_url = input("Enter the URL of the website to scrape: ")
    
    # Scrape the website
    scraped_data = scrape_website(website_url)
    
    # Create dataframes from scraped data
    dataframes = create_dataframes(scraped_data)
    
    # Concatenate dataframes into a single dataframe
    final_dataframe = pd.concat(dataframes, axis=1)
    
    # Print the final dataframe
    print(final_dataframe)
