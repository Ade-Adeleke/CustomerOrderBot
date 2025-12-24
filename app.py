"""
Customer Support Chatbot - Streamlit UI
TechGear Pro: Monitors, Printers, Accessories, Networking
"""
import os
import json
from pathlib import Path
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import requests

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Page config
st.set_page_config(
    page_title="TechGear Pro Support",
    page_icon="🖥️",
    layout="centered"
)

# Configuration
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "google/gemini-2.0-flash-001"
MCP_SERVER_URL = "https://vipfapwm3x.us-east-1.awsapprunner.com/mcp"
MCP_HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

# System prompt
SYSTEM_PROMPT = """You are a helpful customer support assistant for TechGear Pro, a company that sells computer products including monitors, printers, accessories, and networking equipment.

Your role is to:
1. Help customers find products they're looking for
2. Provide product information and recommendations
3. Assist with order inquiries and status checks
4. Help customers place new orders (after verification)

Guidelines:
- Be friendly, professional, and concise
- Use the available tools to look up real product and order information
- When customers ask about products, search or list products to give accurate information
- For order-related queries, ask for order ID or customer information
- Before placing orders or accessing sensitive customer data, verify the customer using their email and PIN
- Always provide prices in USD
- If you don't have enough information, ask clarifying questions

Product Categories: Monitors, Printers, Accessories, Networking"""

# Tool definitions
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_products",
            "description": "List all available products. Can filter by category (Monitors, Printers, Accessories, Networking).",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "Filter by category"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search for products by name or description.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_product",
            "description": "Get detailed information about a specific product by SKU.",
            "parameters": {
                "type": "object",
                "properties": {
                    "sku": {"type": "string", "description": "Product SKU code"}
                },
                "required": ["sku"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_orders",
            "description": "List orders. Can filter by customer ID or status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "string", "description": "Customer UUID"},
                    "status": {"type": "string", "description": "Order status"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_order",
            "description": "Get detailed order information by order ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string", "description": "Order UUID"}
                },
                "required": ["order_id"]
            }
        }
    }
]

# MCP Client function
def call_mcp_tool(tool_name: str, arguments: dict) -> str:
    """Call an MCP tool and return the result."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": tool_name, "arguments": arguments}
    }
    try:
        response = requests.post(MCP_SERVER_URL, json=payload, headers=MCP_HEADERS, timeout=15)
        result = response.json()
        content = result.get("result", {}).get("content", [])
        if content:
            return content[0].get("text", "No response")
        return "No response from server"
    except Exception as e:
        return f"Error: {e}"

# Initialize LLM client
@st.cache_resource
def get_llm_client():
    if OPENROUTER_API_KEY:
        return OpenAI(base_url=OPENROUTER_BASE_URL, api_key=OPENROUTER_API_KEY)
    return None

client = get_llm_client()

def get_bot_response(user_message: str, chat_history: list) -> str:
    """Get response from LLM with tool calling."""
    if not client:
        return "⚠️ Please set OPENROUTER_API_KEY in your .env file."
    
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in chat_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_message})
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )
        
        # Handle tool calls
        for _ in range(5):
            msg = response.choices[0].message
            if not msg.tool_calls:
                break
            
            messages.append(msg)
            
            for tc in msg.tool_calls:
                result = call_mcp_tool(tc.function.name, json.loads(tc.function.arguments))
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": result
                })
            
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=TOOLS,
                tool_choice="auto"
            )
        
        return response.choices[0].message.content or "I couldn't generate a response."
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ============== STREAMLIT UI ==============

st.title("🖥️ TechGear Pro Support")
st.markdown("*Your AI assistant for monitors, printers, accessories & networking*")

# Sidebar
with st.sidebar:
    st.header("💡 Quick Help")
    st.markdown("""
    **Try asking:**
    - "What monitors do you have?"
    - "Show me wireless keyboards"
    - "Tell me about product MON-0056"
    
    **Categories:**
    - 🖥️ Monitors
    - 🖨️ Printers  
    - ⌨️ Accessories
    - 🌐 Networking
    """)
    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.caption("Powered by Gemini Flash via OpenRouter + MCP")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_bot_response(prompt, st.session_state.messages[:-1])
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
