import asyncio, random, redis, json
from cachetools import TTLCache
from fastapi import FastAPI
from random import randint

app = FastAPI()
recommender_model_names = ["peerius", "strands", "parallel_dots",
                           "sajari", "recombee", "watson", "rumo",
                           "froomble"]
redis_cache = redis.Redis()
local_cache = TTLCache(maxsize=3, ttl=10)



@app.post("/generator/{model_name}")
async def generator(model_name):
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
    model_names_list = [generator(model_name) for model_name in random.choices(recommender_model_names, k=5)]
    res = list(await asyncio.gather(*model_names_list))
    return res


@app.get("/generator/{viewerid}")
async def recommend(viewerid):
    """
    recommender function that gives a random recommendation for the viewer id, or read it from the cache
    """
    if viewerid in local_cache:
        return local_cache[viewerid]
    else:
        cached_item = redis_cache.get(viewerid)
        if cached_item:
            return eval(await cached_item)
        else:
            res = await runcascade()
            await redis_cache.set(viewerid, str(res))
            return res
