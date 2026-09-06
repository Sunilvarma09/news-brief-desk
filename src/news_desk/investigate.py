from typing_extensions import TypedDict
from news_desk.models import NewsItem, Story
from langchain_groq import ChatGroq
from datetime import datetime
import json
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

model = ChatGroq(
    model_name="openai/gpt-oss-120b",
    api_key=api_key
)


class State(TypedDict):
    news_items: list[NewsItem]
    stories: list[Story]


def investigate(state: State):
    news_items = state["news_items"]

    prompt = f"""You are a news desk assistant. Your task is to investigate and summarize the news based on content, news id, and news source.

Follow these instructions:

-Investigate each news item based on its content, id, and source.
-If multiple news items describe the SAME real-world event,group them together even if they use different wording.
-If news items have a similar topic but describe DIFFERENT real-world events, keep them in different groups.
-For each unique story, provide a short and clear brief.
-Do not put the same news item in multiple groups.
-or every group, provide the news IDs and sources that belong to that story.

News items:
{news_items}


Return the response using this structure:

[
    {{
        "story_id": "Generate a unique story ID",
        "brief": "Short summary of the unique real-world event",
        "news_ids": ["News IDs belonging to this story"],
        "sources": ["Sources belonging to this story"]
    }}d
]"""
    result = model.invoke(prompt)
    stories_data = json.loads(result.content)

    stories = []

    for story_data in stories_data:
        story_news_items = []

        for news_item in news_items:
            if news_item.id in story_data["news_ids"]:
                story_news_items.append(news_item)

        story = Story(
            story_id=story_data["story_id"],
            brief=story_data["brief"],
            news_items=story_news_items,
            status="investigated",
            created_at=max(item.received_at for item in story_news_items),
            published_at=None
        )

        stories.append(story)

    return {
        "stories": stories
    }





