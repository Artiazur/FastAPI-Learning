"""
Module: order_handler
---------------------
This module defines a simple FastAPI application for handling customer orders.😊

It demonstrates the use of:
- Path parameters (`customer_id`)
- Request body models (Pydantic `Order` and `Product`)
- Computed fields using `@computed_field`
- Basic data persistence using an in-memory list (`fake_orders_db`)

The API receives an order from a customer, calculates the total price and total quantity,
and returns a summary response containing the customer ID, total quantity, and total price.
"""


from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field, EmailStr

app = FastAPI()


class Product(BaseModel):
    """
    Represents a product in an order.

    Attributes:
        product_name (str): Name of the product.
        price (float): Price per unit of the product.
        quantity (int): Number of units ordered.
    """

    product_name: str
    price: float
    quantity: int


class Order(BaseModel):
    """
    Represents a customer order.

    Attributes:
        email (EmailStr | None): Optional email of the customer.
        products (list[Product]): List of products included in the order.

    Computed Properties:
        total_price (float): Total cost of all products.
        total_quantity (int): Total number of product units.
    """

    email: EmailStr | None = None
    products: list[Product]

    @computed_field
    @property
    def total_price(self) -> float:
        total_price = 0
        for product in self.products:
            total_price += product.price * product.quantity
        return total_price

    @computed_field
    @property
    def total_quantity(self) -> int:
        total_quantity = 0
        for product in self.products:
            total_quantity += product.quantity
        return total_quantity


fake_orders_db = []


@app.post("/order/{customer_id}")
async def process_order(customer_id: int, order: Order):
    """
    Processes a customer order.

    Args:
        customer_id (int): Unique identifier of the customer.
        order (Order): The order data sent in the request body.

    Returns:
        dict: Summary containing the customer ID, total quantity, and total price.
    """
    fake_orders_db.append(order.model_dump())
    return {
        "id": customer_id,
        "quantity": order.total_quantity,
        "total_price": order.total_price,
    }
