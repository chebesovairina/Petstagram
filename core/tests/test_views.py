from django.urls import reverse
import json


def test_feed_view(client, test_post):
    url = reverse('feed')
    response = client.get(url)
    assert response.status_code == 200
    assert test_post.caption.encode() in response.content  # Для байтов


def test_toggle_like(client, test_user, test_post):
    client.force_login(test_user)
    url = reverse('toggle_like', args=[test_post.id])

    response = client.post(url)
    data = json.loads(response.content)
    assert data['is_liked'] is True
    assert data['likes_count'] == 1

    response = client.post(url)
    data = json.loads(response.content)
    assert data['is_liked'] is False
    assert data['likes_count'] == 0