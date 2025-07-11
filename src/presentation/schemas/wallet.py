from decimal import Decimal
from pydantic import BaseModel, ConfigDict


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
        arbitrary_types_allowed=True,
        json_encoders={
            Decimal: lambda v: str(v)
        }
    )
