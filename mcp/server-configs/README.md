# Raibid Labs MCP Server Configuration

Organization-wide Model Context Protocol (MCP) server configuration for AI/ML development workflows.

## Overview

This directory contains the organization's standardized MCP server configurations that enable enhanced capabilities across all raibid-labs repositories.

## Available MCP Servers

### Required Servers

#### claude-flow (REQUIRED)
SPARC methodology orchestration with swarm coordination for Test-Driven Development workflows.

```bash
# Add to any repo
claude mcp add claude-flow npx claude-flow@alpha mcp start
```

**Features:**
- Swarm coordination and agent spawning
- SPARC methodology (Specification, Pseudocode, Architecture, Refinement, Completion)
- Task orchestration and memory management
- Neural training and pattern learning
- GitHub integration
- Auto-hooks for pre/post operations

**Usage:**
```bash
# List SPARC modes
npx claude-flow sparc modes

# Run TDD workflow
npx claude-flow sparc tdd "feature description"

# Check swarm status
npx claude-flow swarm status
```

### Recommended Servers

#### filesystem
File system access scoped to raibid-labs organization repositories.

```bash
claude mcp add filesystem npx -y @modelcontextprotocol/server-filesystem /Users/beengud/raibid-labs
```

#### github
GitHub API integration for repository management and automation.

```bash
# Requires GITHUB_TOKEN environment variable
export GITHUB_TOKEN="ghp_your_token_here"
claude mcp add github npx -y @modelcontextprotocol/server-github
```

#### git
Git operations and repository management.

```bash
claude mcp add git npx -y @modelcontextprotocol/server-git
```

#### memory
Persistent memory for cross-session context and learning.

```bash
claude mcp add memory npx -y @modelcontextprotocol/server-memory
```

### AI/ML Development Servers

#### python-lsp
Python language server for AI/ML development with code intelligence.

```bash
claude mcp add python-lsp npx -y @modelcontextprotocol/server-python-lsp
```

#### jupyter
Jupyter notebook integration for AI/ML experiments and data exploration.

```bash
claude mcp add jupyter npx -y @modelcontextprotocol/server-jupyter
```

#### postgres
PostgreSQL database operations for AI/ML data pipelines.

```bash
# Requires DATABASE_URL environment variable
export DATABASE_URL="postgresql://user:pass@localhost:5432/dbname"
claude mcp add postgres npx -y @modelcontextprotocol/server-postgres
```

#### sqlite
SQLite database operations for local AI/ML experiments.

```bash
claude mcp add sqlite npx -y @modelcontextprotocol/server-sqlite
```

### Rust Development Servers

#### rust-analyzer
Rust language server integration (requires rust-analyzer installed).

```bash
# Ensure rust-analyzer is installed
rustup component add rust-analyzer

# Add MCP server
claude mcp add rust-analyzer rust-analyzer --mcp
```

### Optional Advanced Servers

#### ruv-swarm
Enhanced swarm coordination with advanced agent patterns.

```bash
claude mcp add ruv-swarm npx ruv-swarm mcp start
```

#### flow-nexus (Requires Authentication)
Cloud-based orchestration with 70+ tools for sandboxes, neural AI, and GitHub.

```bash
# Register first
npx flow-nexus@latest register

# Then login
npx flow-nexus@latest login

# Add server
claude mcp add flow-nexus npx flow-nexus@latest mcp start
```

**Features:**
- Cloud sandbox execution
- Pre-built project templates
- Advanced neural AI features
- Real-time monitoring
- Cloud storage

#### kubernetes
Kubernetes cluster management for ML workload orchestration.

```bash
# Requires KUBECONFIG environment variable
export KUBECONFIG="/path/to/kubeconfig"
claude mcp add kubernetes npx -y @modelcontextprotocol/server-kubernetes
```

#### prometheus
Prometheus metrics for ML model monitoring.

```bash
# Requires PROMETHEUS_URL environment variable
export PROMETHEUS_URL="http://prometheus:9090"
claude mcp add prometheus npx -y @modelcontextprotocol/server-prometheus
```

## Installation

### Quick Start

Install the essential servers for raibid-labs development:

```bash
# Required
claude mcp add claude-flow npx claude-flow@alpha mcp start

# Recommended
claude mcp add filesystem npx -y @modelcontextprotocol/server-filesystem /Users/beengud/raibid-labs
claude mcp add github npx -y @modelcontextprotocol/server-github
claude mcp add git npx -y @modelcontextprotocol/server-git
claude mcp add memory npx -y @modelcontextprotocol/server-memory
```

### AI/ML Development Stack

```bash
# Python development
claude mcp add python-lsp npx -y @modelcontextprotocol/server-python-lsp
claude mcp add jupyter npx -y @modelcontextprotocol/server-jupyter

# Data storage
claude mcp add postgres npx -y @modelcontextprotocol/server-postgres
claude mcp add sqlite npx -y @modelcontextprotocol/server-sqlite
```

### Full Stack

```bash
# Copy org-servers.json to your repo
cp /Users/beengud/raibid-labs/workspace/mcp/org-servers.json ~/.config/claude/mcp.json

# Enable specific servers by setting disabled: false in the config
```

## Adding a New Org-Wide MCP Server

### 1. Evaluate the Server

Before adding a new org-wide MCP server:

- **Purpose**: Does it solve a common need across multiple repos?
- **Maintenance**: Is it actively maintained?
- **Dependencies**: What are the prerequisites?
- **Security**: Does it require sensitive credentials?
- **Performance**: What is the resource impact?

### 2. Test in a Single Repo

```bash
# Test the server in one repo first
cd /path/to/test-repo
claude mcp add test-server npx -y @example/mcp-server

# Verify functionality
# Document any issues or configuration needs
```

### 3. Add to org-servers.json

Edit `/Users/beengud/raibid-labs/workspace/mcp/org-servers.json`:

```json
{
  "mcpServers": {
    "new-server": {
      "command": "npx",
      "args": ["-y", "@example/mcp-server"],
      "description": "Brief description of what this server does",
      "tags": ["category", "purpose", "optional|recommended|required"],
      "disabled": true,
      "env": {
        "SERVER_API_KEY": "${SERVER_API_KEY}"
      }
    }
  }
}
```

### 4. Document in README

Add a section to this README with:

- Installation instructions
- Required environment variables
- Usage examples
- Common troubleshooting

### 5. Announce to Team

- Create an announcement in team channels
- Update any onboarding documentation
- Add to relevant project templates

## Using Org MCP Servers in Your Repo

### Option 1: Reference Org Config

Create a `.claude/mcp.json` in your repo:

```json
{
  "extends": "/Users/beengud/raibid-labs/workspace/mcp/org-servers.json",
  "mcpServers": {
    "claude-flow": {
      "disabled": false
    },
    "filesystem": {
      "disabled": false
    },
    "github": {
      "disabled": false
    }
  }
}
```

### Option 2: Copy and Customize

```bash
# Copy org config
cp /Users/beengud/raibid-labs/workspace/mcp/org-servers.json .claude/mcp.json

# Edit to enable/disable servers for your repo
# Add repo-specific servers if needed
```

### Option 3: Selective Installation

```bash
# Install only the servers you need
claude mcp add claude-flow npx claude-flow@alpha mcp start
claude mcp add filesystem npx -y @modelcontextprotocol/server-filesystem /path/to/your/repo
```

## Environment Variables

Many MCP servers require environment variables. Set these in your shell or `.env` file:

```bash
# GitHub
export GITHUB_TOKEN="ghp_your_token_here"

# PostgreSQL
export DATABASE_URL="postgresql://user:pass@localhost:5432/dbname"

# AWS
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
export AWS_REGION="us-east-1"

# Kubernetes
export KUBECONFIG="/path/to/kubeconfig"

# Prometheus
export PROMETHEUS_URL="http://prometheus:9090"

# Slack
export SLACK_BOT_TOKEN="xoxb-your-token"
export SLACK_TEAM_ID="T1234567890"

# Brave Search
export BRAVE_API_KEY="your_api_key"
```

## SPARC Methodology with Claude Flow

Claude Flow provides the SPARC (Specification, Pseudocode, Architecture, Refinement, Completion) methodology for systematic TDD.

### SPARC Phases

1. **Specification**: Requirements analysis and feature specification
2. **Pseudocode**: Algorithm design and logic planning
3. **Architecture**: System design and component structure
4. **Refinement**: TDD implementation with red-green-refactor
5. **Completion**: Integration and final testing

### Common Commands

```bash
# List available modes
npx claude-flow sparc modes

# Run TDD workflow
npx claude-flow sparc tdd "user authentication feature"

# Run specific mode
npx claude-flow sparc run architect "design microservices architecture"

# Batch parallel execution
npx claude-flow sparc batch spec-pseudocode,architect "payment processing"

# Full pipeline
npx claude-flow sparc pipeline "user registration system"
```

### Agent Coordination

Claude Flow spawns specialized agents for different tasks:

- **researcher**: Requirements analysis and pattern research
- **coder**: Implementation and coding
- **tester**: Test creation and validation
- **reviewer**: Code review and quality assurance
- **architect**: System design and architecture

### Hooks Integration

Claude Flow provides automatic hooks for coordination:

```bash
# Pre-task hook (run before work)
npx claude-flow@alpha hooks pre-task --description "implement feature"

# Post-edit hook (run after file changes)
npx claude-flow@alpha hooks post-edit --file "src/feature.rs"

# Post-task hook (run after work)
npx claude-flow@alpha hooks post-task --task-id "task-123"

# Session management
npx claude-flow@alpha hooks session-restore --session-id "swarm-abc"
npx claude-flow@alpha hooks session-end --export-metrics true
```

## Best Practices

### 1. Concurrent Operations

Always batch related operations in a single message:

```javascript
// ✅ CORRECT: All operations in one message
[Single Message]:
  Task("Research agent", "Analyze requirements...", "researcher")
  Task("Coder agent", "Implement features...", "coder")
  Task("Tester agent", "Create tests...", "tester")
  TodoWrite { todos: [...10 todos...] }
  Write "src/feature.rs"
  Write "tests/feature_test.rs"

// ❌ WRONG: Multiple messages
Message 1: Task("Research agent", ...)
Message 2: Task("Coder agent", ...)
Message 3: Write file
```

### 2. File Organization

Never save working files to the root folder:

```bash
# ✅ CORRECT
/src/          # Source code
/tests/        # Test files
/docs/         # Documentation
/config/       # Configuration
/scripts/      # Utility scripts
/examples/     # Example code

# ❌ WRONG
/feature.rs    # No files in root
/test.md       # No docs in root
```

### 3. Security

- Never commit API keys or secrets
- Use environment variables for credentials
- Add secrets to `.gitignore`
- Rotate tokens regularly

### 4. Performance

- Enable only needed servers (disable unused ones)
- Use `disabled: true` for optional servers
- Monitor resource usage with hooks
- Clean up old sessions

## Troubleshooting

### MCP Server Not Starting

```bash
# Check if server is installed
which claude-flow
npm list -g claude-flow

# Reinstall if needed
npm install -g claude-flow@alpha

# Check logs
tail -f ~/.config/claude/logs/mcp.log
```

### Authentication Issues

```bash
# Verify environment variables
env | grep GITHUB_TOKEN
env | grep DATABASE_URL

# Re-export if needed
export GITHUB_TOKEN="ghp_new_token"

# Test GitHub connection
gh auth status
```

### Performance Issues

```bash
# Check running MCP servers
ps aux | grep mcp

# Monitor resource usage
npx claude-flow@alpha hooks session-end --export-metrics true

# Disable unused servers
# Edit mcp.json and set disabled: true
```

## Examples

### Example 1: Full-Stack AI/ML Project

```bash
# Initialize with SPARC
npx claude-flow sparc tdd "ML model serving API"

# Agents will coordinate to:
# 1. Research best practices (researcher)
# 2. Design architecture (architect)
# 3. Implement API (coder)
# 4. Create tests (tester)
# 5. Review code (reviewer)

# All operations happen in parallel with automatic coordination
```

### Example 2: Rust Microservice

```bash
# Enable Rust development servers
claude mcp add rust-analyzer rust-analyzer --mcp

# Run SPARC TDD workflow
npx claude-flow sparc tdd "authentication microservice with JWT"

# Agents spawn concurrently:
# - researcher: Analyze auth patterns
# - architect: Design service architecture
# - coder: Implement in Rust
# - tester: Create integration tests
```

### Example 3: Data Pipeline

```bash
# Enable database servers
claude mcp add postgres npx -y @modelcontextprotocol/server-postgres
claude mcp add jupyter npx -y @modelcontextprotocol/server-jupyter

# Run SPARC pipeline
npx claude-flow sparc pipeline "ETL pipeline for ML training data"

# Full workflow:
# 1. Specification phase
# 2. Pseudocode design
# 3. Architecture planning
# 4. TDD refinement
# 5. Integration completion
```

## Support

- **Claude Flow Documentation**: https://github.com/ruvnet/claude-flow
- **MCP Protocol**: https://modelcontextprotocol.io
- **Organization Issues**: File in raibid-labs/workspace repository

## Contributing

To contribute improvements to the org MCP configuration:

1. Test changes in your repo first
2. Create a PR with your changes
3. Document new servers thoroughly
4. Update this README
5. Announce changes to the team

---

**Remember**: Claude Flow coordinates, Claude Code creates! MCP tools handle coordination while Claude Code's Task tool executes the actual work.
