# TechGear Pro Customer Support Chatbot

A customer support chatbot prototype for a computer products company, built with:
- **Streamlit** - Modern chat UI
- **Google Gemini Flash** - Fast, cost-effective LLM (via OpenRouter)
- **MCP Server** - Real-time product and order data via JSON-RPC

## Features

- 🔍 **Product Search** - Find monitors, printers, accessories, and networking equipment
- 📦 **Order Management** - Check order status and details
- 🛒 **Order Creation** - Place new orders (with customer verification)
- 💬 **Natural Language** - Ask questions in plain English
- 🛠️ **Function Calling** - LLM automatically calls MCP tools to fetch real data

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/Ade-Adeleke/CustomerOrderBot.git
cd CustomerOrderBot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your OpenRouter API key:
```
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
```

Get a free API key from: https://openrouter.ai/

### 4. Run the App

```bash
streamlit run app.py --server.port 8501
```

Open http://localhost:8501 in your browser.

## Project Structure

```
CustomerOrderBot/
├── app.py              # Main Streamlit chatbot (single-file)
├── src/
│   ├── app.py          # Modular version
│   ├── config.py       # Configuration & environment
│   ├── mcp_client.py   # MCP server communication
│   └── tools.py        # Tool definitions for LLM
├── tests/              # MCP server test scripts
├── requirements.txt
├── .env.example
└── README.md
```

## MCP Server Integration

The chatbot connects to the MCP server via JSON-RPC and uses these tools:

| Tool | Description |
|------|-------------|
| `list_products` | List products by category |
| `get_product` | Get product details by SKU |
| `search_products` | Search products by keyword |
| `get_customer` | Get customer information |
| `verify_customer_pin` | Verify customer identity |
| `list_orders` | List orders with filters |
| `get_order` | Get order details |
| `create_order` | Create new orders |

## Example Conversations

**User:** What monitors do you have?  
**Bot:** *Lists available monitors with prices and stock*

**User:** I'm looking for a wireless keyboard under $100  
**Bot:** *Searches and recommends keyboards in budget*

**User:** What's the status of order 6632c0ed-46c0-4a09-9077-024ee81d6424?  
**Bot:** *Retrieves and displays order details*

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Streamlit  │────▶│   Gemini    │────▶│ MCP Server  │
│   Chat UI   │◀────│   Flash     │◀────│ (JSON-RPC)  │
└─────────────┘     └─────────────┘     └─────────────┘
                    (via OpenRouter)
```

## Tech Stack

- **Frontend:** Streamlit
- **LLM:** Google Gemini 2.0 Flash (via OpenRouter API)
- **Backend:** MCP Server (JSON-RPC over HTTP)
- **Language:** Python 3.11+

## License

MIT
