import pprint
import os
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Initialize the ChatOpenAI instance
os.environ["OPENAI_API_KEY"] = ""
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

# Define the extract function
def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).run(content)

# Function to scrape content with Playwright and extract using LLM
def scrape_with_playwright(url):
    loader = AsyncChromiumLoader([url])
    docs = loader.load()

    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(docs, tags_to_extract=["span"])

    print("Extracting content with LLM")

    # Split documents into chunks for processing
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1000, chunk_overlap=0)
    splits = splitter.split_documents(docs_transformed)

    # Process the first split
    extracted_content = extract(schema={}, content=splits[0].page_content)
    pprint.pprint(extracted_content)
    return extracted_content

# Main function to initiate scraping
def main():
    url = input("Enter the URL to scrape: ")
    extracted_content = scrape_with_playwright(url)
    print(extracted_content)

if __name__ == "__main__":
    main()


