"""EngagementLog model."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.settings import EngagementState
from src.models.base import Base

if TYPE_CHECKING:
    from src.models.session import Session
    from src.models.user import User


class EngagementLog(Base):
    """Stores per-frame engagement data."""

    __tablename__ = "engagement_logs"

    id: Mapped[int] = mapped_column(primary_key=True)

    session_id: Mapped[int] = mapped_column(
        ForeignKey("sessions.id", ondelete="CASCADE"),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
    )

    score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    state: Mapped[EngagementState] = mapped_column(
        Enum(EngagementState),
        nullable=False,
    )

    gaze: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    drowsiness: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    expression: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    session: Mapped["Session"] = relationship(back_populates="engagement_logs")

    user: Mapped["User"] = relationship(back_populates="engagement_logs")
