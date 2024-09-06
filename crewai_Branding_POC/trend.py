# @tool("Function to get Google Trends data")
from pytrends.request import TrendReq

def get_google_trends(brand_category):
    """
    This function retrieves Google Trends data using the provided brand category.
    Args:
        brand_category (str): The category to query Google Trends.
    Returns:
        tuple: A tuple containing DataFrames for interest by region and interest over time.
    """
    try:
        # Pytrend initialization
        pytrend = TrendReq()#hl='PK', tz=360
        kw_list = [brand_category]
        pytrend.build_payload(kw_list=kw_list,
                              cat=0,
                              timeframe='today 3-m',
                              geo='PK',
                              gprop='')
        
        # Get data from each function
        interest_by_region = pytrend.interest_by_region()
        interest_over_time = pytrend.interest_over_time()
        
        return interest_by_region, interest_over_time
    except Exception as e:
        # Error handling
        raise Exception(f"An error occurred while retrieving Google Trends data: {str(e)}")
      
brand_category = "Fashion & Clothing"
print(get_google_trends(brand_category))