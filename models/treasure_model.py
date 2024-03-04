import uuid
from sqlalchemy import VARCHAR, Column, text, TEXT, String
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.types import TIMESTAMP

from core.db import Base


class Ranger(Base):
    __tablename__ = "ranger"
    ranger_id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, nullable=False)
    nickname = Column(VARCHAR(30), nullable=False, unique=True)
    ph_number = Column(VARCHAR(20), nullable=False, unique=True)
    treasure1 = Column(TINYINT, default=0)
    treasure2 = Column(TINYINT, default=0)
    treasure3 = Column(TINYINT, default=0)
    complete = Column(TINYINT, default=0, comment="0 no, 1 just complete, 2 선착순 겟또")
    address = Column(TEXT, default=None)
    create_time = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    update_time = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )
    mysql_engine = "InnoDB"
