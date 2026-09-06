import sqlite3

def create_database():
    connection = sqlite3.connect("news.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stories (
            story_id TEXT PRIMARY KEY,
            brief TEXT,
            status TEXT,
            created_at TEXT,
            published_at TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_stories(stories):
    connection = sqlite3.connect("news.db")
    cursor = connection.cursor()

    for story in stories:
        cursor.execute("""
            INSERT OR REPLACE INTO stories
            (story_id, brief, status, created_at, published_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            story.story_id,
            story.brief,
            story.status,
            story.created_at.isoformat(),
            story.published_at.isoformat() if story.published_at else None
        ))

    connection.commit()
    connection.close()

def get_published_stories():
    connection = sqlite3.connect("news.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT story_id, brief, status, created_at, published_at
        FROM stories
        WHERE status = 'published'
    """)

    stories = cursor.fetchall()
    connection.close()

    return stories

if __name__ == "__main__":
    create_database()
    print("I")