import sqlite3

# script différentiel kobo-calibre en ignorant les #collec = 113 (bande dessinées)

calibre_db = "/config/Bibliothèque calibre/metadata.db"
kobo_db = "/mnt/KOBOeReader/.kobo/KoboReader.sqlite"

# Connexions
con_calibre = sqlite3.connect(calibre_db)
con_kobo = sqlite3.connect(kobo_db)

# --- Récupère les titres depuis Calibre ---
cur = con_calibre.cursor()
cur.execute("""
SELECT b.title FROM books b LEFT JOIN books_custom_column_1_link c ON b.id = c.book WHERE c.value IS NULL OR c.value != 113
""")
calibre_titles = {title.strip().lower() for (title,) in cur.fetchall()}

# --- Récupère les titres depuis Kobo ---
cur = con_kobo.cursor()
cur.execute("""
    SELECT Title
    FROM content
    WHERE BookID IS NULL AND (Series IS NULL OR (lower(Series) != 'bandes-dessinées' AND lower(Series) != 'a-trier' AND lower(Series) != 'beaux-livres' AND lower(Series) != 'cusine'))
""")
kobo_titles = {title.strip().lower() for (title,) in cur.fetchall() if title}

# --- Comparaison ---
missing_on_kobo = calibre_titles - kobo_titles
extra_on_kobo = kobo_titles - calibre_titles

print("=== Livres Calibre absents sur Kobo ===")
for title in sorted(missing_on_kobo):
    print(f"- {title}")

print("\n=== Livres présents sur Kobo mais pas dans Calibre ===")
for title in sorted(extra_on_kobo):
    print(f"- {title}")
