from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

"""
ranger 테이블 schema
"""


class PostTreasure(BaseModel):
    nickname: str = Field(..., example="이재선")
    ph_number: str = Field(..., example="010-8XX8-2XX0")

    class Config:
        orm_mode = True


class ReadTreasure(PostTreasure):
    ranger_id: str
    treasure1: int
    treasure2: int
    treasure3: int
    complete: int
    address: Optional[str]
    create_time: datetime
    update_time: datetime

    class Config:
        orm_mode = True

