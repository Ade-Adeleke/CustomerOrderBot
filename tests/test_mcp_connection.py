import requests
import json

MCP_SERVER_URL = "https://vipfapwm3x.us-east-1.awsapprunner.com/mcp"

def test_basic_get():
    """Test basic GET request with SSE accept header"""
    print("\n=== Testing Basic GET Request (SSE) ===")
    try:
        response = requests.get(
            MCP_SERVER_URL,
            headers={"Accept": "text/event-stream"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Content: {response.text[:500]}..." if len(response.text) > 500 else f"Content: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def test_mcp_initialize():
    """Test MCP initialize method"""
    print("\n=== Testing MCP Initialize ===")
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "customer-support-bot",
                "version": "1.0.0"
            }
        }
    }
    
    try:
        response = requests.post(
            MCP_SERVER_URL,
            json=payload,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.json() if response.text else None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_mcp_list_tools():
    """Test MCP list_tools method"""
    print("\n=== Testing MCP List Tools ===")
    payload = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    
    try:
        response = requests.post(
            MCP_SERVER_URL,
            json=payload,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.json() if response.text else None
    except Exception as e:
        print(f"Error: {e}")
        return None

def test_mcp_list_resources():
    """Test MCP list_resources method"""
    print("\n=== Testing MCP List Resources ===")
    payload = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "resources/list",
        "params": {}
    }
    
    try:
        response = requests.post(
            MCP_SERVER_URL,
            json=payload,
            headers={"Content-Type": "application/json", "Accept": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return response.json() if response.text else None
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    print(f"Testing MCP Server at: {MCP_SERVER_URL}")
    print("=" * 50)
    
    test_basic_get()
    test_mcp_initialize()
    test_mcp_list_tools()
    test_mcp_list_resources()

if __name__ == "__main__":
    main()
