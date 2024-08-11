import asyncio
import random
import redis
import json
from cachetools import TTLCache
from fastapi import FastAPI
from random import randint

app = FastAPI()
recommender_model_names = [
    "peerius", "strands", "parallel_dots", "sajari",
    "recombee", "watson", "rumo", "froomble"
]
redis_cache = redis.Redis()
local_cache = TTLCache(maxsize=3, ttl=10)


@app.post("/generator/{model_name}")
async def generator(model_name: str):
    """
    The service that generates recommendations.
    :param model_name: recommender model name.
    :return: A JSON object containing 'reason' (model name) and 'result' (random number).
    """
    random_number = randint(1, 100)
    return {"reason": model_name, "result": random_number}


async def runcascade():
    """
    Generates 5 random numbers with different model names.
    :return: A list of results from the generator function.
    """
    model_names_list = [generator(model_name) for model_name in random.choices(recommender_model_names, k=5)]
    res = list(await asyncio.gather(*model_names_list))
    return res


@app.get("/recommend/{viewerid}")
async def recommend(viewerid: str):
    """
    Recommender function that gives a random recommendation for the viewer ID,
    or reads it from the cache.
    :param viewerid: The ID of the viewer.
    :return: The cached recommendation or a newly generated one.
    """
    if viewerid in local_cache:
        return local_cache[viewerid]
    else:
        cached_item = redis_cache.get(viewerid)
        if cached_item:
            # Decode and load JSON from Redis
            res = json.loads(cached_item.decode('utf-8'))
        else:
            res = await runcascade()
            # Store in Redis as a JSON string
            redis_cache.set(viewerid, json.dumps(res))

        # Store in the local cache
        local_cache[viewerid] = res

        return res
