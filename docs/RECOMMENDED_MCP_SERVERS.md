# Recommended MCP Servers & Extensions for raibid-labs

Based on research of the MCP ecosystem (as of January 2025), here are recommended tools that complement raibid-labs' tech stack and workflows.

## Already Integrated ✅

- **claude-flow** - Multi-agent orchestration (required, already enabled)
- **supermemory** - Organizational memory (already configured)
- **mermaid** - Architecture diagrams (already configured)
- **raibid-labs-mcp** - Org context server (disabled by default)

---

## High Priority Recommendations

### 🏗️ Infrastructure & DevOps

#### Kubernetes MCP Server
**Repo**: `containers/kubernetes-mcp-server` (Red Hat/Containers)
**Why**: Native Go implementation that interacts directly with K8s API (not just kubectl wrapper)
**Features**:
- Multi-cluster management
- Native Kubernetes and OpenShift support
- 50+ built-in DevOps tools
- Real-time cluster health monitoring
- AI-driven resource management

**Setup**:
```bash
npx @containers/kubernetes-mcp-server
```

**raibid-labs Use Case**: Perfect for mop, hack-k8s repos. Enables AI-assisted K8s management.

---

#### kubectl-mcp-server
**Repo**: `Flux159/mcp-server-kubernetes`
**Why**: Simpler alternative if you prefer kubectl-based interactions
**Features**:
- Natural language K8s operations
- Pod/service/deployment management
- Log retrieval and analysis

**raibid-labs Use Case**: Lighter option for basic K8s operations.

---

### 🤖 AI/ML Development

#### PyTorch Documentation Search MCP
**Repo**: `seanmichaelmcgee/pytorch-docs`
**Why**: Semantic search over PyTorch docs for DGX workloads
**Features**:
- Vector embeddings for doc search
- API reference lookup
- Code example retrieval
- Error message explanations

**raibid-labs Use Case**: Essential for dgx-* repos (dgx-pixels, dgx-music, dgx-spark).

**Setup**:
```bash
npx pytorch-docs-mcp
```

---

#### PyTorch HUD MCP
**Repo**: `izaitsevfb/pytorch-treehugger`
**Why**: CI/CD analytics for PyTorch projects
**Features**:
- Job logs access
- Build analytics
- Performance metrics

**raibid-labs Use Case**: Monitor ML pipeline health in DGX repos.

---

### 📊 Database & Observability

#### Postgres MCP Pro
**Repo**: `crystaldba/postgres-mcp`
**Why**: Not just queries - includes performance analysis and auto-tuning
**Features**:
- PgHero health checks integration
- Database Tuning Advisor algorithm
- Hypothetical index simulation
- Query plan analysis
- Read/write access with safety controls

**raibid-labs Use Case**: Any repos using PostgreSQL. Auto-tune database performance.

**Setup**:
```bash
npx @crystaldba/postgres-mcp
```

---

#### Prometheus MCP Server
**Why**: Monitor infrastructure metrics from Claude
**Features**:
- Query Prometheus metrics
- Alert analysis
- Performance trending

**raibid-labs Use Case**: Integrate with mop observability stack (LGTM).

---

#### Dynatrace / Last9 MCP
**Why**: Full observability (metrics, logs, traces)
**Features**:
- AI-powered performance insights
- Distributed tracing analysis
- Log aggregation

**raibid-labs Use Case**: Production monitoring for deployed services.

---

### 🔧 Development Tools

#### Official Anthropic MCP Servers
**Repo**: `modelcontextprotocol/servers`

Essential servers from the official collection:

**1. Git MCP**
```bash
npx @modelcontextprotocol/server-git
```
- Read/search/manipulate git repos
- Commit history analysis
- Branch management

**2. GitHub MCP**
```bash
npx @modelcontextprotocol/server-github
```
- Repository management
- PR/issue operations
- GitHub API integration

**3. Filesystem MCP**
```bash
npx @modelcontextprotocol/server-filesystem
```
- Secure file operations
- Directory traversal
- File search and manipulation

**raibid-labs Use Case**: Core development operations across all repos.

---

#### Docker MCP Toolkit
**Why**: 200+ pre-built containerized MCP servers
**Features**:
- One-click deployment
- Automatic credential handling
- Easy updates

**raibid-labs Use Case**: Simplify MCP server management org-wide.

**Access**: Via Docker Desktop Extensions

---

### 🧠 Multi-Agent Orchestration

#### wshobson/agents
**Repo**: `github.com/wshobson/agents`
**Why**: Production-ready multi-agent system with 85 agents
**Features**:
- 85 specialized agents
- 15 workflow orchestrators
- 47 agent skills
- 44 development tools
- 63 focused plugins

**raibid-labs Use Case**: Alternative/complement to claude-flow. More specialized agents.

**Note**: Overlap with our workspace/agents/ directory - evaluate if additional agents needed.

---

#### claude-squad
**Repo**: `smtg-ai/claude-squad`
**Why**: Manage multiple Claude instances in separate workspaces
**Features**:
- Parallel Claude Code agents
- Workspace isolation
- Task distribution
- Works with Claude Code, Aider, Codex

**raibid-labs Use Case**: Run multiple agents simultaneously on different repos.

---

#### Agentrooms
**URL**: `claudecode.run`
**Why**: Multi-agent development workspace with @mentions
**Features**:
- Route tasks to specialized agents
- Coordinate complex workflows
- Local and remote agents
- Open source

**raibid-labs Use Case**: Team collaboration with AI agents.

---

### 📝 Knowledge Management

#### Official Notion MCP Server
**Repo**: `makenotion/notion-mcp-server`
**Why**: Official Notion integration
**Features**:
- OAuth authentication
- Full workspace access
- Markdown-optimized API
- Read/write pages
- Task management

**raibid-labs Use Case**: If using Notion for project management.

**Setup**:
```bash
npx @makenotion/notion-mcp-server
```

---

#### Obsidian MCP Server
**Repo**: `cyanheads/obsidian-mcp-server`
**Why**: Comprehensive Obsidian vault integration
**Features**:
- Read/write/search notes
- Tag management
- Frontmatter manipulation
- Bridges to Obsidian Local REST API

**Requires**: Obsidian Local REST API plugin

**raibid-labs Use Case**: If using Obsidian for documentation/knowledge base.

---

#### Obsidian Second Brain MCP
**Repo**: `comfucios/obsidian-mcp-sb`
**Why**: AI-optimized knowledge retrieval
**Features**:
- Semantic search
- Tag filtering
- Temporal queries
- Note summarization
- No external data files needed

**raibid-labs Use Case**: AI-enhanced personal knowledge management.

---

## Medium Priority

### Project Management

- **Linear MCP** - Issue tracking (if using Linear)
- **Jira MCP** - Atlassian integration (if using Jira)
- **Asana MCP** - Task management (if using Asana)

### Communication

- **Slack MCP** - Official Slack integration
- **Discord MCP** - Discord bot integration

### Cloud Platforms

- **AWS MCP Servers** - EC2, S3, Lambda operations
- **Vercel MCP** - Deployment and preview URLs
- **Cloudflare MCP** - Edge compute and KV storage

### Testing & QA

- **Sentry MCP** - Error monitoring integration
- **Puppeteer MCP** - Browser automation and E2E testing

---

## Installation Priority Order

For raibid-labs, I recommend this rollout sequence:

### Phase 1: Infrastructure (Week 1)
1. ✅ Kubernetes MCP Server (containers/kubernetes-mcp-server)
2. ✅ Git MCP (official)
3. ✅ GitHub MCP (official)
4. ✅ Filesystem MCP (official)

### Phase 2: AI/ML (Week 2)
5. ✅ PyTorch Documentation Search MCP
6. ✅ Postgres MCP Pro

### Phase 3: Observability (Week 3)
7. ✅ Prometheus MCP
8. ✅ Choose one: Dynatrace or Last9 MCP

### Phase 4: Advanced Orchestration (Week 4)
9. ⚠️ Evaluate: claude-squad or wshobson/agents
10. ⚠️ Optional: Agentrooms for team collaboration

### Phase 5: Knowledge Management (As Needed)
11. ⚙️ Notion MCP or Obsidian MCP (based on team preference)

---

## Configuration Template

To add any MCP server to workspace base config:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["package-name"],
      "description": "What this server does",
      "disabled": true,  // Start disabled for optional servers
      "env": {
        "ENV_VAR": "${ENV_VAR}"
      }
    }
  }
}
```

---

## Resources

- **Official MCP Directory**: https://github.com/modelcontextprotocol/servers
- **PulseMCP Directory**: https://www.pulsemcp.com/servers (6,480+ servers)
- **Awesome MCP Servers**: https://github.com/wong2/awesome-mcp-servers
- **DevOps MCP Servers**: https://github.com/rohitg00/awesome-devops-mcp-servers
- **MCP Documentation**: https://modelcontextprotocol.io
- **Claude Code MCP Docs**: https://docs.anthropic.com/en/docs/claude-code/mcp

---

## Notes

- All server recommendations are based on January 2025 ecosystem state
- Test servers in non-production repos first
- Monitor token usage when enabling multiple servers
- Community servers are not endorsed by Anthropic - use at own risk
- Check server GitHub repos for latest installation instructions
- Many servers require API keys or authentication

---

## Maintenance

This document should be reviewed quarterly as the MCP ecosystem evolves rapidly.

**Last Updated**: January 2025
**Next Review**: April 2025
