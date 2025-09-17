from typing import Optional, Literal, Annotated
from pydantic import BaseModel, StringConstraints

Username = Annotated[str, StringConstraints(strip_whitespace=True, min_length=3, max_length=50)]
Password = Annotated[str, StringConstraints(min_length=6, max_length=128)]
ElementKey = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)]

class RegisterIn(BaseModel):
    username: Username
    password: Password

class LoginIn(BaseModel):
    username: Username
    password: Password

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    username: str
    model_config = {"from_attributes": True}

class UIElementOut(BaseModel):
    id: int
    type: Literal["button", "text_input"]
    label: str
    key: str
    model_config = {"from_attributes": True}

class EventIn(BaseModel):
    """
    What the frontend sends when a user interacts with the UI.
    - element_key: stable identifier for the element (e.g., "btn_red", "txt_note")
    - event_type: "click" | "text_submit"
    - payload: optional text; REQUIRED when event_type == "text_submit"
    - session_id: optional, future grouping
    """
    element_key: ElementKey
    event_type: Literal["click", "text_submit"]
    payload: Optional[str] = None
    session_id: Optional[str] = None

class EventOut(BaseModel):
    id: int
    event_type: Literal["click", "text_submit"]
    user_id: int
    ui_element_id: int
    payload: Optional[str] = None
    session_id: Optional[str] = None
    model_config = {"from_attributes": True}