import functools

import asyncpg
import os

from typing import List

from asyncpg import Connection, Record
from asyncpg.cursor import Cursor
from models import Customer


def pool_wrapper():
    """
    Decorator to handle connection pool and
    facilitate query execution on the database
    """
    def wrapper(func):
        @functools.wraps(func)
        async def wrapped(*args, **kwargs):
            
            pool = await asyncpg.create_pool(
                dsn=os.environ['DATABASE_URL'],
                max_inactive_connection_lifetime=10
            )
            async with pool.acquire() as connection:
                # Open a transaction.
                async with connection.transaction():
                    result = await func(connection, *args, **kwargs)
            await pool.release(connection)
            return result
        return wrapped
    return wrapper


@pool_wrapper()
async def get_all_customers(
        connection: Connection,
        page: int = 0,
        size: int = 10
) -> List[Customer]:
    
    sql = """
        SELECT *
        FROM customers
    """
    
    cur: Cursor = await connection.cursor(sql)
    if page * size > 0:
        # Move the cursor to provide pagination
        await cur.forward(page * size)
        
    # Fetch rows according to the chunk size
    return await cur.fetch(size)


@pool_wrapper()
async def get_customer_by_id(connection: Connection, customer_id: int) -> Record:
    sql = """
        SELECT *
        FROM customers
        WHERE id = $1
    """
    return await connection.fetchrow(sql, customer_id)


@pool_wrapper()
async def add_default_customers(connection: Connection) -> str:
    
    default_customers = [
        (1, 'Caroline Westernick', 21, 'NYC'),
        (2, 'Adam Mengol', 31, 'London'),
        (4, 'João Maria José', 25, 'Rio de Janeiro'),
        (5, 'Sebastian Urel', 27, 'Toronto'),
        (6, 'Leon Colda Dongal', 22, 'Ibiza'),
        (11, 'Ted Honda Connel', 33, 'Amsterdam'),
        (13, 'Loriel Merita', 24, 'Berlim'),
        (14, 'Spliker Sonik', 46, 'Tokio'),
        (15, 'Fernando Ogawa', 30, 'Porto Alegre'),
        (17, 'Abdul Hamid', 48, 'Daca'),
        (18, 'Ariston Alex', 25, 'Kaohsiung'),
        (21, 'Chris Arthus', 22, 'Naipidau'),
        (22, 'Katty Deanna', 19, 'Hanói'),
        (23, 'Emily Ethel', 38, 'Katmandu'),
        (25, 'Nico Teofil', 38, 'Naggu'),
        (30, 'Calvin Joseph', 38, 'Kabul'),
        (32, 'Amberlee Thomas', 38, 'Bagdá'),
        (33, 'Jacob Tyler', 38, 'Paris')
    ]
    
    default_customers_upsert_sql = """
        INSERT INTO customers (id, name, age, city)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (id)
            DO UPDATE
                SET name=$2, age=$3, city=$4
    """
    try:
        await connection.executemany(default_customers_upsert_sql, default_customers)
    except Exception as e:
        return f"Something went wrong: {e}"
    return "Customers added!"


@pool_wrapper()
async def update_customer(
        connection: Connection,
        customer_id: int,
        customer: Customer
) -> str:
    sql = """
        UPDATE customers
        SET name=$1,
            age=$2,
            city=$3
        WHERE id = $4
    """
    return await connection.execute(
        sql,
        customer.name,
        customer.age,
        customer.city,
        customer_id
    )
