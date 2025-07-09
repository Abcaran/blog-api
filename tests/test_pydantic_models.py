"""
Unit tests for Pydantic models.
"""
import unittest
from datetime import datetime
from pydantic import ValidationError

from src.models.pydantic_models import (
    PostCreate,
    PostUpdate,
    PostResponse,
    PostListItem,
    PostSummary,
    CommentCreate,
    CommentUpdate,
    CommentResponse,
    ErrorResponse
)


class TestPostModels(unittest.TestCase):
    """Test cases for Post-related Pydantic models."""

    def test_post_create_valid(self):
        """Test creating a valid PostCreate model."""
        post = PostCreate(
            title="Test Post",
            content="This is test content",
            author="Test Author"
        )
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.content, "This is test content")
        self.assertEqual(post.author, "Test Author")

    def test_post_create_empty_title(self):
        """Test PostCreate with empty title should fail."""
        with self.assertRaises(ValidationError) as context:
            PostCreate(
                title="",
                content="Valid content",
                author="Test Author"
            )
        self.assertIn("at least 1 character", str(context.exception))

    def test_post_create_empty_content(self):
        """Test PostCreate with empty content should fail."""
        with self.assertRaises(ValidationError):
            PostCreate(
                title="Valid Title",
                content="",
                author="Test Author"
            )

    def test_post_create_empty_author(self):
        """Test PostCreate with empty author should fail."""
        with self.assertRaises(ValidationError):
            PostCreate(
                title="Valid Title",
                content="Valid content",
                author=""
            )

    def test_post_create_long_title(self):
        """Test PostCreate with title too long should fail."""
        long_title = "x" * 201  # Max is 200
        with self.assertRaises(ValidationError):
            PostCreate(
                title=long_title,
                content="Valid content",
                author="Test Author"
            )

    def test_post_update_partial(self):
        """Test PostUpdate with partial data."""
        post_update = PostUpdate(title="Updated Title")
        self.assertEqual(post_update.title, "Updated Title")
        self.assertIsNone(post_update.content)
        self.assertIsNone(post_update.author)

    def test_post_update_empty_fields(self):
        """Test PostUpdate with empty fields should fail."""
        with self.assertRaises(ValidationError):
            PostUpdate(title="")

    def test_post_response_model(self):
        """Test PostResponse model structure."""
        now = datetime.now()
        post_data = {
            "id": 1,
            "title": "Test Post",
            "content": "Test content",
            "author": "Test Author",
            "created_at": now,
            "updated_at": None,
            "comments": []
        }
        post = PostResponse(**post_data)
        self.assertEqual(post.id, 1)
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.comments, [])

    def test_post_list_item_model(self):
        """Test PostListItem model structure."""
        now = datetime.now()
        post_data = {
            "id": 1,
            "title": "Test Post",
            "content": "Test content",
            "author": "Test Author",
            "created_at": now,
            "updated_at": None,
            "comment_count": 5
        }
        post = PostListItem(**post_data)
        self.assertEqual(post.id, 1)
        self.assertEqual(post.content, "Test content")
        self.assertEqual(post.comment_count, 5)

    def test_post_summary_model(self):
        """Test PostSummary model structure."""
        now = datetime.now()
        post_data = {
            "id": 1,
            "title": "Test Post",
            "author": "Test Author",
            "created_at": now,
            "updated_at": None,
            "comment_count": 3
        }
        post = PostSummary(**post_data)
        self.assertEqual(post.id, 1)
        self.assertEqual(post.comment_count, 3)
        # PostSummary should not have content field
        self.assertFalse(hasattr(post, 'content'))


class TestCommentModels(unittest.TestCase):
    """Test cases for Comment-related Pydantic models."""

    def test_comment_create_valid(self):
        """Test creating a valid CommentCreate model."""
        comment = CommentCreate(
            content="This is a test comment",
            author="Test Author"
        )
        self.assertEqual(comment.content, "This is a test comment")
        self.assertEqual(comment.author, "Test Author")

    def test_comment_create_empty_content(self):
        """Test CommentCreate with empty content should fail."""
        with self.assertRaises(ValidationError):
            CommentCreate(
                content="",
                author="Test Author"
            )

    def test_comment_create_empty_author(self):
        """Test CommentCreate with empty author should fail."""
        with self.assertRaises(ValidationError):
            CommentCreate(
                content="Valid content",
                author=""
            )

    def test_comment_create_long_content(self):
        """Test CommentCreate with content too long should fail."""
        long_content = "x" * 1001  # Max is 1000
        with self.assertRaises(ValidationError):
            CommentCreate(
                content=long_content,
                author="Test Author"
            )

    def test_comment_update_partial(self):
        """Test CommentUpdate with partial data."""
        comment_update = CommentUpdate(content="Updated content")
        self.assertEqual(comment_update.content, "Updated content")
        self.assertIsNone(comment_update.author)

    def test_comment_response_model(self):
        """Test CommentResponse model structure."""
        now = datetime.now()
        comment_data = {
            "id": 1,
            "content": "Test comment",
            "author": "Test Author",
            "post_id": 1,
            "created_at": now,
            "updated_at": None
        }
        comment = CommentResponse(**comment_data)
        self.assertEqual(comment.id, 1)
        self.assertEqual(comment.post_id, 1)
        self.assertEqual(comment.content, "Test comment")


class TestErrorResponse(unittest.TestCase):
    """Test cases for ErrorResponse model."""

    def test_error_response_basic(self):
        """Test basic ErrorResponse model."""
        error = ErrorResponse(detail="Test error message")
        self.assertEqual(error.detail, "Test error message")
        self.assertIsNone(error.error_code)
        self.assertIsInstance(error.timestamp, datetime)

    def test_error_response_with_code(self):
        """Test ErrorResponse with error code."""
        error = ErrorResponse(
            detail="Test error message",
            error_code="TEST_ERROR"
        )
        self.assertEqual(error.detail, "Test error message")
        self.assertEqual(error.error_code, "TEST_ERROR")


class TestModelSerialization(unittest.TestCase):
    """Test model serialization and deserialization."""

    def test_post_create_json_serialization(self):
        """Test PostCreate JSON serialization."""
        post = PostCreate(
            title="Test Post",
            content="Test content",
            author="Test Author"
        )
        
        json_data = post.model_dump()
        expected = {
            "title": "Test Post",
            "content": "Test content",
            "author": "Test Author"
        }
        
        self.assertEqual(json_data, expected)

    def test_comment_create_json_serialization(self):
        """Test CommentCreate JSON serialization."""
        comment = CommentCreate(
            content="Test comment",
            author="Test Author"
        )
        
        json_data = comment.model_dump()
        expected = {
            "content": "Test comment",
            "author": "Test Author"
        }
        
        self.assertEqual(json_data, expected)


if __name__ == '__main__':
    unittest.main()
