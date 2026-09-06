import json
from datetime import datetime, timedelta
from news_desk.models import NewsItem
from news_desk.graph import graph
from news_desk.database import create_database, save_stories
from news_desk.head_desk import get_desk_head_report


with open("data/news.json", "r") as file:
    data = json.load(file)

news_items = [NewsItem(**item) for item in data]

create_database()

state = {
    "news_items": news_items,
    "stories": []
}

result = graph.invoke(state)

save_stories(result["stories"])

for story in result["stories"]:
    print(f"\n{story.story_id}")
    print(f"Status: {story.status}")
    print(f"Brief: {story.brief}")
    print("Sources:")
    for item in story.news_items:
        print(f"- {item.source}")
    print(f"Published: {story.published_at}")
    print(f"Time taken: {story.published_at - story.created_at}")

report_date = (datetime.now().date() - timedelta(days=1)).isoformat()
report = get_desk_head_report(report_date)

print("\nDesk Head Report")
print(f"Total published: {report['total_published']}")

for story in report["stories"]:
    print(f"\n{story['story_id']}")
    print(f"Brief: {story['brief']}")
    print(f"Published: {story['published_at']}")
    print(f"Time taken: {story['time_taken']}")