import requests
import json

MCP_SERVER_URL = "https://vipfapwm3x.us-east-1.awsapprunner.com/mcp"

# Test 1: Initialize with correct headers
print("=== Testing MCP Initialize ===")
payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {
            "name": "test-client",
            "version": "1.0.0"
        }
    }
}

try:
    response = requests.post(
        MCP_SERVER_URL,
        json=payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        },
        timeout=10
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
except requests.exceptions.Timeout:
    print("Request timed out after 10 seconds")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
