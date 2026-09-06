import json
from datetime import datetime
from langchain_groq import ChatGroq
from news_desk.investigate import State
from dotenv import load_dotenv
import os

from news_desk.models import Story


load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(
    model_name="openai/gpt-oss-120b",
    api_key=api_key
)

def editor(state: State):
    stories = state["stories"]

    prompt = f"""
You are a news desk editor.

Review the investigated news stories below.

For each story:
- Rewrite the brief so it is short, clear, and professional.
- Use only the information provided in the story.
- Do not invent facts.
- Keep the meaning of the original story.
- The rewritten brief should be suitable for publication.

Stories:
{stories}

Return JSON in this format:

[
    {{
        "story_id": "existing story id",
        "brief": "rewritten brief"
    }}
]
"""

    result = model.invoke(prompt)
    edited_stories = json.loads(result.content)

    updated_stories = []

    for story in stories:

        for edited_story in edited_stories:
            if story.story_id == edited_story["story_id"]:
                story.brief = edited_story["brief"]
                story.status = "approved"

                updated_stories.append(story)

    return {"stories": updated_stories}