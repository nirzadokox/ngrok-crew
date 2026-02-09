"""Test direct HTTP request to ngrok."""
import httpx
import asyncio

async def test():
    try:
        print("Making async GET request...")
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get("https://85e00b2844ad.ngrok.app")
            print(f"Status: {resp.status_code}")
            print(f"Body: {resp.text[:200]}")
    except Exception as e:
        print(f"Async error: {e}")
    
    # Try sync
    try:
        print("\nMaking sync GET request...")
        resp = httpx.get("https://85e00b2844ad.ngrok.app", timeout=10)
        print(f"Status: {resp.status_code}")
        print(f"Body: {resp.text[:200]}")
    except Exception as e:
        print(f"Sync error: {e}")

if __name__ == "__main__":
    asyncio.run(test())
