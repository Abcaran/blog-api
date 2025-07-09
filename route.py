from fastapi import APIRouter, HTTPException, status, Query
from typing import List
from model import (
    PostCreate,
    PostUpdate,
    PostResponse,
    PostSummary,
    CommentCreate,
    CommentUpdate,
    CommentResponse,
)
from repository import post_repository, comment_repository

router = APIRouter()


@router.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED, tags=["posts"])
async def create_post(post: PostCreate):
    """Create a new post."""
    db_post = post_repository.create_post(post=post)
    return db_post


@router.get("/posts", response_model=List[PostSummary], tags=["posts"])
async def get_posts(
    skip: int = Query(0, ge=0, description="Number of posts to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of posts to return")
):
    """Get all posts with pagination."""
    posts = post_repository.get_posts(skip=skip, limit=limit)

    posts_summary = []
    for post in posts:
        comment_count = comment_repository.get_comments_count_for_post(post.id)
        summary = PostSummary(
            id=post.id,
            title=post.title,
            author=post.author,
            created_at=post.created_at,
            updated_at=post.updated_at,
            comment_count=comment_count
        )
        posts_summary.append(summary)

    return posts_summary


@router.get("/posts/{post_id}", response_model=PostResponse, tags=["posts"])
async def get_post(post_id: int):
    """Get a specific post by ID with all its comments."""
    db_post = post_repository.get_post(post_id=post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return db_post


@router.put("/posts/{post_id}", response_model=PostResponse, tags=["posts"])
async def update_post(post_id: int, post_update: PostUpdate):
    """Update a post."""
    db_post = post_repository.update_post(post_id=post_id, post_update=post_update)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return db_post


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["posts"])
async def delete_post(post_id: int):
    """Delete a post and all its comments."""
    success = post_repository.delete_post(post_id=post_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )


@router.post("/posts/{post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED, tags=["comments"])
async def create_comment(post_id: int, comment: CommentCreate):
    """Create a new comment for a post."""
    db_post = post_repository.get_post(post_id=post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    db_comment = comment_repository.create_comment(comment=comment, post_id=post_id)
    return db_comment


@router.get("/posts/{post_id}/comments", response_model=List[CommentResponse], tags=["comments"])
async def get_comments_for_post(post_id: int):
    """Get all comments for a specific post."""
    # Check if post exists
    db_post = post_repository.get_post(post_id=post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    comments = comment_repository.get_comments_for_post(post_id=post_id)
    return comments


@router.get("/comments/{comment_id}", response_model=CommentResponse, tags=["comments"])
async def get_comment(comment_id: int):
    """Get a specific comment by ID."""
    db_comment = comment_repository.get_comment(comment_id=comment_id)
    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    return db_comment


@router.put("/comments/{comment_id}", response_model=CommentResponse, tags=["comments"])
async def update_comment(comment_id: int, comment_update: CommentUpdate):
    """Update a comment."""
    db_comment = comment_repository.update_comment(comment_id=comment_id, comment_update=comment_update)
    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )

    return db_comment


@router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["comments"])
async def delete_comment(comment_id: int):
    """Delete a comment."""
    success = comment_repository.delete_comment(comment_id=comment_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found"
        )
