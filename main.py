import uvicorn
from fastapi import FastAPI

from middlewares import create_middlewares
from user.interface.controllers.user_controller import router as user_routers
from note.interface.controller.note_controller import router as note_routers

from example.ch10_01.background_task import router as background_router
from example.ch_06_02.sync_ex import router as sync_ex_router
from example.ch_06_02.async_ex import router as async_ex_router
from example.ch08_03.env_ex import router as info_routers
from example.ch11_01.context_sample import router as context_ex_router

from example.ch11_01.middleware import create_sample_middleware

from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from containers import Container


app = FastAPI()
app.container = Container()
app.include_router(user_routers)
app.include_router(sync_ex_router)
app.include_router(async_ex_router)
app.include_router(info_routers)
app.include_router(note_routers)
app.include_router(background_router)
app.include_router(context_ex_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content=exc.errors())


@app.get("/")
def hello():
    return {"Hello": "FastApi"}


create_sample_middleware(app)
create_middlewares(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", reload=True)
