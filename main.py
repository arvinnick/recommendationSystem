import asyncio, random, redis
import json

from fastapi import FastAPI
from random import randint

from pydantic import BaseModel

app = FastAPI()
model_names = ["peerius", "strands", "parallel_dots",
               "sajari", "recombee", "watson", "rumo",
               "froomble"]
redis_cache = redis.Redis()


class ModelName(BaseModel):
    model_name: str


@app.post("/generator")
async def generator(model_name: ModelName):
    """
    The service that generates recommendations
    :param model_name: recommender model name
    :return: random recommendation. A json data including reason (which is essencially the model name)
             and result (recommended number)
    """
    random_number = randint(1, 100)
    return {"reason": model_name, "result": random_number}


async def runcascade():
    """
    generates 5 random number with different model names
    """
    res = list(await asyncio.gather(*[generator(model_name) for model_name in random.choices(model_names, k=5)]))
    return res


async def recommend(viewerid):
    """
    recommender function that gives a random recommendation for the viewer id, or read it from the cache
    """
    cache = redis_cache.get(viewerid)
    #check the cache for the giver user
    if cache:
        res = json.loads(await cache)
    else:
        res = await runcascade()
        await redis_cache.set(viewerid, str(res))
    return res
