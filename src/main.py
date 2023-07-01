from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.models.base import HTTPBaseException
from src.routers.users import router as users_router
from src.collections.users import UsersCollection
origins = ["http://localhost:3000"]

app = FastAPI(
    docs_url="/docs",
    openapi_url="/api",
)


@app.exception_handler(HTTPBaseException)
async def backend_exception_handler(
    request: Request,
    exc: HTTPBaseException,
):
    return JSONResponse(
        status_code=exc.code,
        content={"message": exc.message},
    )

UsersCollection.init_dbconn()
app.include_router(users_router, prefix="/users", tags=["Users"])
