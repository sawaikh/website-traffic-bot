from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Store connected VPS status
vps_status = {}

class StatusRequest(BaseModel):
    vps_id: str
    status: str  # 'online' or 'offline'

class TaskStatus(BaseModel):
    vps_id: str
    success: bool
    message: str

@app.get("/ping")
def ping():
    return {"message": "pong"}

@app.post("/report_status")
async def report_status(data: StatusRequest):
    vps_status[data.vps_id] = data.status
    return {"message": "Status updated"}

@app.get("/vps_status")
def get_vps_status():
    total = len(vps_status)
    online = sum(1 for status in vps_status.values() if status == 'online')
    offline = total - online
    return {
        "online": online,
        "offline": offline,
        "total": total
    }

@app.post("/report_task")
async def report_task_status(data: TaskStatus):
    print(f"✅ Task Report from {data.vps_id}: {'Success' if data.success else 'Failed'} - {data.message}")
    return {"message": "Received"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
