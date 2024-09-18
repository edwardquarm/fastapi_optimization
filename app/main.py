from fastapi import FastAPI, BackgroundTasks
import time
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, UJSONResponse
from pydantic import BaseModel
import ujson
app = FastAPI(default_response_class=UJSONResponse)
app.add_middleware(GZipMiddleware, minimum_size=0)


class MessageSchema(BaseModel):
    message: str

def write_log(message: str):
    with open("log.txt", "a") as log_file:
        log_file.write(message + "\n")
@app.get("/async")
async def async_endpoint():
    import asyncio
    start_time = time.time()
    headers = {"Accept-Encoding": "gzip"}
    await asyncio.sleep(1)
    end_time = time.time()
    time_taken = end_time - start_time
    return UJSONResponse(content={"message": f"This is an asynchronous endpoint. Time taken: {time_taken}"}, headers=headers)

@app.get("/sync")
def sync_endpoint():
    start_time = time.time()
    headers = {"Accept-Encoding": "gzip"}
    time.sleep(1)
    end_time = time.time()
    time_taken = end_time - start_time
    return UJSONResponse(content={"message": f"This is a synchronous endpoint. Time taken: {time_taken}"}, headers=headers)

@app.post("/log")
async def log_message(message: MessageSchema,
                      background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, message.message)
    return JSONResponse(content={"message": "Log will be written in the background."})