import os
import django
from django.core.management.base import BaseCommand

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'petstagram.settings')  # Замени `your_project` на имя своего проекта
django.setup()

from core.models import Comment  # Замени `your_app` на имя приложения, где есть модель Comment


def delete_all_comments():
    """Удаляет все комментарии с подтверждением."""
    total = Comment.objects.count()

    print(f"🔍 Найдено комментариев: {total}")
    if total == 0:
        print("✅ Нет комментариев для удаления.")
        return

    confirm = input(f"❌ Вы уверены, что хотите удалить ВСЕ {total} комментариев? (yes/no): ")
    if confirm.lower() != "yes":
        print("❌ Удаление отменено.")
        return

    print("⏳ Удаление...")
    Comment.objects.all().delete()

    print(f"✅ Удалено {total} комментариев!")


if __name__ == "__main__":
    delete_all_comments()