"""
Tool definitions for the LLM
"""

TOOL_DEFINITIONS = [
    {
        "name": "list_products",
        "description": "List all available products. Can filter by category (Monitors, Printers, Accessories, Networking) or active status.",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "Filter by category: Monitors, Printers, Accessories, or Networking"
                },
                "is_active": {
                    "type": "boolean",
                    "description": "Filter by active status"
                }
            }
        }
    },
    {
        "name": "get_product",
        "description": "Get detailed information about a specific product by its SKU code (e.g., MON-0054, PRI-0101).",
        "parameters": {
            "type": "object",
            "properties": {
                "sku": {
                    "type": "string",
                    "description": "Product SKU code"
                }
            },
            "required": ["sku"]
        }
    },
    {
        "name": "search_products",
        "description": "Search for products by name or description. Use this when customers ask about specific types of products.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (e.g., 'monitor', 'wireless keyboard', '27-inch')"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_customer",
        "description": "Get customer information by their customer ID (UUID).",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "Customer UUID"
                }
            },
            "required": ["customer_id"]
        }
    },
    {
        "name": "verify_customer_pin",
        "description": "Verify a customer's identity using their email and 4-digit PIN. Use this before accessing sensitive information or placing orders.",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "Customer email address"
                },
                "pin": {
                    "type": "string",
                    "description": "4-digit PIN code"
                }
            },
            "required": ["email", "pin"]
        }
    },
    {
        "name": "list_orders",
        "description": "List orders. Can filter by customer ID or order status (draft, submitted, approved, fulfilled, cancelled).",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "Filter by customer UUID"
                },
                "status": {
                    "type": "string",
                    "description": "Filter by status: draft, submitted, approved, fulfilled, or cancelled"
                }
            }
        }
    },
    {
        "name": "get_order",
        "description": "Get detailed information about a specific order including all items.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "Order UUID"
                }
            },
            "required": ["order_id"]
        }
    },
    {
        "name": "create_order",
        "description": "Create a new order for a customer. Requires customer verification first.",
        "parameters": {
            "type": "object",
            "properties": {
                "customer_id": {
                    "type": "string",
                    "description": "Customer UUID"
                },
                "items": {
                    "type": "array",
                    "description": "List of items with sku, quantity, unit_price, and currency (USD)",
                    "items": {
                        "type": "object",
                        "properties": {
                            "sku": {"type": "string"},
                            "quantity": {"type": "integer"},
                            "unit_price": {"type": "string"},
                            "currency": {"type": "string"}
                        }
                    }
                }
            },
            "required": ["customer_id", "items"]
        }
    }
]


def get_openai_tools():
    """Convert tool definitions to OpenAI/OpenRouter format."""
    return [
        {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["parameters"]
            }
        }
        for tool in TOOL_DEFINITIONS
    ]
