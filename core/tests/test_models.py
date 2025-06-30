import pytest
from core.models import Post, Like, Comment, PetUser


def test_post_creation(db):
    user = PetUser.objects.create(username='test', password='test')
    post = Post.objects.create(author=user, caption='Test')
    assert post.caption == 'Test'


def test_like_creation(test_post, test_user):
    like = Like.objects.create(post=test_post, user=test_user)
    assert test_post.like_count == 1
    assert like in test_post.likes.all()


def test_str_methods(test_post):
    assert str(test_post) == f"Post by {test_post.author.pet_name}"