from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == '"This is the root of our api. To see all the available endpoints, go to /docs."'


def test_get_customer():
    response = client.get(
        "/customers/17",
    )
    assert response.status_code == 200
    

def test_update_customer():
    response = client.put(
        "/customers/17",
        json={
            "id": 17,
            "name": "Ariston Alex",
            "age": 25,
            "city": "Kaohsiung"
        },
    )
    assert response.status_code == 200
    assert response.text == '"Updated successfully!"'


def test_wrong_update_customer():
    response = client.put(
        "/customers/77",
        json={
            "id": 77,
            "name": "Ariston Alex",
            "age": 25,
            "city": "Kaohsiung"
        },
    )
    assert response.status_code == 422
    assert response.text == '"Failed to update customer if id of 77"'
    
    
def test_update_customer_wrong_method():
    response = client.post(
        "/customers/17",
        json={
            "id": 17,
            "name": "Ariston Alex",
            "age": 25,
            "city": "Kaohsiung"
        },
    )
    assert response.status_code == 405
    assert response.text == '{"detail":"Method Not Allowed"}'
