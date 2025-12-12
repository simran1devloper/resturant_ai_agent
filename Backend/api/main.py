from fastapi import FastAPI
from .menu_routes import router as menu_router
from .order_routes import router as order_router
from .rag_routes import router as rag_router
from .health import router as health_router


app = FastAPI(title="Food Ordering RAG API", version="1.0.0")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(health_router, tags=["Health"])
app.include_router(menu_router, prefix="/menu", tags=["Menu"])
app.include_router(order_router, prefix="/order", tags=["Order"])
app.include_router(rag_router, prefix="/rag", tags=["RAG"])