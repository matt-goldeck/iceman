import random
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    catchphrases = [
        "🏎️ I feel the need -- the need for speed!",
        "🦅 You can be my wingman any time.",
        "🗼 Sorry Goose, but it's time to buzz the tower.",
        "🥈 No points for second place.",
    ]
    return {"message": random.choice(catchphrases)}
