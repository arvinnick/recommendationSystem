import asyncio

from fastapi import FastAPI
from pydantic import BaseModel
from random import randint

app = FastAPI()




@app.post("/generator")
async def generator(model_name):
    """
    The service that generates recommendations
    :param payload: json payload including model name and viewer id
    :return: random recommendation. A json data including reason (which is essencially the model name)
             and result (recommended number)
    """
    random_number = randint(1, 100)
    return {"reason": model_name, "result": random_number}

@app.get("/cascade-test")
async def runcascade(model_name):
    return await asyncio.gather(*[generator(model_name) for _ in range(5)])



