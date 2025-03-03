import asyncio
from contextvars import ContextVar

from fastapi import APIRouter

""" ContextVar 생성자의 첫 번째 인수는 콘텍스트 변수의 이름이다. 콘텍스트 변수는 여러 개를 생성하고 읽을 수 있다.
콘텍스트 변수를 설정(set)하지 않은 상태에서 변수의 값을 읽으려고(get) 하려고 하면 LookupError 가 일어난다. 따라서 기본값을 정해주는 것이 좋다. """
foo_context: ContextVar[str] = ContextVar("foo", default="bar")

router = APIRouter(prefix="/context")


@router.get("")
async def context_test(var: str):
    # 콘텍스트의 변수로 설정한다.
    foo_context.set(var)
    # 처리에 걸리는 시간을 요청하기 위해 잠시 쉰다.
    await asyncio.sleep(1)

    return {
        "var": var,
        "context_var": foo_context.get(),
    }
