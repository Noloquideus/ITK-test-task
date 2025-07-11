from decimal import Decimal
from pydantic import BaseModel, ConfigDict, field_serializer


class WalletSchema(BaseModel):
    """
    Pydantic schema for wallet data serialization.
    
    Attributes:
        id: Unique identifier for the wallet
        balance: Current balance of the wallet (using Decimal for precision)
    """
    id: str
    balance: Decimal

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

    @field_serializer('balance')
    def serialize_balance(self, value: Decimal) -> str:
        """Serialize Decimal balance to string."""
        return str(value)
