import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from typing import TextIO
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DUMP_FOLDER = "."
file_descriptors = {}


def create_file_ds(view_id: str) -> TextIO:
    global file_descriptors
    file = open(f"{os.path.join(DUMP_FOLDER,view_id)}.txt", "a")
    file_descriptors[view_id] = file
    return file


def parse_descriptor(text: str):
    return text.replace(r' / ', '_').replace(" ", "_")


@app.post("/quality")
async def quality(obj: dict):
    """
    On quality change
    :param obj:
    :return:
    """
    global file_descriptors
    if 'video_id_and_cpn' in obj:
        parsed_desc = parse_descriptor(obj['video_id_and_cpn'])
        name = f"event_{parsed_desc}"
        event_file = file_descriptors.get(name, create_file_ds(name))
        print(obj, file=event_file, flush=True)


@app.post("/state")
async def state(obj: dict):
    """
    On player state change
    :param obj:
    :return:
    """
    global file_descriptors
    if 'video_id_and_cpn' in obj:
        parsed_desc = parse_descriptor(obj['video_id_and_cpn'])
        name = f"event_{parsed_desc}"
        event_file = file_descriptors.get(name, create_file_ds(name))
        print(obj, file=event_file, flush=True)


@app.post("/report")
async def report(obj: dict):
    """
    Each Nms report
    :param obj:
    :return:
    """
    global file_descriptors
    if 'video_id_and_cpn' in obj:
        parsed_desc = parse_descriptor(obj['video_id_and_cpn'])
        name = f"report_{parsed_desc}"
        report_file = file_descriptors.get(name, create_file_ds(name))
        print(obj, file=report_file, flush=True)


if __name__ == '__main__':
    try:
        uvicorn.run(app, host='0.0.0.0', port=34543)
    except (KeyboardInterrupt, Exception) as e:
        for i in file_descriptors:
            file_descriptors[i].close()
        raise
