import pytest
from django.contrib.auth.models import User
from core.models import PetUser, Post


@pytest.fixture
def test_user(db):
    return PetUser.objects.create_user(
        username='testuser',
        password='testpass123',
        pet_name='Fluffy'
    )


@pytest.fixture
def test_post(test_user):
    return Post.objects.create(
        author=test_user,
        caption='Test post',
        image='posts/test.jpg'
    )