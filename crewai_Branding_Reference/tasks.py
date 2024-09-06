from crewai import Task
from textwrap import dedent

class BrandingTasks:
    def __init__(self):
        self.branding_questions = [
            "What is the overarching vision for your personal brand? Consider what you ultimately want to achieve or be known for.",
            "Can you define the mission of your personal brand? This should reflect your core values and what you stand for.",
            "Who is your target audience? Try to describe them in terms of demographics (age, location, gender, etc.) and psychographics (interests, values, lifestyle, etc.).",
            "What message do you want to convey through your personal brand? Think about the key takeaways you want your audience to have.",
            "How does your current social media presence reflect your personal brand's vision and mission? Please provide specific examples or tweets that you believe are aligned or misaligned with your brand.",
            "What are your primary goals for your personal brand over the next year? Consider both qualitative and quantitative goals.",
            "How do you differentiate yourself from others in your field or niche? What makes your personal brand unique?",
            "Can you share any feedback or insights you've received from your audience about your personal brand? This could include direct comments, engagement patterns, or any other form of feedback.",
            "What are the biggest challenges you face in building and maintaining your personal brand?",
            "Are there any specific people or brands that inspire your personal brand? If so, what aspects of their branding do you admire?"
        ]

    def generate_branding_task(self, platform, branding_answers):
        if platform == "linkedin":
            task_description = "Develop a professional and informative LinkedIn profile based on your personal branding."
        elif platform == "instagram":
            task_description = "Create visually appealing and engaging Instagram posts that reflect your personal branding."
        elif platform == "facebook":
            task_description = "Design engaging and shareable Facebook posts aligned with your personal branding."
        elif platform == "pinterest":
            task_description = "Curate creative and inspiring Pinterest boards that showcase your personal branding."

        return Task(
            description=dedent(f"""\
                {task_description}
                Use the provided branding-specific questions to tailor your profile/posts/boards to resonate with your target audience and convey your brand message effectively.
                Answer the following questions to guide your branding process:

                {self._format_branding_questions(branding_answers)}
                """),
            agent=None
        )

    def _format_branding_questions(self, branding_answers):
        formatted_questions = ""
        for i, question in enumerate(self.branding_questions, start=1):
            formatted_questions += f"{i}. {question}\n"
            if i in branding_answers:
                formatted_questions += f"   - {branding_answers[i]}\n\n"
            else:
                formatted_questions += "\n"

        return formatted_questions
