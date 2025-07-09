from typing import List, Optional
from database import SessionLocal
from db_models import Post, Comment
from model import PostCreate, PostUpdate, CommentCreate, CommentUpdate


class PostRepository:
    """Repository for Post operations with internal session management."""

    def create_post(self, post: PostCreate) -> Post:
        """Create a new post."""
        db = SessionLocal()
        try:
            db_post = Post(
                title=post.title,
                content=post.content,
                author=post.author
            )
            db.add(db_post)
            db.commit()
            db.refresh(db_post)
            return db_post
        finally:
            db.close()

    def get_post(self, post_id: int) -> Optional[Post]:
        """Get a post by ID."""
        db = SessionLocal()
        try:
            return db.query(Post).filter(Post.id == post_id).first()
        finally:
            db.close()

    def get_posts(self, skip: int = 0, limit: int = 10) -> List[Post]:
        """Get multiple posts with pagination."""
        db = SessionLocal()
        try:
            return db.query(Post).offset(skip).limit(limit).all()
        finally:
            db.close()

    def update_post(self, post_id: int, post_update: PostUpdate) -> Optional[Post]:
        """Update a post."""
        db = SessionLocal()
        try:
            db_post = db.query(Post).filter(Post.id == post_id).first()
            if not db_post:
                return None

            update_data = post_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_post, field, value)

            db.commit()
            db.refresh(db_post)
            return db_post
        finally:
            db.close()

    def delete_post(self, post_id: int) -> bool:
        """Delete a post."""
        db = SessionLocal()
        try:
            db_post = db.query(Post).filter(Post.id == post_id).first()
            if not db_post:
                return False

            db.delete(db_post)
            db.commit()
            return True
        finally:
            db.close()

    def get_posts_count(self) -> int:
        """Get total count of posts."""
        db = SessionLocal()
        try:
            return db.query(Post).count()
        finally:
            db.close()


class CommentRepository:
    """Repository for Comment operations with internal session management."""

    def create_comment(self, comment: CommentCreate, post_id: int) -> Comment:
        """Create a new comment for a post."""
        db = SessionLocal()
        try:
            db_comment = Comment(
                content=comment.content,
                author=comment.author,
                post_id=post_id
            )
            db.add(db_comment)
            db.commit()
            db.refresh(db_comment)
            return db_comment
        finally:
            db.close()

    def get_comment(self, comment_id: int) -> Optional[Comment]:
        """Get a comment by ID."""
        db = SessionLocal()
        try:
            return db.query(Comment).filter(Comment.id == comment_id).first()
        finally:
            db.close()

    def get_comments_for_post(self, post_id: int) -> List[Comment]:
        """Get all comments for a specific post."""
        db = SessionLocal()
        try:
            return db.query(Comment).filter(Comment.post_id == post_id).all()
        finally:
            db.close()

    def update_comment(self, comment_id: int, comment_update: CommentUpdate) -> Optional[Comment]:
        """Update a comment."""
        db = SessionLocal()
        try:
            db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
            if not db_comment:
                return None

            update_data = comment_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_comment, field, value)

            db.commit()
            db.refresh(db_comment)
            return db_comment
        finally:
            db.close()

    def delete_comment(self, comment_id: int) -> bool:
        """Delete a comment."""
        db = SessionLocal()
        try:
            db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
            if not db_comment:
                return False

            db.delete(db_comment)
            db.commit()
            return True
        finally:
            db.close()

    def get_comments_count_for_post(self, post_id: int) -> int:
        """Get count of comments for a specific blog post."""
        db = SessionLocal()
        try:
            return db.query(Comment).filter(Comment.post_id == post_id).count()
        finally:
            db.close()


post_repository = PostRepository()
comment_repository = CommentRepository()
