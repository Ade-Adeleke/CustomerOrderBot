"""
Customer Support Chatbot - Streamlit UI
TechGear Pro: Monitors, Printers, Accessories, Networking
"""
import streamlit as st

# Page config - MUST be first Streamlit command
st.set_page_config(
    page_title="TechGear Pro Support",
    page_icon="🖥️",
    layout="centered"
)

import sys
import json
from openai import OpenAI

from src.config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, MODEL_NAME, SYSTEM_PROMPT
from src.mcp_client import MCPClient
from src.tools import get_openai_tools

def log(msg):
    """Print log message with flush for immediate output."""
    print(f"[LOG] {msg}", flush=True)

log("App module loaded")

# Initialize clients
@st.cache_resource
def get_mcp_client():
    return MCPClient()

@st.cache_resource
def get_llm_client():
    if OPENROUTER_API_KEY:
        return OpenAI(base_url=OPENROUTER_BASE_URL, api_key=OPENROUTER_API_KEY)
    return None

mcp_client = get_mcp_client()
llm_client = get_llm_client()


def execute_tool(tool_name: str, arguments: dict) -> str:
    """Execute an MCP tool and return the result."""
    log(f"Executing tool: {tool_name} with args: {arguments}")
    tool_map = {
        "list_products": lambda args: mcp_client.list_products(
            category=args.get("category"),
            is_active=args.get("is_active")
        ),
        "get_product": lambda args: mcp_client.get_product(args.get("sku", "")),
        "search_products": lambda args: mcp_client.search_products(args.get("query", "")),
        "get_customer": lambda args: mcp_client.get_customer(args.get("customer_id", "")),
        "verify_customer_pin": lambda args: mcp_client.verify_customer_pin(
            args.get("email", ""), args.get("pin", "")
        ),
        "list_orders": lambda args: mcp_client.list_orders(
            customer_id=args.get("customer_id"),
            status=args.get("status")
        ),
        "get_order": lambda args: mcp_client.get_order(args.get("order_id", "")),
        "create_order": lambda args: mcp_client.create_order(
            args.get("customer_id", ""), args.get("items", [])
        ),
    }
    
    if tool_name in tool_map:
        result = tool_map[tool_name](arguments)
        log(f"Tool {tool_name} returned: {result[:200]}..." if len(result) > 200 else f"Tool {tool_name} returned: {result}")
        return result
    log(f"Unknown tool: {tool_name}")
    return f"Unknown tool: {tool_name}"


def get_bot_response(user_message: str, chat_history: list) -> str:
    """Get response from Gemini via OpenRouter with tool calling."""
    log(f"User message: {user_message}")
    log(f"Chat history length: {len(chat_history)}")
    
    if not llm_client:
        log("No LLM client - OPENROUTER_API_KEY not set")
        return "⚠️ Please set OPENROUTER_API_KEY in your .env file."
    
    try:
        # Build messages
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for msg in chat_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_message})
        
        log(f"Calling LLM with {len(messages)} messages")
        
        # Call LLM with tools
        response = llm_client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=get_openai_tools(),
            tool_choice="auto"
        )
        
        log(f"LLM response received")
        
        # Handle tool calls (max 5 iterations)
        iteration = 0
        for iteration in range(5):
            message = response.choices[0].message
            
            if not message.tool_calls:
                log(f"No more tool calls after {iteration} iterations")
                break
            
            log(f"Iteration {iteration}: {len(message.tool_calls)} tool calls")
            messages.append(message)
            
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)
                log(f"Tool call: {tool_name}")
                result = execute_tool(tool_name, arguments)
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
            
            log(f"Calling LLM again with tool results")
            response = llm_client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                tools=get_openai_tools(),
                tool_choice="auto"
            )
        
        final_response = response.choices[0].message.content or "I couldn't generate a response. Please try again."
        log(f"Final response: {final_response[:100]}..." if len(final_response) > 100 else f"Final response: {final_response}")
        return final_response
        
    except Exception as e:
        log(f"Error in get_bot_response: {e}")
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
    - "Show me wireless keyboards under $100"
    - "Tell me about product MON-0056"
    - "What's the status of my order?"
    
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
    log(f"=== New chat input received ===")
    log(f"Current session messages: {len(st.session_state.messages)}")
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            log("Getting bot response...")
            response = get_bot_response(prompt, st.session_state.messages[:-1])
            log(f"Bot response received, length: {len(response)}")
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    log(f"Messages after response: {len(st.session_state.messages)}")
    log("=== Chat input processing complete ===")
