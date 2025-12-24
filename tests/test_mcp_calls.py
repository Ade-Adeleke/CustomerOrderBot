import requests
import json

MCP_SERVER_URL = "https://vipfapwm3x.us-east-1.awsapprunner.com/mcp"
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

def call_mcp_tool(tool_name, arguments=None):
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments or {}
        }
    }
    response = requests.post(MCP_SERVER_URL, json=payload, headers=HEADERS, timeout=15)
    return response.json()

# Test 1: List all products
print("=== List Products ===")
result = call_mcp_tool("list_products")
print(json.dumps(result, indent=2))

# Test 2: Search products
print("\n=== Search Products: 'monitor' ===")
result = call_mcp_tool("search_products", {"query": "monitor"})
print(json.dumps(result, indent=2))

# Test 3: List orders
print("\n=== List Orders ===")
result = call_mcp_tool("list_orders")
print(json.dumps(result, indent=2))
