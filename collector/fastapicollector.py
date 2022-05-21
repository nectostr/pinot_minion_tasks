import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/quality")
async def quality(obj: dict):
    print(obj)


@app.post("/state")
async def state(obj: dict):
    print(obj)


@app.post("/report")
async def report(obj: dict):
    print(obj)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=34543)
