from datetime import datetime

from sqlalchemy import (
    create_engine,
    String,
    Integer,
    Float,
    Text,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    sessionmaker,
)

from .config import settings


# =========================================================
# DATABASE CONNECTION
# =========================================================

connect_args = {}

# SQLite requires this setting when used with FastAPI.
if settings.database_url.startswith("sqlite"):
    connect_args = {
        "check_same_thread": False
    }


engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    future=True,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)


# =========================================================
# BASE MODEL
# =========================================================

class Base(DeclarativeBase):
    pass


# =========================================================
# USER TABLE
# =========================================================

class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id: Mapped[str] = mapped_column(
        String(80),
        unique=True,
        index=True,
        nullable=False,
    )

    username: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    weight: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    goal: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )

    intensity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    plans: Mapped[list["Plan"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


# =========================================================
# PLAN TABLE
# =========================================================

class Plan(Base):

    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        index=True,
    )

    original_plan: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    updated_plan: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    nutrition_tip: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    latest_feedback: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    user: Mapped[User] = relationship(
        back_populates="plans",
    )


# =========================================================
# CREATE DATABASE TABLES
# =========================================================

def init_db() -> None:

    Base.metadata.create_all(
        bind=engine
    )


# =========================================================
# DATABASE SESSION
# =========================================================

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# =========================================================
# SAVE / UPDATE USER
# =========================================================

def save_user(db, data):

    existing_user = (
        db.query(User)
        .filter(
            User.user_id == data.user_id
        )
        .first()
    )

    if existing_user:

        existing_user.username = data.username
        existing_user.age = data.age
        existing_user.weight = data.weight
        existing_user.goal = data.goal
        existing_user.intensity = data.intensity

        user = existing_user

    else:

        user = User(
            user_id=data.user_id,
            username=data.username,
            age=data.age,
            weight=data.weight,
            goal=data.goal,
            intensity=data.intensity,
        )

        db.add(user)

    db.commit()

    db.refresh(user)

    return user


# =========================================================
# SAVE PLAN
# =========================================================

def save_plan(
    db,
    user,
    workout_plan: str,
    nutrition_tip: str,
):

    plan = Plan(
        user_id=user.id,
        original_plan=workout_plan,
        nutrition_tip=nutrition_tip,
    )

    db.add(plan)

    db.commit()

    db.refresh(plan)

    return plan


# =========================================================
# GET USER
# =========================================================

def get_user(
    db,
    user_id: str,
):

    return (
        db.query(User)
        .filter(
            User.user_id == user_id
        )
        .first()
    )


# =========================================================
# GET LATEST PLAN
# =========================================================

def get_latest_plan(
    db,
    user_id: str,
):

    return (
        db.query(Plan)
        .join(User)
        .filter(
            User.user_id == user_id
        )
        .order_by(
            Plan.created_at.desc()
        )
        .first()
    )


# =========================================================
# UPDATE PLAN
# =========================================================

def update_plan(
    db,
    plan,
    updated_plan: str,
    feedback: str,
):

    plan.updated_plan = updated_plan

    plan.latest_feedback = feedback

    plan.updated_at = datetime.utcnow()

    db.commit()

    db.refresh(plan)

    return plan


# =========================================================
# GET ALL USERS
# =========================================================

def get_all_users(db):

    return (
        db.query(User)
        .order_by(
            User.created_at.desc()
        )
        .all()
    )


# =========================================================
# DELETE USER
# =========================================================

def delete_user(
    db,
    user_id: str,
) -> bool:

    user = get_user(
        db,
        user_id,
    )

    if not user:

        return False

    db.delete(user)

    db.commit()

    return True