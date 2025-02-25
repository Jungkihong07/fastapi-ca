import asyncio
from datetime import datetime
from fastapi import APIRouter

router = APIRouter(prefix="/async-test")


async def async_test(num):
    print("aysnc_task:", num)
    await asyncio.sleep(1)
    return num


@router.get("")
async def async_example():
    now = datetime.now()
    results = await asyncio.gather(async_test(1), async_test(2), async_test(3))
    print(datetime.now() - now)
    return {"results": results}
