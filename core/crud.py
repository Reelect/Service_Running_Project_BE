import math
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import Union
from datetime import datetime, timedelta
import pytz


class CRUD:
    def __init__(self, session: Session) -> None:
        self.session = session
        # self.query = self.session.query(table)

    def get_list(self, table: BaseModel):
        return self.session.query(table).all()

    def get_record(self, table: BaseModel, cond={}):
        filters = []
        for table_id, id in cond.items():
            filters.append(getattr(table, table_id) == id)
        return self.session.query(table).filter(*filters).first()

    def create_record(self, table: BaseModel, req: BaseModel):
        db_record = table(**req.dict())
        self.session.add(db_record)
        self.session.commit()
        self.session.refresh(db_record)
        return db_record

    def update_record(self, db_record: BaseModel, req: Union[BaseModel, dict]):
        if isinstance(req, BaseModel):
            req = req.dict()
        for key, value in req.items():
            setattr(db_record, key, value)
        self.session.commit()

        return db_record

    def patch_record(self, db_record: BaseModel, req: Union[BaseModel, dict]):
        if isinstance(req, BaseModel):
            req = req.dict()
        for key, value in req.items():
            if value:
                setattr(db_record, key, value)
            if value == 0:
                setattr(db_record, key, value)
        self.session.commit()

        return db_record

    def delete_record(self, table: BaseModel, cond={}):
        db_record = self.get_record(table, cond)
        if db_record:
            self.session.delete(db_record)
            self.session.commit()
            return 1
        else:
            return -1

    def paging_record(self, table: BaseModel, req: BaseModel):
        total_row = self.session.query(table).count()
        if total_row % req.size == 0:
            total_page = math.floor(total_row / req.size)
        else:
            total_page = math.floor(total_row / req.size) + 1
        start = (req.page - 1) * req.size

        items = self.session.query(table).order_by(table.create_time.desc()).offset(start).limit(req.size).all()
        pages = {"items": items, "total_pages": total_page, "page": req.page, "size": req.size, "total_row": total_row}
        return pages

    def search_record(self, table: BaseModel, req: Union[BaseModel, dict]):
        if isinstance(req, BaseModel):
            req = req.dict()
        filters = []
        for key, value in req.items():
            if value == 0 or value:
                if isinstance(value, (int, float)):
                    filters.append(getattr(table, key) == value)
                elif isinstance(value, str):
                    filters.append(getattr(table, key).contains(value))
                elif isinstance(value, list):
                    filters.append(func.json_contains(getattr(table, key), str(value)) == 1)

        result = self.session.query(table).filter(*filters).all()
        return result

    def search_today_record(self, table: BaseModel):
        # 현재 날짜와 시간
        seoul_timezone = pytz.timezone("Asia/Seoul")
        today = datetime.now(seoul_timezone)
        # 오늘 0시 0분 0초
        start_of_today = today.replace(hour=0, minute=0, second=0, microsecond=0)
        # 내일 0시 0분 0초
        start_of_tomorrow = start_of_today + timedelta(days=1)

        filters = [
            getattr(table, "update_time") >= start_of_today,
            getattr(table, "update_time") < start_of_tomorrow,
            getattr(table, "complete") == 2
        ]

        result = self.session.query(table).filter(*filters).all()
        return len(result)