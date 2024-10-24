import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from e_comm_app.app.routers import products_v1, users_v1

VERSION_PREFIX = "/v1"
APP_VERSION = "1.0.0"

# FastAPI app
app = FastAPI(
    title="E-Commerse Application Service API",
    description="API for managing products in an e-commerce application.",
    version=APP_VERSION,
)


@app.get("/")
async def read_main():
    return {"msg": "Hello customer"}


app.include_router(users_v1.router, prefix=VERSION_PREFIX)
app.include_router(products_v1.router, prefix=VERSION_PREFIX)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    print("Generating custom OpenAPI schema...")

    openapi_schema = get_openapi(
        title="E-Commerce API",
        version="1.0.0",
        description="API for managing products and orders.",
        routes=app.routes,
    )

    # Add security schemes for BearerAuth
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Add security requirements
    openapi_schema["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    uvicorn.run("main:app", port=8082, host="127.0.0.1", reload=True)
