from typing import List, Optional
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from models import Customer
import database as database


app = FastAPI(title="Customer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return "This is the root of our api. " \
           "To see all the available endpoints, go to /docs."


@app.get("/customers", response_model=List[Customer])
async def paginated_customers(page: Optional[int] = 0, size: Optional[int] = 10):
    try:
        result = await database.get_all_customers(page, size)
    except Exception as e:
        result = f"Error fetching paginated customers: {e}"
    return result


@app.post("/customers")
async def default_customers():
    try:
        result = await database.add_default_customers()
    except Exception as e:
        result = f"Something went wrong: {e}"
    return result


@app.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(customer_id: int):
    return await database.get_customer_by_id(customer_id)


@app.put(
    "/customers/{customer_id}",
    response_model=str, responses={
        200: {
            "description": "Successful Response",
        },
        422: {
            "description": "Error",
        },
    }
)
async def update_customer(
        customer_id: int,
        customer: Customer = Body(
            ...,
            example={
                "id": 17,
                "name": "Ariston Alex",
                "age": 25,
                "city": "Kaohsiung"
            },
        ),
):
    update_status = await database.update_customer(customer_id, customer)

    if update_status == "UPDATE 1":
        return "Updated successfully!"

    elif update_status == "UPDATE 0":
        return JSONResponse(
            status_code=422,
            content=f"Failed to update customer if id of {customer_id}"
        )
