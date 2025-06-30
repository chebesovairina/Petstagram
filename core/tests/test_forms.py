import pytest
from core.forms import PetUserCreationForm
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.mark.django_db
def test_valid_registration_form():
    from PIL import Image
    from io import BytesIO

    image = Image.new('RGB', (20, 20), color='red')
    image_file = BytesIO()
    image.save(image_file, 'JPEG')
    image_file.seek(0)

    test_image = SimpleUploadedFile(
        "test_avatar.jpg",
        image_file.read(),
        content_type="image/jpeg"
    )

    form_data = {
        'username': 'petlover42',
        'email': 'pet@example.com',
        'pet_name': 'Барсик',
        'pet_type': 'cat',
        'bio': 'Люблю корм и спать',
        'password1': 'SecurePass123!',
        'password2': 'SecurePass123!'
    }

    form = PetUserCreationForm(
        data=form_data,
        files={'avatar': test_image}
    )

    assert form.is_valid(), f"Ошибки: {form.errors}"


@pytest.mark.django_db
def test_form_without_required_fields():
    form_data = {
        'username': '',
        'email': '',
        'pet_name': '',
        'pet_type': '',
        'password1': '123',
        'password2': '123'
    }

    form = PetUserCreationForm(data=form_data)

    assert not form.is_valid()
    required_errors = {
        'username': 'This field is required.',
        'email': 'This field is required.',
        'pet_name': 'This field is required.',
        'pet_type': 'This field is required.'
    }

    for field, error in required_errors.items():
        assert field in form.errors
        assert error in str(form.errors[field])


@pytest.mark.django_db
def test_password_mismatch():
    form_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'pet_name': 'Шарик',
        'pet_type': 'dog',
        'password1': 'GoodPass123',
        'password2': 'DifferentPass123'
    }

    form = PetUserCreationForm(data=form_data)

    assert not form.is_valid()
    assert 'password2' in form.errors
    assert "The two password fields didn’t match." in str(form.errors)


@pytest.mark.django_db
def test_invalid_avatar_format():
    invalid_file = SimpleUploadedFile(
        "test.gif",
        b"file_content",
        content_type="image/gif"
    )

    form_data = {
        'username': 'user123',
        'email': 'user@example.com',
        'pet_name': 'Рекс',
        'pet_type': 'dog',
        'password1': 'GoodPass123!',
        'password2': 'GoodPass123!'
    }

    form = PetUserCreationForm(
        data=form_data,
        files={'avatar': invalid_file}
    )

    assert not form.is_valid()
    assert 'avatar' in form.errors
    assert "Upload a valid image." in str(form.errors['avatar'])
