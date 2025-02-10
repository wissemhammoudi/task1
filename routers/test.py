from fastapi import APIRouter
import asyncio
import time
import threading

router = APIRouter(prefix="/test", tags=["tests"])

# Endpoint 1 (Blocking I/O in async context)
@router.get("/1")
async def endpoint1():
    print("hello")
    time.sleep(5)  # Blocking I/O operation for testing
    print("bye")

# Endpoint 2 (Async function with non-blocking I/O)
@router.get("/2")
async def endpoint2():
    print("hello1")
    await asyncio.sleep(5)  # Non-blocking I/O operation
    print("Bye1")

# Endpoint 3 (Blocking I/O, run in a separate thread to avoid blocking the main event loop)
def blocking_function():
    print("hello2")
    time.sleep(5)  # Blocking operation
    print("Bye2")

@router.get("/3")
async def endpoint3():
    # Running blocking I/O operation in a separate thread to prevent blocking event loop
    threading.Thread(target=blocking_function).start()
    return {"message": "Started blocking task in a separate thread."}
