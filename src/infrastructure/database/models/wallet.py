import uuid
from decimal import Decimal
from uuid import uuid4
from datetime import datetime, UTC
from sqlalchemy import DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from src.infrastructure.database.models.base import Base


class Wallet(Base):
    """
    Wallet database model.

    Represents a wallet entity with balance tracking and creation timestamp.

    Attributes:
        id: Unique identifier for the wallet (UUID)
        balance: Current balance of the wallet
        created_at: Timestamp when the wallet was created
    """
    __tablename__ = 'wallets'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        default=uuid4,
        comment='Wallet ID'
    )

    balance: Mapped[Decimal] = mapped_column(
        Numeric(scale=2),
        default=Decimal('0.00'),
        comment='Wallet balance'
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        comment='Record creation date'
    )
