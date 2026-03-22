import os
import uuid
from datetime import datetime, timezone

import boto3
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mangum import Mangum
from pydantic import BaseModel, Field

# メモCRUD API
app = FastAPI(title="Memo API")

ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "http://localhost:5173")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGIN.split(","),
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.environ.get("API_KEY", "")


@app.middleware("http")
async def check_api_key(request: Request, call_next):
    if request.method == "OPTIONS":
        return await call_next(request)
    if API_KEY and request.headers.get("X-API-Key") != API_KEY:
        return JSONResponse(status_code=401, content={"detail": "Invalid API Key"})
    return await call_next(request)


TABLE_NAME = os.environ.get("TABLE_NAME", "Memos")

DYNAMODB_ENDPOINT = os.environ.get("DYNAMODB_ENDPOINT")

if DYNAMODB_ENDPOINT:
    dynamodb = boto3.resource("dynamodb", endpoint_url=DYNAMODB_ENDPOINT)
else:
    dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table(TABLE_NAME)


class MemoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field("", max_length=10000)


class Memo(BaseModel):
    id: str
    title: str
    content: str
    createdAt: str


@app.get("/memos", response_model=list[Memo])
def list_memos():
    result = table.scan()
    return result.get("Items", [])


@app.get("/memos/{memo_id}", response_model=Memo)
def get_memo(memo_id: str):
    result = table.get_item(Key={"id": memo_id})
    item = result.get("Item")
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item


@app.post("/memos", response_model=Memo, status_code=201)
def create_memo(body: MemoCreate):
    item = {
        "id": str(uuid.uuid4()),
        "title": body.title,
        "content": body.content,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }
    table.put_item(Item=item)
    return item


@app.delete("/memos/{memo_id}")
def delete_memo(memo_id: str):
    table.delete_item(Key={"id": memo_id})
    return {"message": "Deleted"}


@app.on_event("startup")
def create_table():
    if not DYNAMODB_ENDPOINT:
        return
    try:
        dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        pass


# Lambda handler
handler = Mangum(app)
