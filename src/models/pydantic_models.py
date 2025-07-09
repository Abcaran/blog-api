from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class CommentBase(BaseModel):
    """Base schema for comments."""
    content: str = Field(..., min_length=1, max_length=1000, description="Comment content")
    author: str = Field(..., min_length=1, max_length=100, description="Comment author name")


class CommentCreate(CommentBase):
    """Schema for creating a new comment."""
    pass


class CommentUpdate(BaseModel):
    """Schema for updating a comment."""
    content: Optional[str] = Field(None, min_length=1, max_length=1000, description="Comment content")
    author: Optional[str] = Field(None, min_length=1, max_length=100, description="Comment author name")


class CommentResponse(CommentBase):
    """Schema for comment response."""
    id: int
    post_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    """Base schema for posts."""
    title: str = Field(..., min_length=1, max_length=200, description="Post title")
    content: str = Field(..., min_length=1, description="Post content")
    author: str = Field(..., min_length=1, max_length=100, description="Post author name")


class PostCreate(PostBase):
    """Schema for creating a new Post."""
    pass


class PostUpdate(BaseModel):
    """Schema for updating a Post."""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Post title")
    content: Optional[str] = Field(None, min_length=1, description="Post content")
    author: Optional[str] = Field(None, min_length=1, max_length=100, description="Post author name")


class PostResponse(PostBase):
    """Schema for Post response."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    comments: List[CommentResponse] = Field(default_factory=list, description="Comments associated with this post")

    class Config:
        from_attributes = True


class PostSummary(BaseModel):
    """Schema for blog post summary (without content and comments for compact list views)."""
    id: int
    title: str
    author: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    comment_count: int = Field(default=0, description="Number of comments on this post")

    class Config:
        from_attributes = True


class PostListItem(BaseModel):
    """Schema for blog post list item (includes content but not comments)."""
    id: int
    title: str
    content: str
    author: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    comment_count: int = Field(default=0, description="Number of comments on this post")

    class Config:
        from_attributes = True


class PaginationResponse(BaseModel):
    """Schema for paginated responses."""
    items: List[PostSummary]
    total: int
    page: int
    size: int
    pages: int


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
