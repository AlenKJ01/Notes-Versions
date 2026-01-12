from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Note, NoteVersion
from app.schemas import NoteCreate, NoteUpdate, NoteOut
from app.auth import get_current_user
from typing import Optional
from fastapi import Query
from sqlalchemy import or_
from app.models import ActivityLog

router = APIRouter(prefix="/notes", tags=["Notes"])

@router.post("/", response_model=NoteOut)
def create_note(
    data: NoteCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if not data.title or not data.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Title cannot be empty"
        )

    if not data.content or not data.content.strip():
        raise HTTPException(
            status_code=400,
            detail="Content cannot be empty"
        )    

    note = Note(
        title=data.title,
        content=data.content,
        owner_id=user.id
    )
    db.add(note)
    db.commit()
    db.refresh(note)

    initial_version = NoteVersion(
        note_id=note.id,
        version_number=1,
        title_snapshot=note.title,
        content_snapshot=note.content,
        editor_id=user.id,
    )

    db.add(initial_version)
    db.commit()

    return note

@router.get("/", response_model=list[NoteOut])
def list_notes(
    q: Optional[str] = Query(None),
    title: Optional[str] = Query(None),
    content: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    query = db.query(Note).filter(Note.owner_id == user.id)

    if q:
        query = query.filter(
            Note.title.ilike(f"%{q}%")
        )

    if title:
        query = query.filter(
            Note.title.ilike(f"%{title}%")
        )

    if content:
        query = query.filter(
            Note.content.ilike(f"%{content}%")
        )

    return (
        query
        .order_by(Note.created_at.desc())
        .all()
    )

@router.get("/{note_id}", response_model=NoteOut)
def get_note(
    note_id: int,
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

    return note

@router.put("/{note_id}", response_model=NoteOut)
def update_note(
    note_id: int,
    data: NoteUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if data.title is not None and not data.title.strip():
        raise HTTPException(
            status_code=400, 
            detail="Title cannot be empty"
            )

    if data.content is not None and not data.content.strip():
        raise HTTPException(
            status_code=400, 
            detail="Content cannot be empty"
            )

    note = (
        db.query(Note)
        .filter(Note.id == note_id, Note.owner_id == user.id)
        .first()
    )
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    latest = (
        db.query(NoteVersion)
        .filter(NoteVersion.note_id == note.id)
        .order_by(NoteVersion.version_number.desc())
        .first()
    )
    
    next_version = latest.version_number + 1 if latest else 1
    note.title = data.title or note.title
    note.content = data.content or note.content

    version = NoteVersion(
        note_id=note.id,
        version_number=latest.version_number + 1,
        title_snapshot=note.title,
        content_snapshot=note.content,
        editor_id=user.id,
    )

    db.add(version)
    db.commit()
    db.refresh(note)

    db.add(ActivityLog(
        user_id=user.id,
        note_id=note.id,
        action="EDIT"
    ))
    db.commit()

    return note

@router.delete("/{note_id}")
def delete_note(
    note_id: int,
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

    db.delete(note)
    db.commit()
    return {"status": "deleted"}
