import os
import requests
import json
import pandas as pd                        
from crewai import Agent, Task, Crew, Process
#from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.agents import load_tools
from langchain.tools import tool
from langchain_community.tools.google_trends import GoogleTrendsQueryRun
from langchain_community.utilities.google_trends import GoogleTrendsAPIWrapper
# from tools.google_trends import get_google_trends
from langchain_community.tools import DuckDuckGoSearchRun
from pytrends.request import TrendReq

@tool("Function to get Google Trends data")
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
    
    # while True:
    #     try:
    #         # Get data from each function
    #         interest_by_region = pytrend.interest_by_region()
    #         interest_over_time = pytrend.interest_over_time()
    #         related_topics = pytrend.related_topics()
    #         related_queries = pytrend.related_queries()
            
    #         # Check if dataframes are not empty
    #         if (not interest_by_region.empty and 
    #             not interest_over_time.empty and 
    #             related_topics and related_queries):
    #             return interest_by_region, interest_over_time, related_topics, related_queries
    #         else:
    #             continue
    #     except Exception as e:
    #         print("Error:", e)
    #         continue


os.environ["OPENAI_API_KEY"] = ""

llm = ChatOpenAI(
  temperature=0.7,
  model_name="gpt-3.5-turbo",
)

brand_name="HAZWOPER OSHA"
brand_mission= "We are a team of safety professionals and enthusiasts who are driven by a central mission: preserving lives. We develop and offer HAZWOPER, RCRA, OSHA, DOT, HAZMAT, MSHA and NFPA 70E safety training courses online, in traditional in-person onsite settings, as well as through virtual instructor-led sessions. Our goal is to aid employers in meeting their responsibilities by adhering to regulations set forth by OSHA, EPA, DOT, and other safety authorities. Our mission is to provide superior quality training services that: INSPECTORS select for their clients, CLIENTS recommend to friends and colleagues, TEACHERS prefer for their students, EMPLOYEES are proud of, and INVESTORS seek for long-term returns.Industrial Training and OSHA Compliance Solutions: Your one-stop shop for workplace safety and compliance. Our mission is to provide superior quality training services that: INSPECTORS select for their clients, CLIENTS recommend to friends and colleagues, TEACHERS prefer for their students, EMPLOYEES are proud of, and INVESTORS seek for long-term returns."
brand_desc="Our commitment extends to ensuring an exceptional customer journey for each and every client. This commitment is rooted in placing our clients' needs and concerns at the forefront of all our endeavors. What sets apart our safety training courses is our unwavering dedication to keeping learners engaged, presenting them with challenges, and furnishing them with substantial knowledge. Our training courses are meticulously designed to adhere to both current state and federal regulations. Moreover, our commitment to excellence has earned us exceptional ratings from respected entities such as the Better Business Bureau, Google, and other prominent organizations. It's worth noting that our courses have been trusted and utilized by esteemed institutions including the Federal Bureau of Investigation (FBI), the National Aeronautics and Space Administration (NASA), as well as numerous federal and local municipalities. These partnerships are a testament to our dedication to ensuring customer satisfaction and our willingness to exceed expectations. Our team is composed of exceptionally qualified instructors who possess a wealth of experience and training in the realm of occupational safety and health. Their expertise spans a variety of subjects within the Environmental Health and Safety (EH&S) domain. At the helm, our senior leadership boasts over two decades of practical experience in Environmental Health & Safety. They are perpetually seeking innovative avenues to enhance the overall educational and training experience. Our Address is : 11901 Santa Monica Blvd., Suite # 414 Los Angeles, CA 90025 and our email is :info@HAZWOPER-OSHA.com"
brand_category = "Health & Safety Training "
prompt= "Generate content about our upcoming course 'burning hazards' that is a fire safety course launching on easters."
num_of_posts = 3

#Tools
human_tools = load_tools(["human"])
search_tool = DuckDuckGoSearchRun()
# google_trend = get_google_trends(brand_category)

#Agents
Brand_Consultant = Agent(
    role='Personal Brand Consultant',
    goal=f"""Gather insights into the user's brand :{brand_name} brand, mission:{brand_mission}, and target audience, and 
    provide a comprehensive understanding of their brand aspirations. {brand_desc} Conduct amazing analysis of the 
    products and competitors, providing in-depth insights to guide marketing strategies.""",
    verbose=True,
    backstory=f"""As the Lead Brand Consultant at a premier digital marketing firm, you specialize in dissecting
	Branding of a Company. You have knowledge of Branding as a whole and create knowledge basis of your brand""",
    tools=[search_tool],
    llm=llm
)

# Creating a Trend Researcher agent
Trend_Researcher = Agent(
    role='Digital Trends Analyst',
    goal=f"the brand category is {brand_category} your goal is To scour a wide array of sources, including DuckDuckGo, Google Trends, YouTube, and other relevant platforms, for trends, articles, books, and videos that align with the user's brand strategy,",
    verbose=True,
    backstory=f"""You are at the forefront of trend analysis but of the {brand_category} industry, with an uncanny ability to sift through the noise and identify the signals that matter. 
    Using cutting-edge tools and your intuition for what's next, you provide a roadmap for content that not only trends but sets the pace for industry standards.""",
    tools=[search_tool], #get_google_trends(brand_category),
    llm=llm
)

Data_Insight_Gatherer=Agent(
    role='Data Insights Analyst',
    goal=f"""Using All the data collected. You are now the actual embodiment of the brand {brand_name}. You will now using 
    the insights, make a graph and generate questions about the brand then come up with answers to these 
    questions as well""",
    verbose=True,
    backstory=f"""Some questions that you should come up with answers are:
    1. What is the overarching vision for your  brand? Consider what you ultimately want to achieve or be known for. 
    2. Can you define the mission of your  brand? This should reflect your core values and what you stand for.
    3. Who is your target audience? Try to describe them in terms of demographics (age, location, gender, etc.) and psychographics (interests, values, lifestyle, etc.).
    4. What message do you want to convey through your  brand? Think about the key takeaways you want your audience to have.
    5. How does your current social media presence reflect your  brand's vision and mission? Please provide specific examples or tweets that you believe are aligned or misalig ned with your brand.
    6. What are your primary goals for your  brand over the next year? Consider both qualitative and quantitative goals.
    7. How do you differentiate yourself from others in your field or niche? What makes your  brand unique?
    8. Can you share any feedback or insights you've received from your audience about your  brand? This could include direct comments, engagement patterns, or any other form
    of feedback.
    9. What are the biggest challenges you face in building and maintaining your  brand?
    10. Are there any specific people or brands that inspire your  brand? If so, what aspects of their branding do you admire?""",
    tools=[search_tool], #get_google_trends(brand_category),
    llm=llm
)

Brand_Content_Writer =  Agent(
    role='Brand Content Writer',
    goal=f"""With all the knowledge you have accumulated Craft compelling content for {brand_name}""",
    backstory=f""""As a versatile Content Strategist and writer, you are renowned for creating insightful and engaging marketing posts 
        tailored for various brands across multiple social media platforms. Your expertise lies in transforming complex concepts into compelling 
        narratives, ensuring maximum impact for each unique brand.""",
    verbose=True,
    allow_delegation=True,
    llm=llm
)

# #Tasks  Describe the personality and tone associated with 
#       the brand. Is it friendly, professional, playful, or authoritative. Define the key messages or phrases 
#       associated with the brand. What does the brand want to communicate to its audience.Outline the brand's 
#       future goals and aspirations.Where does the brand envision itself in the coming years?

Brand_Review = Task(
      description=f"""Conduct a comprehensive analysis of {brand_name},which is in the {brand_category} industry, brief description of the 
      brand{brand_desc}. Include its mission{brand_mission}, values, Products and unique selling points. 
      The Brands Target Audience. Identify key competitors, but never mention their names, in the industry 
      and how the brand differentiates itself from them. """,
      agent=Brand_Consultant
    )

Trend_Analysis = Task(
    description=f"""Leverage insights from the brand identity analysis to identify and compile trends, 
    articles, books, and videos that resonate with the brand's strategic direction. Focus on content that 
    not only aligns, do not hesitate to reach broader topics but also holds relevance to the brand's core 
    identity and future aspirations. When searching do not explicitly state any year""",
    expected_output=f""" A comprehensive content strategy report highlighting relevant trends, articles, 
    books, and YouTube videos, aimed at inspiring future posts and content creation that aligns with the 
    brand's ideal trajectory.""",

    agent=Trend_Researcher,
)

# Gather_Insights = Task(
#     description="""Use the tool and initiate a deep dive into the user's personal brand vision, mission,
#     target audience through their social media presence for their brand, from their perspective. From these 
#     inputs analyze and come up with questions about the brand and thier respectove answers.""",
#     expected_output="A comprehensive understanding of the user's brand in the form of a knowledge graph by generating questions and answering already assigned questions and their respective answers.",
#     tools= [search_tool] + human_tools,
#     agent=Data_Insight_Gatherer,
#     context=[],
# )

# Task for the Brand Identity Writer to synthesize insights from the initial review into a cohesive analysis, outlining the discrepancies between the current and ideal state of the user's personal brand, complete with actionable recommendations.
Brand_Content_Generation = Task(
    description=f"""Using the insights provided, {prompt}, Can you generate {num_of_posts} posts for this prompt with different versions to 
    post on seperate days. Just give me the response nothing else is required. """,
    expected_output="""Generate the best possible content for the brand tailored to the social media prompted
    if no social media is prompted generate content""",
    tools=[search_tool],
    agent=Brand_Content_Writer,
)

#Crew Chain
crew = Crew(
  agents=[Brand_Consultant, Trend_Researcher,Brand_Content_Writer], #Data_Insight_Gatherer       
  tasks=[Brand_Review, Trend_Analysis, Brand_Content_Generation], #Gather_Insights
  process=Process.sequential,
)

result = crew.kickoff()

print("###############################################################")
print(result)

# Make sure that your response is less than 1600 
#     words and includes necessary details but donot mention the charachter count. Donot give any further
#     details just the response is enough.