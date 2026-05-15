# Environment Setup

This project uses environment variables for MCP authentication. Keep real credentials out of version control.

## Required Variables
- `CONTEXT7_API_KEY`
- `GITHUB_PERSONAL_ACCESS_TOKEN`
- `MAPBOX_ACCESS_TOKEN`

## Quick Setup (Current Shell)
```bash
export CONTEXT7_API_KEY="your_context7_key"
export GITHUB_PERSONAL_ACCESS_TOKEN="your_github_pat"
export MAPBOX_ACCESS_TOKEN="your_mapbox_token"
```

## Notes
- `.env.example` is a template only; never place real tokens in tracked files.
- `.vscode/mcp.json` references these values via `${env:...}` placeholders.