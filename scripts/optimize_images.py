#!/usr/bin/env python3
"""
Script pour optimiser les images (réduire la taille des fichiers).
Usage: python scripts/optimize_images.py docs/images/
"""

import sys
from pathlib import Path
from PIL import Image


def optimize_image(image_path: Path, max_width: int = 1600, quality: int = 85):
    """
    Optimise une image en réduisant sa taille et sa qualité.

    Args:
        image_path: Chemin vers l'image
        max_width: Largeur maximale (pixels)
        quality: Qualité JPEG/PNG (0-100)
    """
    try:
        with Image.open(image_path) as img:
            original_size = image_path.stat().st_size

            # Redimensionner si trop large
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                print(f"  Redimensionné: {img.width}x{img.height}")

            # Sauvegarder avec optimisation
            if image_path.suffix.lower() in ['.jpg', '.jpeg']:
                img.save(image_path, 'JPEG', quality=quality, optimize=True)
            elif image_path.suffix.lower() == '.png':
                img.save(image_path, 'PNG', optimize=True)

            new_size = image_path.stat().st_size
            reduction = ((original_size - new_size) / original_size) * 100

            print(f"  Taille: {original_size//1024} KB → {new_size//1024} KB (-{reduction:.1f}%)")

    except Exception as e:
        print(f"  ❌ Erreur: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/optimize_images.py <dossier>")
        print("Exemple: python scripts/optimize_images.py docs/images/")
        sys.exit(1)

    folder = Path(sys.argv[1])

    if not folder.exists():
        print(f"❌ Le dossier {folder} n'existe pas")
        sys.exit(1)

    # Trouver toutes les images
    image_extensions = ['.png', '.jpg', '.jpeg']
    images = []
    for ext in image_extensions:
        images.extend(folder.glob(f'*{ext}'))

    if not images:
        print(f"ℹ️  Aucune image trouvée dans {folder}")
        sys.exit(0)

    print(f"🖼️  Optimisation de {len(images)} image(s)...\n")

    for img_path in sorted(images):
        print(f"📸 {img_path.name}")
        optimize_image(img_path, max_width=1600, quality=85)

    print(f"\n✅ {len(images)} image(s) optimisée(s)")


if __name__ == "__main__":
    main()
