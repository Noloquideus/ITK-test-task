from pydantic import BaseModel


class WalletSchema(BaseModel):
    id: str
    balance: float
