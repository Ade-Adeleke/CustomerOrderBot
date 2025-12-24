"""
Configuration and environment settings
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# API Configuration
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "google/gemini-2.0-flash-001"

# MCP Server Configuration
MCP_SERVER_URL = os.environ.get(
    "MCP_SERVER_URL", 
    "https://vipfapwm3x.us-east-1.awsapprunner.com/mcp"
)
MCP_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
MCP_TIMEOUT = 15

# System Prompt
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
