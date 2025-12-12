import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

import uvicorn

def main():
    print("Starting Multi-Agent Food Ordering Backend...")
    # Run the FastAPI app from the api package
    # Reload is enabled for development convenience
    uvicorn.run("Backend.api.main:app", host="0.0.0.0", port=8005, reload=True)


if __name__ == "__main__":
    main()
