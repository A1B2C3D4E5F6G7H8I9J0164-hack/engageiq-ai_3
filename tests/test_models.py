"""Tests for database models."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.config.settings import PrivacyMode, UserRole
from src.models import Base, Course, User

# DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/engageiq_dev"

# engine = create_engine(DATABASE_URL)
engine = create_engine("sqlite:///:memory:")


@pytest.fixture(scope="module", autouse=True)
def create_tables():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


def test_create_user():
    """Test user creation."""

    with Session(engine) as db:
        user = User(
            name="Test User",
            email="testuser@example.com",
            role=UserRole.STUDENT,
            privacy_mode=PrivacyMode.LOCAL_ONLY,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        assert user.id is not None
        assert user.name == "Test User"


def test_course_teacher_relationship():
    """Test course belongs to a teacher."""

    with Session(engine) as db:
        teacher = User(
            name="Teacher",
            email="teacher@example.com",
            role=UserRole.TEACHER,
            privacy_mode=PrivacyMode.SHARE_WITH_TEACHER,
        )

        db.add(teacher)
        db.commit()
        db.refresh(teacher)

        course = Course(
            name="Mathematics",
            code="MATH999",
            teacher_id=teacher.id,
        )

        db.add(course)
        db.commit()
        db.refresh(course)

        assert course.teacher_id == teacher.id
        assert course.teacher.name == "Teacher"


def test_unique_email():
    """Email should be unique."""

    with Session(engine) as db:
        user1 = User(
            name="A",
            email="duplicate@example.com",
            role=UserRole.STUDENT,
            privacy_mode=PrivacyMode.LOCAL_ONLY,
        )

        db.add(user1)
        db.commit()

        user2 = User(
            name="B",
            email="duplicate@example.com",
            role=UserRole.STUDENT,
            privacy_mode=PrivacyMode.LOCAL_ONLY,
        )

        db.add(user2)

        with pytest.raises(IntegrityError):
            db.commit()

        db.rollback()
