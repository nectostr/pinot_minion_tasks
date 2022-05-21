import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DUMP_FOLDER = "."
event_file_name = "events.txt"
report_file_name = "report.txt"


@app.post("/quality")
async def quality(obj: dict):
    """
    On quality change
    :param obj:
    :return:
    """
    print(obj, file=event_file, flush=True)



@app.post("/state")
async def state(obj: dict):
    """
    On player state change
    :param obj:
    :return:
    """
    print(obj, file=event_file, flush=True)


@app.post("/report")
async def report(obj: dict):
    """
    Each Nms report
    :param obj:
    :return:
    """
    print(obj, file=report_file, flush=True)


if __name__ == '__main__':
    event_file = open(os.path.join(DUMP_FOLDER, event_file_name), "a")
    report_file = open(os.path.join(DUMP_FOLDER, report_file_name), "a")
    try:
        uvicorn.run(app, host='0.0.0.0', port=34543)
    except (KeyboardInterrupt, Exception) as e:
        event_file.close()
        report_file.close()
        raise

