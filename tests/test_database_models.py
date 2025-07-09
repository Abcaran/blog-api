"""
Unit tests for SQLAlchemy database models.
"""
import unittest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.database import Base
from src.models.db_models import Post, Comment


class TestDatabaseModels(unittest.TestCase):
    """Test cases for SQLAlchemy database models."""

    @classmethod
    def setUpClass(cls):
        """Set up test database."""
        # Use in-memory SQLite database for testing
        cls.engine = create_engine("sqlite:///:memory:", echo=False)
        Base.metadata.create_all(cls.engine)
        cls.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)

    def setUp(self):
        """Set up test session for each test."""
        self.session = self.SessionLocal()

    def tearDown(self):
        """Clean up after each test."""
        self.session.rollback()
        self.session.close()

    def test_post_creation(self):
        """Test creating a Post model."""
        post = Post(
            title="Test Post",
            content="This is test content",
            author="Test Author"
        )
        
        self.session.add(post)
        self.session.commit()
        
        # Verify the post was created
        self.assertIsNotNone(post.id)
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.content, "This is test content")
        self.assertEqual(post.author, "Test Author")
        self.assertIsNotNone(post.created_at)

    def test_comment_creation(self):
        """Test creating a Comment model."""
        post = Post(
            title="Test Post",
            content="Test content",
            author="Test Author"
        )
        self.session.add(post)
        self.session.commit()
        
        comment = Comment(
            content="This is a test comment",
            author="Comment Author",
            post_id=post.id
        )
        
        self.session.add(comment)
        self.session.commit()
        
        self.assertIsNotNone(comment.id)
        self.assertEqual(comment.content, "This is a test comment")
        self.assertEqual(comment.author, "Comment Author")
        self.assertEqual(comment.post_id, post.id)

    def test_post_comment_relationship(self):
        """Test the relationship between Post and Comment models."""
        post = Post(
            title="Test Post",
            content="Test content",
            author="Test Author"
        )
        self.session.add(post)
        self.session.commit()
        
        comment1 = Comment(
            content="First comment",
            author="Author 1",
            post_id=post.id
        )
        comment2 = Comment(
            content="Second comment",
            author="Author 2",
            post_id=post.id
        )
        
        self.session.add_all([comment1, comment2])
        self.session.commit()
        
        self.assertEqual(len(post.comments), 2)
        self.assertEqual(comment1.post, post)
        self.assertEqual(comment2.post, post)

    def test_cascade_delete(self):
        """Test that deleting a post deletes its comments (cascade)."""
        post = Post(
            title="Test Post",
            content="Test content",
            author="Test Author"
        )
        self.session.add(post)
        self.session.commit()
        
        comment = Comment(
            content="Test comment",
            author="Comment Author",
            post_id=post.id
        )
        self.session.add(comment)
        self.session.commit()
        
        self.assertEqual(self.session.query(Post).count(), 1)
        self.assertEqual(self.session.query(Comment).count(), 1)
        
        self.session.delete(post)
        self.session.commit()
        
        self.assertEqual(self.session.query(Post).count(), 0)
        self.assertEqual(self.session.query(Comment).count(), 0)


if __name__ == '__main__':
    unittest.main()
