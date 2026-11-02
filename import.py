import os
import re
from datetime import datetime
from calibre.library import db
from calibre.ebooks.metadata.meta import get_metadata
from calibre.utils.date import now

# 📁 Dossier à scanner
import_folder = '/mnt/Livres'

# 📦 Chemin de la bibliothèque calibre
LIBRARY_PATH = "/config/Bibliothèque calibre"

# 📄 Fichier de suivi des chemins déjà importés
log_file = '/root/imported_paths.txt'

# 🏷️ Champ personnalisé dans Calibre
custom_field = '#collec'

# 📅 Importer uniquement les fichiers créés/modifiés depuis cette date
# Format : AAAA-MM-JJ
DATE_MIN = "2026-10-01"
date_min = datetime.strptime(DATE_MIN, "%Y-%m-%d")


# 🔧 Fonction pour normaliser le nom du dossier parent
def normalize_folder_name(name):
    name = name.strip()
    name = re.sub(r'\s+', '-', name)
    name = re.sub(r'[^\w\-]', '', name)
    return name


# 📚 Charger la librairie avec la nouvelle API
library = db(LIBRARY_PATH).new_api


# 📥 Charger chemins déjà importés
imported_paths = set()

if os.path.exists(log_file):
    with open(log_file, 'r', encoding='utf-8') as f:
        imported_paths = set(
            line.strip()
            for line in f
            if line.strip()
        )


# 🔄 Parcourir les fichiers
with open(log_file, 'a', encoding='utf-8') as log:

    for root, dirs, files in os.walk(import_folder):

        for filename in files:

            if not filename.lower().endswith(('.epub', '.pdf', '.cbr', '.cbz')):
                continue

            full_path = os.path.abspath(
                os.path.join(root, filename)
            )

            # 📅 Date de dernière modification du fichier
            file_date = datetime.fromtimestamp(
                os.path.getmtime(full_path)
            )

            # ⏩ Ignorer les fichiers antérieurs à DATE_MIN
            if file_date < date_min:
                print(
                    f"⏩ Trop ancien : {full_path} "
                    f"({file_date.strftime('%Y-%m-%d %H:%M:%S')})"
                )
                continue

            # ⏩ Ignorer les fichiers déjà importés
            if full_path in imported_paths:
                print(f'⏩ Déjà importé : {full_path}')
                continue

            print(
                f"→ Ajout : {full_path} "
                f"({file_date.strftime('%Y-%m-%d %H:%M:%S')})"
            )

            rel_path = os.path.relpath(
                full_path,
                import_folder
            )

            parts = rel_path.split(os.sep)

            folder_name = (
                parts[0]
                if len(parts) > 1
                else ""
            )

            collection_name = normalize_folder_name(
                folder_name
            )

            # 🔍 Extraction des métadonnées
            file_ext = os.path.splitext(
                filename
            )[1][1:].lower()

            format_key = file_ext.upper()

            with open(full_path, 'rb') as f:
                mi = get_metadata(
                    f,
                    file_ext
                )

            mi.timestamp = now()
            mi.isbn = None

            # ➕ Ajout du livre
            ids, duplicates = library.add_books([
                (
                    mi,
                    {
                        format_key: full_path
                    }
                )
            ])

            if not ids:
                print(
                    f"⚠️ Livre non ajouté "
                    f"(duplicate ou erreur) : {full_path}"
                )
                continue

            book_id = ids[0]

            # 🏷️ Appliquer la valeur dans le champ personnalisé
            try:

                if folder_name != "":
                    library.set_field(
                        custom_field,
                        {
                            book_id: collection_name
                        }
                    )

                print(
                    f"✅ '{filename}' ajouté "
                    f"avec collec = '{collection_name}'"
                )

            except KeyError:

                print(
                    f"❌ Erreur : champ personnalisé "
                    f"'{custom_field}' introuvable dans la base."
                )

                continue

            # 📝 Ajout immédiat dans le fichier de log
            log.write(full_path + '\n')
            log.flush()
