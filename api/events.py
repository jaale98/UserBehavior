from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.db import get_db
from api.models import Event, EventType, UIElement, User
from api.schemas import EventIn, EventOut
from api.auth import get_current_user

router = APIRouter()

@router.post("/events", response_model=EventOut, status_code=status.HTTP_201_CREATED)
def create_event(
    payload: EventIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    el = db.query(UIElement).filter(UIElement.key == payload.element_key).first()
    if not el:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown element_key")
    
    if payload.event_type == "text_submit" and not (payload.payload and payload.payload.strip()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="payload is required for text_submit")
    
    evt = Event(
        event_type=EventType(payload.event_type),
        user_id=current_user.id,
        ui_element_id=el.id,
        payload=(payload.payload or None),
        session_id=payload.session_id,
    )
    db.add(evt)
    db.commit()
    db.refresh(evt)
    return evt

@router.get("/events", response_model=list[EventOut])
def list_events_for_user(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(Event)
        .filter(Event.user_id == current_user.id)
        .order_by(Event.id.desc())
        .limit(min(limit, 200))
        .all()
    )
    return rows