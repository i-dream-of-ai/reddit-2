# Contributing to Reddit MCP

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature (`git checkout -b feature/amazing-feature`)
4. Make your changes
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

1. Set up your Python environment (we recommend using `uv`)

```bash
uv sync
```

2. Create a `.env` file in the project root with your Reddit API credentials:

```sh
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret
```

## Running your dev server

### Claude Desktop

Add the following to your Claude Desktop configuration file:

```json
{
  "mcpServers": {
    "reddit": {
      "command": "<absolute path to your uv executable>",
      "args": [
        "run",
        "--directory",
        "<absolute path to the project root>",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "main.py"
      ]
    }
  }
}
```

### Running directly

```bash
uv run main.py
```

### MCP Inspector

```bash
npx @modelcontextprotocol/inspector $(which uv) --directory <absolute path to the project root> run main.py
```

## Testing

Run the test suite:

```bash
uv run pytest
```

## Development Tools

Check tool schemas:

```bash
uv run dump-schemas
```
