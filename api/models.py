from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Enum, CheckConstraint, Index
import enum

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    events: Mapped[list["Event"]] = relationship(back_populates="user")

class UIType(str, enum.Enum):
    button = "button"
    text_input = "text_input"

class UIElement(Base):
    __tablename__ = "ui_elements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[UIType] = mapped_column(Enum(UIType, name="ui_type", nullable=False))
    label: Mapped[str] = mapped_column(String(100), nullable=False)
    key: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)

    events: Mapped[list["Event"]] = relationship(back_populates="ui_element")

Index("ix_ui_elements_type_key", UIElement.type, UIElement.key, unique=True)

class EventType(str, enum.Enum):
    click = "click"
    text_submit = "text_submit"

class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_type: Mapped[EventType] = mapped_column(Enum(EventType, name="event_type"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    ui_element_id: Mapped[int] = mapped_column(ForeignKey("ui_elements.id", ondelete="RESTRICT"), nullable=False, index=True)
    payload: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    session_id: Mapped[str | None] = mapped_column(String(64), nullable=True)

    user: Mapped["User"] = relationship(back_populates="events")
    ui_element: Mapped["UIElement"] = relationship(back_populates="events")

CheckConstraint(
    "(event_type <> 'text_submit') OR (payload IS NOT NULL)",
    name="events_text_submit_requires_payload",
)