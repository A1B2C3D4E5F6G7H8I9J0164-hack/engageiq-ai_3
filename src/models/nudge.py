"""Nudge model."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.settings import NudgeType
from src.models.base import Base

if TYPE_CHECKING:
    from src.models.session import Session
    from src.models.user import User


class Nudge(Base):
    """Stores nudges sent to students."""

    __tablename__ = "nudges"

    id: Mapped[int] = mapped_column(primary_key=True)

    session_id: Mapped[int] = mapped_column(
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    nudge_type: Mapped[NudgeType] = mapped_column(
        Enum(NudgeType),
        nullable=False,
    )

    trigger_state: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    effectiveness_delta: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
    )

    session: Mapped["Session"] = relationship(back_populates="nudges")

    user: Mapped["User"] = relationship(back_populates="nudges")
