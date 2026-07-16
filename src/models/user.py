"""User model."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.settings import PrivacyMode, UserRole
from src.models.base import Base

if TYPE_CHECKING:
    from src.models.course import Course
    from src.models.engagement_log import EngagementLog
    from src.models.nudge import Nudge


class User(Base):
    """User model representing students and teachers."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        nullable=False,
        default=UserRole.STUDENT,
    )

    privacy_mode: Mapped[PrivacyMode] = mapped_column(
        Enum(PrivacyMode),
        nullable=False,
        default=PrivacyMode.LOCAL_ONLY,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    courses: Mapped[list["Course"]] = relationship(back_populates="teacher")

    engagement_logs: Mapped[list["EngagementLog"]] = relationship(back_populates="user")

    nudges: Mapped[list["Nudge"]] = relationship(back_populates="user")
