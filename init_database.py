import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.core.database import create_tables, reset_database
from src.repositories.repository import post_repository, comment_repository
from src.models.pydantic_models import PostCreate, CommentCreate

def create_sample_data():
    """Create some sample blog posts and comments for testing."""
    try:
        sample_posts = [
            PostCreate(
                title="Welcome to Our Blog",
                content="This is our first blog post. Welcome to our amazing blog platform!",
                author="Admin"
            ),
            PostCreate(
                title="Getting Started with FastAPI",
                content="FastAPI is a modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints.",
                author="Tech Writer"
            ),
            PostCreate(
                title="SQLAlchemy Best Practices",
                content="Here are some best practices when working with SQLAlchemy ORM in your Python applications.",
                author="Database Expert"
            )
        ]

        created_posts = []
        for post_data in sample_posts:
            post = post_repository.create_post(post=post_data)
            created_posts.append(post)
            print(f"Created post: {post.title}")

        # Create sample comments
        sample_comments = [
            (created_posts[0].id, CommentCreate(
                content="Great first post! Looking forward to more content.",
                author="Reader1"
            )),
            (created_posts[0].id, CommentCreate(
                content="Welcome! This looks like a promising blog.",
                author="Visitor"
            )),
            (created_posts[1].id, CommentCreate(
                content="FastAPI is indeed amazing! Thanks for the introduction.",
                author="Developer"
            )),
            (created_posts[1].id, CommentCreate(
                content="I've been using FastAPI for a year now. Highly recommended!",
                author="Senior Dev"
            )),
            (created_posts[2].id, CommentCreate(
                content="These SQLAlchemy tips are very helpful. Thank you!",
                author="Student"
            ))
        ]

        for post_id, comment_data in sample_comments:
            comment = comment_repository.create_comment(comment=comment_data, post_id=post_id)
            print(f"Created comment by {comment.author} on post {post_id}")

        print(f"\n✅ Successfully created {len(created_posts)} posts and {len(sample_comments)} comments")

    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        raise

def main():
    """Main function to initialize the database."""
    print("🗄️ Initializing Blog API Database")
    print("=" * 40)
    
    try:
        # Create tables
        print("Creating database tables...")
        create_tables()
        print("✅ Database tables created successfully")
        
        # Create sample data
        print("\nCreating sample data...")
        create_sample_data()
        
        print("\n🎉 Database initialization completed!")
        print("\nYou can now start the API server and test the endpoints.")
        print("Sample data includes:")
        print("- 3 blog posts")
        print("- 5 comments across the posts")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)

def reset_db():
    """Reset the database (drop and recreate all tables)."""
    print("⚠️ Resetting database (this will delete all data)...")
    reset_database()
    print("✅ Database reset completed")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_db()
    else:
        main()
