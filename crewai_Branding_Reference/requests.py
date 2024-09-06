from langchain.agents import load_tools
from langchain_community.utilities import TextRequestsWrapper

# Load the requests tool
requests_tools = load_tools(["requests_all"])
requests_wrapper = requests_tools[0].requests_wrapper


def fetch_website_data(url):
    response = requests_wrapper.get(url)
    return response


def main():
    
    url = input("Enter the website URL: ")

    website_data = fetch_website_data(url)
    
    print("Website Data:")
    print(website_data)

# Run the main function
if __name__ == "__main__":
    main()
