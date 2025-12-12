from fastapi import APIRouter, HTTPException
import json
import os
from pathlib import Path

router = APIRouter()

# Build absolute path to menu.json
# This file is in Backend/api/
# menu.json is in Backend/Rag/
CURRENT_DIR = Path(__file__).parent
MENU_PATH = CURRENT_DIR.parent / "Rag" / "menu.json"


@router.get("/all")
def list_menu():
    try:
        if not MENU_PATH.exists():
            raise FileNotFoundError(f"Menu file not found at {MENU_PATH}")
            
        with open(MENU_PATH) as f:
            data = json.load(f)
        return data
    except Exception as e:
       print(f"Error loading menu: {e}")
       raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
def search_menu(q: str):
    try:
        with open(MENU_PATH) as f:
            data = json.load(f)
        
        # Simple case-insensitive search
        results = [
            item for item in data 
            if q.lower() in item["name"].lower() or q.lower() in item.get("description", "").lower()
        ]
        return results
    except Exception as e:
        print(f"Error searching menu: {e}")
        raise HTTPException(status_code=500, detail=str(e))