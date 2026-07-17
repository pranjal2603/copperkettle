import os

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from cafe.models import GalleryImage


class Command(BaseCommand):
    help = "Upload gallery images to Cloudinary and create/update GalleryImage records."

    def add_arguments(self, parser):
        parser.add_argument(
            "--folder",
            type=str,
            default=str(settings.MEDIA_ROOT / "gallery"),
            help="Folder containing gallery images.",
        )

    def handle(self, *args, **options):

        folder = options["folder"]

        if not os.path.isdir(folder):
            self.stderr.write(
                self.style.ERROR(f"Folder not found: {folder}")
            )
            return

        valid_extensions = (
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
            ".avif",
        )

        files = sorted(
            f
            for f in os.listdir(folder)
            if f.lower().endswith(valid_extensions)
        )

        if not files:
            self.stdout.write(
                self.style.WARNING("No gallery images found.")
            )
            return

        for index, filename in enumerate(files):

            filepath = os.path.join(folder, filename)

            caption = (
                os.path.splitext(filename)[0]
                .replace("_", " ")
                .replace("-", " ")
                .title()
            )

            image_obj, created = GalleryImage.objects.get_or_create(
                caption=caption,
                defaults={
                    "order": index,
                },
            )

            image_obj.order = index

            with open(filepath, "rb") as image_file:
                image_obj.image.save(
                    filename,
                    File(image_file),
                    save=False,
                )

            image_obj.save()

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✓ Uploaded {filename}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"↻ Updated {filename}"
                    )
                )
        self.stdout.write(
            self.style.SUCCESS(
                "\nGallery uploaded successfully to Cloudinary!"
            )
        )