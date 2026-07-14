"""Seed script for development data."""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.config.settings import PrivacyMode, UserRole
from src.models import Course
from src.models import Session as LectureSession
from src.models import User

DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/engageiq_dev"

engine = create_engine(DATABASE_URL)


def seed() -> None:
    with Session(engine) as db:
        # Prevent duplicate seeding
        if db.query(User).first():
            print("Database already contains data. Skipping seed.")
            return

        # -------------------------
        # Teachers
        # -------------------------
        teacher1 = User(
            name="Rahul Sharma",
            email="rahul@example.com",
            role=UserRole.TEACHER,
            privacy_mode=PrivacyMode.SHARE_WITH_TEACHER,
        )

        teacher2 = User(
            name="Zalak Patel",
            email="zalak@example.com",
            role=UserRole.TEACHER,
            privacy_mode=PrivacyMode.SHARE_WITH_TEACHER,
        )

        db.add_all([teacher1, teacher2])
        db.commit()

        db.refresh(teacher1)
        db.refresh(teacher2)

        # -------------------------
        # Students
        # -------------------------
        students = []

        for i in range(1, 11):
            students.append(
                User(
                    name=f"Student {i}",
                    email=f"student{i}@example.com",
                    role=UserRole.STUDENT,
                    privacy_mode=PrivacyMode.LOCAL_ONLY,
                )
            )

        db.add_all(students)
        db.commit()

        # -------------------------
        # Courses
        # -------------------------
        courses = [
            Course(
                name="Mathematics",
                code="MATH101",
                teacher_id=teacher1.id,
            ),
            Course(
                name="Science",
                code="SCI101",
                teacher_id=teacher2.id,
            ),
            Course(
                name="English",
                code="ENG101",
                teacher_id=teacher1.id,
            ),
        ]

        db.add_all(courses)
        db.commit()

        for course in courses:
            db.refresh(course)

        # -------------------------
        # Sessions
        # -------------------------
        sessions = [
            LectureSession(course_id=courses[0].id),
            LectureSession(course_id=courses[0].id),
            LectureSession(course_id=courses[1].id),
            LectureSession(course_id=courses[1].id),
            LectureSession(course_id=courses[2].id),
        ]

        db.add_all(sessions)
        db.commit()

        print("✅ Seed completed successfully!")
        print("Teachers: 2")
        print("Students: 10")
        print("Courses: 3")
        print("Sessions: 5")


if __name__ == "__main__":
    seed()
