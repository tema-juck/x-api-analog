from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/{user_id}")
def get_id(user_id: int) -> dict:
    return {"user_id": user_id}


@router.post("/create_post")
async def create_post(request: Request):
    data = await request.json()
    return data


@router.patch("/update_post")
async def update_post(request: Request):
    data = await request.json()
    return data


@router.delete("/delete_post")
async def delete_post(request: Request):
    data = await request.json()
    return data
