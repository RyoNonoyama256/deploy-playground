import os

import boto3
import pytest
from moto import mock_aws
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def aws_env(monkeypatch):
    """テスト用のAWS環境変数を設定"""
    monkeypatch.setenv("AWS_DEFAULT_REGION", "ap-northeast-1")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("TABLE_NAME", "Memos")
    # DYNAMODB_ENDPOINTを消してmotoを使わせる
    monkeypatch.delenv("DYNAMODB_ENDPOINT", raising=False)


@pytest.fixture()
def client(aws_env):
    """motoでDynamoDBをモックし、テスト用のFastAPIクライアントを返す"""
    with mock_aws():
        # テーブル作成
        dynamodb = boto3.resource("dynamodb", region_name="ap-northeast-1")
        dynamodb.create_table(
            TableName="Memos",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )

        # appモジュールをmotoのコンテキスト内でリロード
        import importlib
        import app as app_module
        importlib.reload(app_module)

        yield TestClient(app_module.app)


def test_list_memos_empty(client):
    """最初はメモが空"""
    res = client.get("/memos")
    assert res.status_code == 200
    assert res.json() == []


def test_create_and_get_memo(client):
    """メモを作成して取得できる"""
    res = client.post("/memos", json={"title": "テスト", "content": "内容"})
    assert res.status_code == 201
    memo = res.json()
    assert memo["title"] == "テスト"
    assert memo["content"] == "内容"
    assert "id" in memo
    assert "createdAt" in memo

    # 一覧に含まれる
    res = client.get("/memos")
    assert len(res.json()) == 1

    # IDで取得
    res = client.get(f"/memos/{memo['id']}")
    assert res.status_code == 200
    assert res.json()["title"] == "テスト"


def test_create_memo_title_required(client):
    """titleは必須"""
    res = client.post("/memos", json={"content": "内容だけ"})
    assert res.status_code == 422


def test_delete_memo(client):
    """メモを削除できる"""
    res = client.post("/memos", json={"title": "削除テスト"})
    memo_id = res.json()["id"]

    res = client.delete(f"/memos/{memo_id}")
    assert res.status_code == 200

    res = client.get(f"/memos/{memo_id}")
    assert res.status_code == 404


def test_get_memo_not_found(client):
    """存在しないIDは404"""
    res = client.get("/memos/nonexistent")
    assert res.status_code == 404
