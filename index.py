import logging
import random

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import resume

app = FastAPI()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    catchphrases = [
        "🏎️ I feel the need -- the need for speed!",
        "🦅 You can be my wingman any time.",
        "🗼 Sorry Goose, but it's time to buzz the tower.",
        "🥈 No points for second place.",
    ]
    return {"message": random.choice(catchphrases)}


app.include_router(resume.router, prefix="/resume", tags=["resume"])

print("\nRegistered Routes:")
for route in app.routes:
    if hasattr(route, "methods"):
        print(f"{list(route.methods)} -> {route.path}")
