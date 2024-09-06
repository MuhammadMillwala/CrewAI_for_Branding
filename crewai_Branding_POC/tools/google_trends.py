from pytrends.request import TrendReq
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool


# @tool("Google Trend Analysis")
# def get_google_trends(category):

#     interest_over_time_df,  = pytrends.interest_over_time()
#     interest_by_region_df = pytrends.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
#     related_topics_dict = pytrends.related_topics()
#     related_queries_dict = pytrends.related_queries()

#     return {
#         "interest_over_time": interest_over_time_df,
#         "interest_by_region": interest_by_region_df,
#         "related_topics": related_topics_dict,
#         "related_queries": related_queries_dict
#     }

# def get_trends(pytrend):
#     if pytrend.interest_over_time() != 400:
#     # if pytrend.interest_by_region() & pytrend.interest_over_time() & pytrend.related_topics() & pytrend.related_queries():
#         return pytrend.interest_by_region(),pytrend.interest_over_time(),pytrend.related_topics(),pytrend.related_queries()
#     get_trends(pytrend)

@tool("Function to get Google Trends data")
def get_google_trends(pytrends):
    """
    This function retrieves Google Trends data using the provided pytrends object.
    Args:
        pytrends (TrendReq): An instance of TrendReq from pytrends.
    Returns:
        DataFrame: A DataFrame containing the Google Trends data.
    """
    
    while True:
        try:
            # Get data from each function
            interest_by_region = pytrends.interest_by_region()
            interest_over_time = pytrends.interest_over_time()
            related_topics = pytrends.related_topics()
            related_queries = pytrends.related_queries()
            
            # Check if dataframes are not empty
            if (not interest_by_region.empty and 
                not interest_over_time.empty and 
                related_topics.empty and related_queries.empty):
                return interest_by_region, interest_over_time, related_topics, related_queries
            else:
                continue
        except Exception as e:
            print("Error:", e)
            continue