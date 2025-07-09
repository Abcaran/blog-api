"""
Unit tests for API routes.
"""
import unittest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from fastapi import status

from src.main import app
from src.models.db_models import Post, Comment


class TestPostRoutes(unittest.TestCase):
    """Test cases for Post API routes."""

    def setUp(self):
        """Set up test client."""
        self.client = TestClient(app)

    @patch('src.api.routes.post_repository')
    def test_create_post_success(self, mock_post_repo):
        """Test successful post creation."""
        mock_post = Mock(spec=Post)
        mock_post.id = 1
        mock_post.title = "Test Post"
        mock_post.content = "Test content"
        mock_post.author = "Test Author"
        mock_post.created_at = "2024-01-01T12:00:00"
        mock_post.updated_at = None
        mock_post.comments = []
        
        mock_post_repo.create_post.return_value = mock_post
        
        post_data = {
            "title": "Test Post",
            "content": "Test content",
            "author": "Test Author"
        }
        
        response = self.client.post("/posts", json=post_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_post_repo.create_post.assert_called_once()

    def test_create_post_invalid_data(self):
        """Test post creation with invalid data."""
        invalid_data = {
            "title": "",
            "content": "Valid content",
            "author": "Valid author"
        }
        
        response = self.client.post("/posts", json=invalid_data)
        
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)

    @patch('src.api.routes.comment_repository')
    @patch('src.api.routes.post_repository')
    def test_get_posts_success(self, mock_post_repo, mock_comment_repo):
        """Test successful retrieval of posts."""
        mock_post = Mock(spec=Post)
        mock_post.id = 1
        mock_post.title = "Test Post"
        mock_post.content = "Test content"
        mock_post.author = "Test Author"
        mock_post.created_at = "2024-01-01T12:00:00"
        mock_post.updated_at = None
        
        mock_post_repo.get_posts.return_value = [mock_post]
        mock_comment_repo.get_comments_count_for_post.return_value = 2
        
        response = self.client.get("/posts")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertIsInstance(data, list)
        if data:
            self.assertIn("content", data[0])
            self.assertIn("comment_count", data[0])

    @patch('src.api.routes.post_repository')
    def test_get_post_success(self, mock_post_repo):
        """Test successful retrieval of a specific post."""
        mock_post = Mock(spec=Post)
        mock_post.id = 1
        mock_post.title = "Test Post"
        mock_post.content = "Test content"
        mock_post.author = "Test Author"
        mock_post.created_at = "2024-01-01T12:00:00"
        mock_post.updated_at = None
        mock_post.comments = []
        
        mock_post_repo.get_post.return_value = mock_post
        
        response = self.client.get("/posts/1")
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_post_repo.get_post.assert_called_once_with(post_id=1)

    @patch('src.api.routes.post_repository')
    def test_get_post_not_found(self, mock_post_repo):
        """Test retrieval of non-existent post."""
        mock_post_repo.get_post.return_value = None
        
        response = self.client.get("/posts/999")
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch('src.api.routes.post_repository')
    def test_update_post_success(self, mock_post_repo):
        """Test successful post update."""
        mock_post = Mock(spec=Post)
        mock_post.id = 1
        mock_post.title = "Updated Post"
        mock_post.content = "Updated content"
        mock_post.author = "Test Author"
        mock_post.comments = []
        
        mock_post_repo.update_post.return_value = mock_post
        
        update_data = {
            "title": "Updated Post",
            "content": "Updated content"
        }
        
        response = self.client.put("/posts/1", json=update_data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_post_repo.update_post.assert_called_once()

    @patch('src.api.routes.post_repository')
    def test_delete_post_success(self, mock_post_repo):
        """Test successful post deletion."""
        mock_post_repo.delete_post.return_value = True
        
        response = self.client.delete("/posts/1")
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        mock_post_repo.delete_post.assert_called_once_with(post_id=1)

    @patch('src.api.routes.post_repository')
    def test_delete_post_not_found(self, mock_post_repo):
        """Test deletion of non-existent post."""
        mock_post_repo.delete_post.return_value = False
        
        response = self.client.delete("/posts/999")
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestCommentRoutes(unittest.TestCase):
    """Test cases for Comment API routes."""

    def setUp(self):
        """Set up test client."""
        self.client = TestClient(app)

    @patch('src.api.routes.comment_repository')
    @patch('src.api.routes.post_repository')
    def test_create_comment_success(self, mock_post_repo, mock_comment_repo):
        """Test successful comment creation."""
        mock_post = Mock(spec=Post)
        mock_post_repo.get_post.return_value = mock_post
        
        mock_comment = Mock(spec=Comment)
        mock_comment.id = 1
        mock_comment.content = "Test comment"
        mock_comment.author = "Test Author"
        mock_comment.post_id = 1
        mock_comment.created_at = "2024-01-01T12:00:00"
        mock_comment.updated_at = None
        
        mock_comment_repo.create_comment.return_value = mock_comment
        
        comment_data = {
            "content": "Test comment",
            "author": "Test Author"
        }
        
        response = self.client.post("/posts/1/comments", json=comment_data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_comment_repo.create_comment.assert_called_once()

    @patch('src.api.routes.post_repository')
    def test_create_comment_post_not_found(self, mock_post_repo):
        """Test comment creation for non-existent post."""
        mock_post_repo.get_post.return_value = None
        
        comment_data = {
            "content": "Test comment",
            "author": "Test Author"
        }
        
        response = self.client.post("/posts/999/comments", json=comment_data)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_comment_invalid_data(self):
        """Test comment creation with invalid data."""
        invalid_data = {
            "content": "",
            "author": "Valid author"
        }
        
        response = self.client.post("/posts/1/comments", json=invalid_data)
        
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)


class TestPaginationAndValidation(unittest.TestCase):
    """Test cases for pagination and validation."""

    def setUp(self):
        """Set up test client."""
        self.client = TestClient(app)

    def test_get_posts_invalid_pagination(self):
        """Test posts endpoint with invalid pagination parameters."""
        response = self.client.get("/posts?skip=-1&limit=10")
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        response = self.client.get("/posts?skip=0&limit=0")
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        response = self.client.get("/posts?skip=0&limit=101")
        self.assertEqual(response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY)


if __name__ == '__main__':
    unittest.main()
