# TechGear Pro Customer Support Chatbot

A customer support chatbot prototype for a computer products company, built with:
- **Gradio** - Modern web UI
- **Google Gemini Flash** - Fast, cost-effective LLM
- **MCP Server** - Real-time product and order data

## Features

- 🔍 **Product Search** - Find monitors, printers, accessories, and networking equipment
- 📦 **Order Management** - Check order status and details
- 🛒 **Order Creation** - Place new orders (with customer verification)
- 💬 **Natural Language** - Ask questions in plain English

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
export GOOGLE_API_KEY="your-gemini-api-key"
```

Get a free API key from: https://makersuite.google.com/app/apikey

### 3. Run Locally

```bash
python app.py
```

Open http://localhost:7860 in your browser.

## Deployment to HuggingFace Spaces

1. Create a new Space on [HuggingFace](https://huggingface.co/spaces)
2. Select "Gradio" as the SDK
3. Upload these files:
   - `app.py`
   - `mcp_client.py`
   - `requirements.txt`
4. Add your `GOOGLE_API_KEY` as a secret in Space settings

## MCP Server Integration

This chatbot connects to the company's MCP server which provides:

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
│   Gradio    │────▶│   Gemini    │────▶│ MCP Server  │
│     UI      │◀────│   Flash     │◀────│  (Orders)   │
└─────────────┘     └─────────────┘     └─────────────┘
```

## License

MIT
