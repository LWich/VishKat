from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.container import Container
from app.domain.exceptions import (
    DomainError,
    DuplicateInventoryNumberError,
    InspectionRejectedError,
)


def create_app(container: Container | None = None) -> FastAPI:
    application_container = container or Container()
    settings = application_container.settings()
    app = FastAPI(title=settings.app_name, version="1.0.0")
    app.state.container = application_container
    app.include_router(router, prefix=settings.api_prefix)

    @app.exception_handler(DuplicateInventoryNumberError)
    async def duplicate_handler(
        _request: Request, exception: DuplicateInventoryNumberError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": str(exception)},
        )

    @app.exception_handler(InspectionRejectedError)
    async def inspection_handler(
        _request: Request, exception: InspectionRejectedError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": str(exception)},
        )

    @app.exception_handler(DomainError)
    async def domain_handler(_request: Request, exception: DomainError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exception)},
        )

    return app


app = create_app()
