import sqlite3
from datetime import datetime

def get_publication_times():
    connection = sqlite3.connect("news.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT story_id, brief, created_at, published_at
        FROM stories
        WHERE status = 'published'
    """)

    stories = cursor.fetchall()
    connection.close()

    results = []

    for story in stories:
        story_id = story[0]
        brief = story[1]
        created_at = datetime.fromisoformat(story[2])
        published_at = datetime.fromisoformat(story[3])

        time_taken = published_at - created_at

        results.append({
            "story_id": story_id,
            "brief": brief,
            "time_taken": time_taken
        })

    return results

def get_desk_head_report(report_date):
    connection = sqlite3.connect("news.db")
    cursor = connection.cursor()

    cursor.execute("""
    SELECT story_id, brief, created_at, published_at
    FROM stories
    WHERE status = 'published'
    AND date(published_at) = ?
""", (report_date,))
    
    stories = cursor.fetchall()
    connection.close()

    report = []

    for story in stories:
        story_id = story[0]
        brief = story[1]
        created_at = datetime.fromisoformat(story[2])
        published_at = datetime.fromisoformat(story[3])

        time_taken = published_at - created_at

        report.append({
            "story_id": story_id,
            "brief": brief,
            "published_at": published_at,
            "time_taken": time_taken
        })

    return {
        "total_published": len(report),
        "stories": report
    }

if __name__ == "__main__":
    print(get_desk_head_report("2026-09-04"))