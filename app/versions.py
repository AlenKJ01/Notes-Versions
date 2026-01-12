from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Note, NoteVersion
from app.schemas import VersionOut
from app.auth import get_current_user
from app.models import ActivityLog

router = APIRouter(prefix="/notes", tags=["Versions"])

@router.get("/{note_id}/versions")
def list_versions(
    note_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return (
        db.query(NoteVersion)
        .join(Note)
        .filter(
            Note.id == note_id,
            Note.owner_id == user.id
        )
        .order_by(NoteVersion.version_number.desc())
        .all()
    )

@router.post("/{note_id}/versions/{version_number}/restore")
def restore_version(
    note_id: int,
    version_number: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.owner_id == user.id)
        .first()
    )
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    target = (
        db.query(NoteVersion)
        .filter(
            NoteVersion.note_id == note_id,
            NoteVersion.version_number == version_number,
        )
        .first()
    )
    if not target:
        raise HTTPException(status_code=404, detail="Version not found")

    latest = (
        db.query(NoteVersion)
        .filter(NoteVersion.note_id == note_id)
        .order_by(NoteVersion.version_number.desc())
        .first()
    )

    note.title = target.title_snapshot
    note.content = target.content_snapshot

    db.commit()

    new_version = NoteVersion(
        note_id=note_id,
        version_number=latest.version_number + 1,
        title_snapshot=note.title,
        content_snapshot=note.content,
        editor_id=user.id,
    )

    db.add(new_version)
    db.commit()

    db.add(ActivityLog(
        user_id=user.id,
        note_id=note_id,
        action="RESTORE",
        version_number=version_number,
    ))
    db.commit()

    return {"status": "restored"}


@router.post("/{note_id}/versions/{version_number}/preview")
def log_preview(
    note_id: int,
    version_number: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    log = ActivityLog(
        user_id=user.id,
        note_id=note_id,
        action="VIEW",
        version_number=version_number,
    )

    db.add(log)
    db.commit()

    return {"status": "logged"}

@router.delete("/{note_id}/versions/{version_number}")
def delete_version(
    note_id: int,
    version_number: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.owner_id == user.id)
        .first()
    )
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    versions = (
        db.query(NoteVersion)
        .filter(NoteVersion.note_id == note_id)
        .order_by(NoteVersion.version_number)
        .all()
    )

    if len(versions) <= 1:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete the only version"
        )

    target = next(
        (v for v in versions if v.version_number == version_number),
        None
    )

    if not target:
        raise HTTPException(status_code=404, detail="Version not found")

    db.delete(target)
    db.flush() 

    for v in versions:
        if v.version_number > version_number:
            v.version_number += 1000

    db.flush()

    for v in versions:
        if v.version_number > 1000:
            v.version_number -= 1001

    db.commit()

    return {"status": "version deleted"}