from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.db import get_db
from api.models import UIElement
from api.schemas import UIElementOut
from api.auth import get_current_user

router = APIRouter()

@router.get("/elements", response_model=list[UIElementOut])
def list_elements(
    db: Session = Depends(get_db),
    _user = Depends(get_current_user),
):
    rows = db.query(UIElement).order_by(UIElement.id.asc()).all()
    return rows

