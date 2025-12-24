import requests
import json

MCP_SERVER_URL = "https://vipfapwm3x.us-east-1.awsapprunner.com/mcp"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

def mcp_request(method, params=None, req_id=1):
    payload = {
        "jsonrpc": "2.0",
        "id": req_id,
        "method": method,
        "params": params or {}
    }
    response = requests.post(MCP_SERVER_URL, json=payload, headers=HEADERS, timeout=15)
    return response.json()

# List tools
print("=== Available Tools ===")
result = mcp_request("tools/list")
print(json.dumps(result, indent=2))

print("\n=== Available Resources ===")
result = mcp_request("resources/list")
print(json.dumps(result, indent=2))

print("\n=== Available Prompts ===")
result = mcp_request("prompts/list")
print(json.dumps(result, indent=2))
