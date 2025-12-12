from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


router = APIRouter()


orders = {}


class OrderRequest(BaseModel):
    items: list[str]

 
@router.post("/create")
def create_order(order: OrderRequest):
    order_id = str(len(orders) + 1)
    orders[order_id] = order
    return {"order_id": order_id, "status": "Order Created", "items": order.items}


@router.get("/view/{order_id}")
def view_order(order_id: str):
    if order_id not in orders:
      raise HTTPException(status_code=404, detail="Order not found")
    return orders[order_id]


@router.post("/confirm/{order_id}")
def confirm_order(order_id: str):
    if order_id not in orders:
       raise HTTPException(status_code=404, detail="Order not found")
    return {"order_id": order_id, "status": "Order Confirmed"} 