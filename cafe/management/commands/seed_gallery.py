import os

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from cafe.models import GalleryImage


class Command(BaseCommand):
    help = (
        "Upload gallery images to Cloudinary without creating duplicates "
        "or overwriting custom captions."
    )

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
            f for f in os.listdir(folder)
            if f.lower().endswith(valid_extensions)
        )

        if not files:
            self.stdout.write(
                self.style.WARNING("No gallery images found.")
            )
            return

        for order, filename in enumerate(files):

            filepath = os.path.join(folder, filename)

            relative_path = f"gallery/{filename}"

            default_caption = (
                os.path.splitext(filename)[0]
                .replace("_", " ")
                .replace("-", " ")
                .title()
            )

            # -------------------------------------------------
            # Find existing image by original filename
            # -------------------------------------------------

            image_obj = None

            for obj in GalleryImage.objects.all():
                existing_name = os.path.basename(obj.image.name)

                # Remove Cloudinary unique suffix before comparison
                base_existing = os.path.splitext(existing_name)[0].split("_")[0]
                base_current = os.path.splitext(filename)[0].split("_")[0]

                if base_existing == base_current:
                    image_obj = obj
                    break

            created = False

            if image_obj is None:
                image_obj = GalleryImage()
                created = True

            image_obj.order = order

            # Preserve custom caption
            if not image_obj.caption:
                image_obj.caption = default_caption

            # Upload only if image doesn't exist
            if created or not image_obj.image:

                with open(filepath, "rb") as image_file:
                    image_obj.image.save(
                        filename,
                        File(image_file),
                        save=False,
                    )

            image_obj.save()

            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"✓ Added {filename}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"↻ Exists {filename}")
                )

        self.stdout.write(
            self.style.SUCCESS(
                "\nGallery synced successfully!"
            )
        )