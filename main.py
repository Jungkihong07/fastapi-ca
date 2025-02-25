import uvicorn
from fastapi import FastAPI
from user.interface.controllers.user_controller import router as user_routers
from example.ch_06_02.sync_ex import router as sync_ex_router
from example.ch_06_02.async_ex import router as async_ex_router

from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from containers import Container


app = FastAPI()
app.container = Container()
app.include_router(user_routers)
app.include_router(sync_ex_router)
app.include_router(async_ex_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content=exc.errors())


@app.get("/")
def hello():
    return {"Hello": "FastApi"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)
