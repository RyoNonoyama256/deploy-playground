import os
import uuid
from datetime import datetime, timezone

import boto3
from boto3.dynamodb.conditions import Key
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from pydantic import BaseModel

# メモCRUD API
app = FastAPI(title="Memo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TABLE_NAME = os.environ.get("TABLE_NAME", "Memos")

DYNAMODB_ENDPOINT = os.environ.get("DYNAMODB_ENDPOINT")

if DYNAMODB_ENDPOINT:
    dynamodb = boto3.resource("dynamodb", endpoint_url=DYNAMODB_ENDPOINT)
else:
    dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table(TABLE_NAME)


class MemoCreate(BaseModel):
    title: str
    content: str = ""


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
