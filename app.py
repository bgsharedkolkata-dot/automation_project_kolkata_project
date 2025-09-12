import httpx
import asyncio

# URL of the FastAPI server (Assuming it runs locally)
BASE_URL = "http://127.0.0.1:8000"

# Function to send POST request to the /update-context endpoint
async def test_post():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/update-context",
            json={
                "model": "model_v1",
                "task": "classification",
                "status": "in-progress"
            }
        )
        if response.status_code == 200:
            print("POST request successful:")
            print(response.json())
        else:
            print(f"Failed to POST: {response.status_code} - {response.text}")

# Function to send GET request to the /context/{model_name} endpoint
async def test_get(model_name: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/context/{model_name}")
        if response.status_code == 200:
            print("GET request successful:")
            print(response.json())
        else:
            print(f"Failed to GET: {response.status_code} - {response.text}")

# Main function to test both POST and GET
async def main():
    await test_post()  # Test POST request to /update-context
    await asyncio.sleep(2)  # Wait for the POST request to be processed
    await test_get("model_v1")  # Test GET request to /context/model_v1

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())
