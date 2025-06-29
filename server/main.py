from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# ✅ CORS for communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🟢 Live check
@app.get("/ping")
async def ping():
    return {"message": "Server is running."}

# ✅ Get VPS Online Status
@app.get("/vps_status")
async def vps_status():
    try:
        with open("vps_status.json", "r") as f:
            return f.read()
    except:
        return {"online": 0, "offline": 0, "total": 0}

# ✅ Main Task Handler
@app.post("/run_task")
async def run_task(req: Request):
    data = await req.json()
    # Tum custom logic yaha add karo (jaise message save karna, log file, etc.)
    print(f"📥 New Task: {data}")
    with open("current_task.json", "w") as f:
        f.write(str(data))
    return {"status": "success", "message": "Task received"}

# ✅ Script Update Handler
@app.get("/get_script_version")
async def script_version():
    return {"version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
