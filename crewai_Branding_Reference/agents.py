import os
from textwrap import dedent
from crewai import Agent
from langchain.agents import load_tools
from langchain.llms import Ollama
from tasks import MarketingAnalysisTasks

class BrandSpecificContentAgents:
    def __init__(self):
        self.llm = Ollama(model=os.environ['MODEL'])
        self.tasks = MarketingAnalysisTasks()

    def generate_content_agent(self, platform):
        if platform == "linkedin":
            goal_description = "Generate professional and informative content tailored for LinkedIn."
            backstory_description = "As a LinkedIn Content Creator, your mission is to create professional and informative posts that align with the brand's identity and goals."
        elif platform == "instagram":
            goal_description = "Craft catchy and visually appealing content suitable for Instagram."
            backstory_description = "As an Instagram Content Creator, your mission is to create visually appealing and engaging posts that resonate with the audience on a personal level."
        elif platform == "facebook":
            goal_description = "Create engaging and shareable content suitable for Facebook's diverse audience."
            backstory_description = "As a Facebook Content Creator, your mission is to create engaging and shareable posts that appeal to Facebook's diverse audience."
        elif platform == "pinterest":
            goal_description = "Design creative and inspiring content tailored for Pinterest's visual platform."
            backstory_description = "As a Pinterest Content Creator, your mission is to design creative and inspiring posts that capture the audience's attention and drive engagement."

        return Agent(
            role=f"{platform.capitalize()} Content Creator",
            goal=dedent(f"""\
                {goal_description}
                Use the provided branding-specific questions to craft personalized content that resonates with the audience.
                """),
            backstory=dedent(f"""\
                {backstory_description}
                Leverage your creativity and insights to produce content that captivates the audience and drives engagement.
                """),
            tools=load_tools(),
            llm=self.llm,
            allow_delegation=False,
            verbose=True
        )

    def create_agents(self):
        instagram_agent = self.generate_content_agent("instagram")
        linkedin_agent = self.generate_content_agent("linkedin")
        facebook_agent = self.generate_content_agent("facebook")
        pinterest_agent = self.generate_content_agent("pinterest")

        return {
            "instagram": instagram_agent,
            "linkedin": linkedin_agent,
            "facebook": facebook_agent,
            "pinterest": pinterest_agent
        }
