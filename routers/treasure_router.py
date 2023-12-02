from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import Response
from starlette.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from sqlalchemy.exc import IntegrityError

from core.schema import RequestPage
from core.utils import get_crud
from models.treasure_model import Ranger
from schemas import treasure_schema

from typing import List

router = APIRouter(
    prefix="/ranger",
    tags=["Ranger"],
)

"""
ranger table CRUD
"""


@router.post(
    "/create",
    name="ranger record 생성",
    description="ranger 테이블에 Record 생성합니다, 탐험가를 생성합니다.\n\n",
    response_model_exclude={"create_time", "update_time"},
)
async def create_post(req: treasure_schema.PostTreasure, crud=Depends(get_crud)):
    try:
        result = crud.create_record(Ranger, req)
        return result.ranger_id
    except IntegrityError:
        print(IntegrityError)
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Item with this unique key already exists.")


@router.post(
    "/page-list",
    name="Post Page 리스트 조회(web 최적화)",
    description="Ranger 테이블의 페이지별 Record list 가져오는 API입니다.\
                Page는 0이 아닌 양수로 입력해야합니다\
                Size는 100개로 제한됩니다.\n\n"
                "웹 페이지의 게시글 리스트 조회 형식이므로 앱에서는 사용을 비추천합니다.",
)
async def page_post(req: RequestPage, crud=Depends(get_crud)):
    if req.page <= 0:
        raise HTTPException(status_code=400, detail="Page number should be positive")
    if req.size > 100:
        raise HTTPException(status_code=400, detail="Size should be below 100")
    if req.size <= 0:
        raise HTTPException(status_code=400, detail="Size should be positive")
    return crud.paging_record(Ranger, req)


@router.post(
    "/search",
    name="Post 테이블에서 입력한 조건들에 부합하는 record 를 반환하는 API",
    description="body에 원하는 조건들을 입력하면 and로 필터 결과 리스트를 반환합니다\n\n"
                "조건값이 str 일 경우 그 문자열을 포함하는 모든 record를 반환합니다.\n\n"
                "조건값이 int,float 일 경우 그 값과 동일한 record만 반환합니다.\n\n"
                "조건값이 list 경우 list 항목을 포함하는 모든 record를 반환합니다.\n\n"
                "조건값은 dictionary 형태로 모델에서 검색가능한 [post_id, title, price, description, representative_photo_id, "
                "status, account_id, username, liked]\n\n"
                "위와 같은 목록들을 검색할 수 있습니다. 원하는 필드만 넣어서 검색할 수 있습니다.",
)
async def search_post(
        filters: dict, crud=Depends(get_crud)):
    result = crud.search_record(Ranger, filters)
    if result:
        return result[0].ranger_id
    else:
        raise HTTPException(status_code=404, detail="Record not found")


@router.get(
    "/list",
    name="Post 리스트 조회",
    description="Post 테이블의 모든 Record를 가져옵니다",
    response_model=List[treasure_schema.ReadTreasure],
)
def get_list(crud=Depends(get_crud)):
    return crud.get_list(Ranger)


@router.get(
    "/{id}",
    name="Post record 가져오기",
    description="입력된 id를 키로 해당하는 Record 반환합니다",
)
def read_post(id: str, crud=Depends(get_crud)):
    filter = {"ranger_id": id}
    db_record = crud.get_record(Ranger, filter)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    result = {
        "treasure1": db_record.treasure1,
        "treasure2": db_record.treasure2,
        "treasure3": db_record.treasure3,
        "complete": db_record.complete
    }
    return result


@router.patch(
    "/{id}",
    name="Post 한 record 일부 내용 수정",
    description="수정하고자 하는 id의 record 일부 수정, record가 존재하지 않을시엔 404 오류 메시지반환합니다\n\n"
                "예시 중에 변경하고 싶은 key와 value만 지정하면 됩니다.",
    response_model=treasure_schema.ReadTreasure,
    response_model_exclude={"create_time", "update_time"},
)
async def update_post_sub(id: str, req: dict, crud=Depends(get_crud)):
    filter = {"ranger_id": id}
    db_record = crud.get_record(Ranger, filter)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    result = crud.patch_record(db_record, req)

    if db_record.treasure1 and db_record.treasure2 and db_record.treasure3 and not db_record.complete:
        result = crud.patch_record(db_record, {"complete": 1})
    return result


@router.delete(
    "/{id}",
    name="Post record 삭제",
    description="입력된 id에 해당하는 record를 삭제합니다.",
)
async def delete_post(id: str, crud=Depends(get_crud)):
    filter = {"post_id": id}
    db_record = crud.get_record(Ranger, filter)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    db_api = crud.delete_record(Ranger, filter)
    if db_api != 1:
        raise HTTPException(status_code=404, detail="Record not found")
    return Response(status_code=HTTP_204_NO_CONTENT)

