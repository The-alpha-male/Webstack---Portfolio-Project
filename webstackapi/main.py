from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from customer.routes import router as customer_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(customer_router)
