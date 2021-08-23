from typing import Optional

from pydantic import BaseModel


class CommandArgument(BaseModel):
    name: str
    description: str


class Command(BaseModel):
    name: str
    description: str
    arguments: Optional[list[CommandArgument]]
