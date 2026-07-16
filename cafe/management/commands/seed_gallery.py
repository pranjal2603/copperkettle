import os
from django.core.management.base import BaseCommand
from django.conf import settings
from cafe.models import GalleryImage


class Command(BaseCommand):
    help = (
        "Registers image files that already exist in MEDIA_ROOT/gallery/ as "
        "GalleryImage records, without copying or duplicating the files."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--folder",
            type=str,
            default=str(settings.MEDIA_ROOT / "gallery"),
            help="Path to the folder containing already-uploaded images (default: MEDIA_ROOT/gallery).",
        )

    def handle(self, *args, **options):
        folder = options["folder"]

        if not os.path.isdir(folder):
            self.stderr.write(self.style.ERROR(f"Folder not found: {folder}"))
            return

        valid_extensions = (".jpg", ".jpeg", ".png", ".webp")
        files = sorted(
            f for f in os.listdir(folder)
            if f.lower().endswith(valid_extensions)
        )

        if not files:
            self.stdout.write(self.style.WARNING(f"No image files found in {folder}"))
            return

        created_count = 0

        for index, filename in enumerate(files):
            relative_path = f"gallery/{filename}"

            # Skip if this file is already registered in the DB
            if GalleryImage.objects.filter(image=relative_path).exists():
                self.stdout.write(f"Skipped (already registered): {filename}")
                continue

            caption = os.path.splitext(filename)[0].replace("_", " ").replace("-", " ").title()

            gallery_image = GalleryImage(caption=caption, order=index)
            gallery_image.image.name = relative_path  # point at existing file, no copy
            gallery_image.save()

            created_count += 1
            self.stdout.write(f"Registered: {filename} -> caption: '{caption}'")

        self.stdout.write(self.style.SUCCESS(f"Done. {created_count} new image(s) registered."))