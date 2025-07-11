import uuid
from uuid import uuid4
from datetime import datetime, UTC
from sqlalchemy import DateTime, Float
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from src.infrastructure.database.models.base import Base


class Wallet(Base):
    __tablename__ = 'wallets'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid4,
        comment='Wallet ID'
    )

    balance: Mapped[float] = mapped_column(
        Float,
        comment='Wallet balance'
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        comment='Record creation date'
    )
