from django.core.management.base import BaseCommand
from blog.models import Post
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from django.core.files import File
import os

class Command(BaseCommand):
    help = "Insert default blog posts with images"

    def handle(self, *args, **kwargs):

        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        media_path = os.path.join(base_dir, "media", "blog_thumbnails")

        posts = [
            ("Introduction to Python", "python.png"),
            ("Django vs Flask", "django.png"),
            ("What is API?", "api.png"),
        ]

        user, _ = User.objects.get_or_create(username="admin")
        user.set_password("admin123")
        user.is_staff = True
        user.is_superuser = True
        user.save()

        for title, image_name in posts:

            image_full_path = os.path.join(media_path, image_name)

            post, created = Post.objects.get_or_create(
                slug=slugify(title),
                defaults={
                    "title": title,
                    "author": user,
                    "content": "Auto generated post",
                    "timeStamp": timezone.now(),
                }
            )

            if created and os.path.exists(image_full_path):
                with open(image_full_path, "rb") as img:
                    post.thumbnail.save(image_name, File(img), save=True)

        self.stdout.write(self.style.SUCCESS("Posts inserted successfully with images"))
