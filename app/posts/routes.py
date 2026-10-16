from fastapi import APIRouter, Depends

from .schema import PostCreateRequest, PostPath, PostUpdateRequest, PostUpdateResponse

router = APIRouter()


@router.get("/{post_id}")
def get_id(path: PostPath = Depends()) -> dict:
    return {"post_id": path.post_id}


@router.post("/create_post")
async def create_post(post: PostCreateRequest):
    return post


@router.patch("/{post_id}")
async def update_post(data: PostUpdateRequest, path: PostPath = Depends()):
    return PostUpdateResponse(post_id=path.post_id, content=data.content)


@router.delete("/{post_id}")
async def delete_post(path: PostPath = Depends()): ...
