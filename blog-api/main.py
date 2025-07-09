from fastapi import FastAPI
from route import router


app = FastAPI(
    title="Blogging API",
    description="A FastAPI application for managing blog posts",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
