from celery.result import AsyncResult
from common.messaging import celery

if __name__ == "__main__":
    async_result = AsyncResult("11d91d21-a0af-4476-aabe-69cc67e660f4", app=celery)
    result = async_result.result

    print(result)
