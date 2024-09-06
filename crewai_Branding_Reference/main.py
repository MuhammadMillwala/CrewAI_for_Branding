from dotenv import load_dotenv
load_dotenv()

from agents import BrandSpecificContentAgents
from tasks import BrandingTasks

def ask_branding_questions():
    branding_answers = {}
    print("To initiate a deep dive into your personal brand's vision, mission, and target audience, I need to ask you some comprehensive questions.")
    print("These questions are designed to uncover the core of your personal brand and help us create a strategy that aligns with your goals.")
    print("Please answer the following questions in as much detail as possible:")

    for i in range(1, 11):
        question = input(f"{i}. ")
        branding_answers[i] = question
    
    return branding_answers

def main():
    # Ask branding questions
    branding_answers = ask_branding_questions()

    # Create Branding Tasks
    branding_tasks = BrandingTasks()

    # Generate Brand-Specific Content Agents
    content_agents = BrandSpecificContentAgents()
    agents = content_agents.create_agents()

    for platform, agent in agents.items():
        # Generate branding task for each platform
        branding_task = branding_tasks.generate_branding_task(platform, branding_answers)
        print(f"\n### Branding Task for {platform.capitalize()} ###")
        print(branding_task.description)
        print("")

if __name__ == "__main__":
    main()
