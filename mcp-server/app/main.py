from fastapi import FastAPI
from routes.chat import router

app = FastAPI(title="MCP Server")

app.include_router(router, prefix="/chat", tags=["Chat"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
