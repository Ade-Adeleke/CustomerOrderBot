"""
MCP Client for the Order Management Server
Handles all communication with the MCP server.
"""
import requests
from typing import Optional
from src.config import MCP_SERVER_URL, MCP_HEADERS, MCP_TIMEOUT


class MCPClient:
    """Client for interacting with the MCP server."""
    
    def __init__(self, server_url: str = MCP_SERVER_URL):
        self.server_url = server_url
        self.request_id = 0
    
    def _call(self, method: str, params: Optional[dict] = None) -> dict:
        """Make a JSON-RPC call to the MCP server."""
        self.request_id += 1
        payload = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }
        
        try:
            response = requests.post(
                self.server_url,
                json=payload,
                headers=MCP_HEADERS,
                timeout=MCP_TIMEOUT
            )
            return response.json()
        except requests.exceptions.Timeout:
            return {"error": "Request timed out"}
        except Exception as e:
            return {"error": str(e)}
    
    def call_tool(self, tool_name: str, arguments: Optional[dict] = None) -> str:
        """Call an MCP tool and return the result text."""
        result = self._call("tools/call", {
            "name": tool_name,
            "arguments": arguments or {}
        })
        
        if "error" in result:
            return f"Error: {result['error']}"
        
        try:
            content = result.get("result", {}).get("content", [])
            if content and len(content) > 0:
                return content[0].get("text", "No response")
            return "No response from server"
        except Exception as e:
            return f"Error parsing response: {e}"
    
    # Convenience methods for each tool
    def list_products(self, category: Optional[str] = None, is_active: Optional[bool] = None) -> str:
        args = {}
        if category:
            args["category"] = category
        if is_active is not None:
            args["is_active"] = is_active
        return self.call_tool("list_products", args)
    
    def get_product(self, sku: str) -> str:
        return self.call_tool("get_product", {"sku": sku})
    
    def search_products(self, query: str) -> str:
        return self.call_tool("search_products", {"query": query})
    
    def get_customer(self, customer_id: str) -> str:
        return self.call_tool("get_customer", {"customer_id": customer_id})
    
    def verify_customer_pin(self, email: str, pin: str) -> str:
        return self.call_tool("verify_customer_pin", {"email": email, "pin": pin})
    
    def list_orders(self, customer_id: Optional[str] = None, status: Optional[str] = None) -> str:
        args = {}
        if customer_id:
            args["customer_id"] = customer_id
        if status:
            args["status"] = status
        return self.call_tool("list_orders", args)
    
    def get_order(self, order_id: str) -> str:
        return self.call_tool("get_order", {"order_id": order_id})
    
    def create_order(self, customer_id: str, items: list) -> str:
        return self.call_tool("create_order", {
            "customer_id": customer_id,
            "items": items
        })
