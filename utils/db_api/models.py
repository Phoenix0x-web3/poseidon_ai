import random
from datetime import datetime

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from data.settings import Settings
from data.constants import PROJECT_SHORT_NAME

class Base(DeclarativeBase):
    pass

class Wallet(Base):
    __tablename__ = 'wallets'

    id: Mapped[int] = mapped_column(primary_key=True)
    email_data: Mapped[str] = mapped_column(unique=True, default=None, nullable=True)
    proxy_status: Mapped[str] = mapped_column(default="OK", nullable=True)
    proxy: Mapped[str] = mapped_column(default=None, nullable=True)
    next_activity_action_time: Mapped[datetime | None] = mapped_column(default=None, nullable=True)
    points: Mapped[int] = mapped_column(default=0)
    top: Mapped[int] = mapped_column(default=0)
    invite_code: Mapped[str] = mapped_column(default="")
    ai_model: Mapped[str] = mapped_column(default={})
    completed: Mapped[bool] = mapped_column(default=False)


    def __repr__(self):
        if Settings().show_email_in_logs:
            return f'[{PROJECT_SHORT_NAME} | {self.id} | {self.email_data.split(":")[0] if "icloud" not in self.email_data else self.email_data.split(":")[-1]}]'
        return f'[{PROJECT_SHORT_NAME} | {self.id}]'
