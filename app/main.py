from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/{user_id}")
def get_id(user_id: int) -> dict:
    return {"user_id": user_id}


@app.post("/create_post")
async def create_post(request: Request):
    data = await request.json()
    return data


@app.patch("/update_post")
async def update_post(request: Request):
    data = await request.json()
    return data


@app.delete("/delete_post")
async def delete_post(request: Request):
    data = await request.json()
    return data
