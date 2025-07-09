import unittest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from src.repositories.repository import PostRepository, CommentRepository
from src.models.pydantic_models import PostCreate, PostUpdate, CommentCreate
from src.models.db_models import Post, Comment


class TestPostRepository(unittest.TestCase):
    """Test cases for PostRepository."""

    def setUp(self):
        """Set up test fixtures."""
        self.repository = PostRepository()

    @patch('src.repositories.repository.SessionLocal')
    def test_create_post(self, mock_session_local):
        """Test creating a post through repository."""
        mock_session = Mock(spec=Session)
        mock_session_local.return_value = mock_session
        
        post_data = PostCreate(
            title="Test Post",
            content="Test content",
            author="Test Author"
        )
        
        mock_db_post = Mock(spec=Post)
        mock_db_post.id = 1
        mock_db_post.title = "Test Post"
        mock_db_post.content = "Test content"
        mock_db_post.author = "Test Author"
        mock_db_post.comments = []
        
        self.repository.create_post(post_data)
        
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
        mock_session.close.assert_called_once()

    @patch('src.repositories.repository.SessionLocal')
    def test_get_post(self, mock_session_local):
        """Test getting a post by ID."""
        mock_session = Mock(spec=Session)
        mock_session_local.return_value = mock_session
        
        mock_post = Mock(spec=Post)
        mock_post.id = 1
        mock_post.title = "Test Post"
        mock_session.query.return_value.options.return_value.filter.return_value.first.return_value = mock_post
        
        result = self.repository.get_post(1)
        
        mock_session.query.assert_called_once()
        mock_session.close.assert_called_once()
        self.assertEqual(result, mock_post)

    @patch('src.repositories.repository.SessionLocal')
    def test_get_post_not_found(self, mock_session_local):
        """Test getting a non-existent post."""
        mock_session = Mock(spec=Session)
        mock_session_local.return_value = mock_session
        
        mock_session.query.return_value.options.return_value.filter.return_value.first.return_value = None
        
        result = self.repository.get_post(999)
        
        self.assertIsNone(result)
        mock_session.close.assert_called_once()

    @patch('src.repositories.repository.SessionLocal')
    def test_get_posts(self, mock_session_local):
        """Test getting multiple posts with pagination."""
        mock_session = Mock(spec=Session)
        mock_session_local.return_value = mock_session
        
        mock_posts = [Mock(spec=Post), Mock(spec=Post)]
        mock_session.query.return_value.offset.return_value.limit.return_value.all.return_value = mock_posts
        
        result = self.repository.get_posts(skip=0, limit=10)
        
        mock_session.query.return_value.offset.assert_called_once_with(0)
        mock_session.query.return_value.offset.return_value.limit.assert_called_once_with(10)
        mock_session.close.assert_called_once()
        self.assertEqual(result, mock_posts)

    @patch('src.repositories.repository.SessionLocal')
    def test_update_post(self, mock_session_local):
        """Test updating a post."""
        mock_session = Mock(spec=Session)
        mock_session_local.return_value = mock_session
        
        mock_post = Mock(spec=Post)
        mock_post.id = 1
        mock_post.comments = []
        mock_session.query.return_value.options.return_value.filter.return_value.first.return_value = mock_post
        
        update_data = PostUpdate(title="Updated Title")
        
        result = self.repository.update_post(1, update_data)
        
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
        mock_session.close.assert_called_once()
        self.assertEqual(result, mock_post)

    @patch('src.repositories.repository.SessionLocal')
    def test_delete_post(self, mock_session_local):
        """Test deleting a post."""
        mock_session = Mock(spec=Session)
        mock_session_local.return_value = mock_session
        
        mock_post = Mock(spec=Post)
        mock_session.query.return_value.filter.return_value.first.return_value = mock_post
        
        result = self.repository.delete_post(1)
        
        mock_session.delete.assert_called_once_with(mock_post)
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()
        self.assertTrue(result)

    @patch('src.repositories.repository.SessionLocal')
    def test_delete_post_not_found(self, mock_session_local):
        """Test deleting a non-existent post."""
        mock_session = Mock(spec=Session)
        mock_session_local.return_value = mock_session
        
        mock_session.query.return_value.filter.return_value.first.return_value = None
        
        result = self.repository.delete_post(999)
        
        self.assertFalse(result)
        mock_session.delete.assert_not_called()
        mock_session.close.assert_called_once()


class TestCommentRepository(unittest.TestCase):
    """Test cases for CommentRepository."""

    def setUp(self):
        """Set up test fixtures."""
        self.repository = CommentRepository()

    @patch('src.repositories.repository.SessionLocal')
    def test_create_comment(self, mock_session_local):
        """Test creating a comment through repository."""
        mock_session = Mock(spec=Session)
        mock_session_local.return_value = mock_session

        comment_data = CommentCreate(
            content="Test comment",
            author="Test Author"
        )
        
        self.repository.create_comment(comment_data, post_id=1)
        
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
        mock_session.close.assert_called_once()

    @patch('src.repositories.repository.SessionLocal')
    def test_get_comments_for_post(self, mock_session_local):
        """Test getting comments for a specific post."""
        mock_session = Mock(spec=Session)
        mock_session_local.return_value = mock_session
        
        mock_comments = [Mock(spec=Comment), Mock(spec=Comment)]
        mock_session.query.return_value.filter.return_value.all.return_value = mock_comments
        
        result = self.repository.get_comments_for_post(1)
        
        mock_session.query.assert_called_once()
        mock_session.close.assert_called_once()
        self.assertEqual(result, mock_comments)

    @patch('src.repositories.repository.SessionLocal')
    def test_get_comments_count_for_post(self, mock_session_local):
        """Test getting comment count for a post."""
        mock_session = Mock(spec=Session)
        mock_session_local.return_value = mock_session
        
        mock_session.query.return_value.filter.return_value.count.return_value = 5
        
        result = self.repository.get_comments_count_for_post(1)
        
        self.assertEqual(result, 5)
        mock_session.close.assert_called_once()


if __name__ == '__main__':
    unittest.main()
