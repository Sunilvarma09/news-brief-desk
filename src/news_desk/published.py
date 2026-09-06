from datetime import datetime, timedelta
from news_desk.models import Story
from news_desk.investigate import State

def publish(state: State):

    stories = state["stories"]
    published_stories = []

    for story in stories:
        if story.status == "approved":
            story.status = "published"
            story.published_at = story.created_at + timedelta(hours=2)
            published_stories.append(story)
            
    return {"stories": published_stories}