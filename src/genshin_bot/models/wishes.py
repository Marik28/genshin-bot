from typing import Optional

from pydantic import BaseModel


class WishesInfo(BaseModel):
    five_drops_amount: Optional[int]
    four_drops_amount: Optional[int]
    total_rolls_done: Optional[int]
