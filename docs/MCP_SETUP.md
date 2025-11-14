# MCP Server Setup Guide

This guide explains how to configure MCP servers for raibid-labs repositories.

## raibid-labs-mcp Server

The `raibid-labs-mcp` server provides organization context and repository management tools. It's disabled by default in all repos and requires GitHub App authentication.

### Setup GitHub App

1. **Create a GitHub App** (if not already created):
   - Go to: https://github.com/organizations/raibid-labs/settings/apps/new
   - Name: `raibid-labs-mcp-server` (or similar)
   - Homepage URL: `https://github.com/raibid-labs/raibid-labs-mcp`
   - Webhook: Uncheck "Active"

2. **Set Repository Permissions**:
   - Contents: Read-only
   - Metadata: Read-only
   - Pull requests: Read-only
   - Issues: Read-only

3. **Generate Private Key**:
   - After creating the app, scroll down to "Private keys"
   - Click "Generate a private key"
   - Save the downloaded `.pem` file securely

4. **Install the App**:
   - Go to: https://github.com/organizations/raibid-labs/settings/apps/[your-app-name]
   - Click "Install App"
   - Select "All repositories" or specific repos
   - Note the Installation ID from the URL after installation

### Configure Environment Variables

Add these to your shell profile (`~/.zshrc`, `~/.bashrc`, etc.):

```bash
# GitHub App credentials for raibid-labs-mcp
export GITHUB_APP_ID="123456"                      # From app settings page
export GITHUB_INSTALLATION_ID="87654321"           # From installation URL
export GITHUB_PRIVATE_KEY="$(cat /path/to/app.pem)" # Or paste the key directly
```

**Alternative**: Use a dedicated key file:

```bash
export GITHUB_APP_ID="123456"
export GITHUB_INSTALLATION_ID="87654321"
export GITHUB_PRIVATE_KEY_PATH="/path/to/raibid-labs-mcp.pem"
```

Then modify your shell to read the key:
```bash
export GITHUB_PRIVATE_KEY="$(cat $GITHUB_PRIVATE_KEY_PATH)"
```

### Enable the MCP Server

In any raibid-labs repository:

```bash
# Check available MCP servers
/mcp

# Enable raibid-labs-mcp
/mcp enable raibid-labs-mcp

# Verify it's running
/mcp status
```

### Security Notes

- **Never commit** the private key or `.pem` file to git
- Store the private key securely (1Password, encrypted file, etc.)
- Use environment variables to inject credentials
- The GitHub App provides better security than personal access tokens:
  - Granular permissions
  - Organization-level control
  - Audit logging
  - Easy revocation

### Troubleshooting

**Error: Missing required environment variables**
```
Solution: Ensure GITHUB_APP_ID, GITHUB_PRIVATE_KEY, and GITHUB_ORG are set
```

**Error: Authentication failed**
```
Solution: Verify the GitHub App is installed on the raibid-labs organization
```

**Error: Private key format invalid**
```
Solution: Ensure the entire PEM file content is in GITHUB_PRIVATE_KEY, including:
-----BEGIN RSA PRIVATE KEY-----
...
-----END RSA PRIVATE KEY-----
```

## Other MCP Servers

### claude-flow (required)

Enabled by default for all repos. No configuration needed.

```bash
npx claude-flow@alpha mcp start
```

### supermemory (optional)

Requires API credentials from supermemory.ai:

```bash
export SUPERMEMORY_API_KEY="your-api-key"
export SUPERMEMORY_PROJECT_ID="your-project-id"
```

### mermaid (optional)

No configuration required. Provides diagram generation:

```bash
/mcp enable mermaid
```
