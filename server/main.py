from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# In-memory store for connected VPS
vps_registry = {}

# Allow all origins for now
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register_vps")
async def register_vps(request: Request):
    data = await request.json()
    ip = data.get("ip")
    if ip:
        vps_registry[ip] = {"status": "online"}
    return {"status": "registered", "ip": ip}

@app.get("/vps_status")
async def vps_status():
    return vps_registry

@app.post("/run_task")
async def run_task(request: Request):
    task_data = await request.json()
    return {"status": "task received", "task": task_data}

@app.post("/update_script")
async def update_script():
    return {"status": "update triggered"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
