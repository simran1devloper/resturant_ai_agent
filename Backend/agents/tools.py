# backend/agents/tools.py
import requests

BASE_URL = "http://localhost:8005"    # FastAPI backend URL


# ------------------------
# SEARCH MENU TOOL
# ------------------------
def search_menu(query: str):
    """
    Search food items in the menu.
    """
    url = f"{BASE_URL}/menu/search?q={query}"
    res = requests.get(url)
    return res.json()


# ------------------------
# CREATE ORDER TOOL
# ------------------------
def create_order(items: list[str]):
    """
    Create a new order with list of item IDs.
    """
    url = f"{BASE_URL}/order/create"
    payload = {"items": items}
    res = requests.post(url, json=payload)
    return res.json()


# ------------------------
# VIEW ORDER TOOL
# ------------------------
def view_order(order_id: int):
    """
    Fetch the order details.
    """
    url = f"{BASE_URL}/order/{order_id}"
    res = requests.get(url)
    return res.json()


# ------------------------
# CONFIRM ORDER TOOL
# ------------------------
def confirm_order(order_id: int):
    """
    Confirm the user's order.
    """
    url = f"{BASE_URL}/order/{order_id}/confirm"
    res = requests.post(url)
    return res.json()
