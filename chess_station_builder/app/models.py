from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import (
    JSON,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_child: Mapped[bool] = mapped_column(default=True)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_login: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    parent: Mapped[User | None] = relationship("User", remote_side=[id])
    settings: Mapped["UserSettings"] = relationship(
        "UserSettings", back_populates="user", uselist=False
    )


class UserSettings(db.Model):
    __tablename__ = "user_settings"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    sound_enabled: Mapped[bool] = mapped_column(default=True)
    music_enabled: Mapped[bool] = mapped_column(default=True)
    hint_mode: Mapped[str] = mapped_column(
        Enum("always", "limited", "earned", name="hint_mode"), default="always"
    )
    daily_time_limit_minutes: Mapped[int | None] = mapped_column(nullable=True)
    theme: Mapped[str] = mapped_column(String(20), default="default")

    user: Mapped[User] = relationship("User", back_populates="settings")


class Puzzle(db.Model):
    __tablename__ = "puzzles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    module: Mapped[str] = mapped_column(String(50), nullable=False)
    collection: Mapped[str | None] = mapped_column(String(50))
    puzzle_order: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[str] = mapped_column(
        Enum("easy", "medium", "hard", "expert", name="difficulty"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    fen_position: Mapped[str] = mapped_column(String(100), nullable=False)
    solution_moves: Mapped[dict] = mapped_column(JSON, nullable=False)
    best_move_count: Mapped[int] = mapped_column(Integer, nullable=False)
    hint_text: Mapped[str | None] = mapped_column(Text)


class PuzzleProgress(db.Model):
    __tablename__ = "puzzle_progress"
    __table_args__ = (UniqueConstraint("user_id", "puzzle_id", name="uk_user_puzzle"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    puzzle_id: Mapped[int] = mapped_column(ForeignKey("puzzles.id"), nullable=False)
    stars_earned: Mapped[int] = mapped_column(Integer, default=0)
    best_moves: Mapped[int | None] = mapped_column(Integer)
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    hints_used: Mapped[int] = mapped_column(Integer, default=0)
    first_solved_at: Mapped[datetime | None] = mapped_column(DateTime)
    last_attempted_at: Mapped[datetime | None] = mapped_column(DateTime)


class ModuleProgress(db.Model):
    __tablename__ = "module_progress"
    __table_args__ = (UniqueConstraint("user_id", "module_name", name="uk_user_module"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    module_name: Mapped[str] = mapped_column(String(50), nullable=False)
    is_unlocked: Mapped[bool] = mapped_column(default=False)
    is_completed: Mapped[bool] = mapped_column(default=False)
    unlocked_at: Mapped[datetime | None] = mapped_column(DateTime)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime)


class StarWallet(db.Model):
    __tablename__ = "star_wallet"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    total_earned: Mapped[int] = mapped_column(Integer, default=0)
    total_spent: Mapped[int] = mapped_column(Integer, default=0)
    current_balance: Mapped[int] = mapped_column(Integer, default=0)


class Building(db.Model):
    __tablename__ = "buildings"
    __table_args__ = (UniqueConstraint("user_id", "building_type", name="uk_user_building"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    building_type: Mapped[str] = mapped_column(String(50), nullable=False)
    purchased_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    position_x: Mapped[int] = mapped_column(Integer, default=0)
    position_y: Mapped[int] = mapped_column(Integer, default=0)
    customization: Mapped[dict | None] = mapped_column(JSON)


class Decoration(db.Model):
    __tablename__ = "decorations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    decoration_type: Mapped[str] = mapped_column(String(50), nullable=False)
    position_x: Mapped[int] = mapped_column(Integer, nullable=False)
    position_y: Mapped[int] = mapped_column(Integer, nullable=False)
    rotation: Mapped[int] = mapped_column(Integer, default=0)
    purchased_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Session(db.Model):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime)
    puzzles_solved: Mapped[int] = mapped_column(Integer, default=0)
    stars_earned: Mapped[int] = mapped_column(Integer, default=0)


class DailyChallenge(db.Model):
    __tablename__ = "daily_challenges"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    challenge_date: Mapped[date] = mapped_column(Date, unique=True, nullable=False)
    puzzle_id: Mapped[int] = mapped_column(ForeignKey("puzzles.id"), nullable=False)
    bonus_stars: Mapped[int] = mapped_column(Integer, default=5)


class DailyChallengeCompletion(db.Model):
    __tablename__ = "daily_challenge_completions"
    __table_args__ = (UniqueConstraint("user_id", "challenge_date", name="uk_user_date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    challenge_date: Mapped[date] = mapped_column(Date, nullable=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    stars_earned: Mapped[int] = mapped_column(Integer, nullable=False)


class Streak(db.Model):
    __tablename__ = "streaks"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    current_streak: Mapped[int] = mapped_column(Integer, default=0)
    longest_streak: Mapped[int] = mapped_column(Integer, default=0)
    last_activity_date: Mapped[date | None] = mapped_column(Date)
