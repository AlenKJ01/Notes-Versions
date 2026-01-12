from app.database import SessionLocal
from app.models import Note, NoteVersion

db = SessionLocal()

notes = db.query(Note).all()

created = 0

for note in notes:
    existing = (
        db.query(NoteVersion)
        .filter(NoteVersion.note_id == note.id)
        .first()
    )

    if not existing:
        version = NoteVersion(
            note_id=note.id,
            version_number=1,
            title_snapshot=note.title,
            content_snapshot=note.content,
            editor_id=note.owner_id,
        )
        db.add(version)
        created += 1

db.commit()
db.close()

print(f"Backfill complete. Created {created} initial versions.")
