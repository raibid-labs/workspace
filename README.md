# raibid-labs Workspace Configuration

**Centralized Claude configuration, rules, and context for the raibid-labs GitHub organization.**

---

## Purpose

This repository provides:
- **Shared configuration** that all 22+ raibid-labs repos can inherit
- **Org-wide rules** for code style, architecture, security, and conventions
- **Branding & flavor** to maintain consistency across AI/ML, infrastructure, and research projects
- **MCP server configs** for org-level tooling (Claude Flow, SPARC methodology)
- **Cross-repo context** for Claude to understand the full raibid-labs ecosystem
- **SPARC methodology** integration for Test-Driven Development workflows
- **Repository type templates** for common project patterns

---

## Repository Structure

```
workspace/
├── README.md                       # This file
├── .claude/
│   ├── base-project.json          # Base configuration for all repos
│   ├── rules/
│   │   ├── code-style.md          # Coding standards (Rust, Python, TS, Nushell)
│   │   ├── architecture.md        # Architecture patterns & best practices
│   │   ├── security.md            # Security guidelines for DGX/K8s
│   │   └── conventions.md         # Naming, structure conventions
│   └── prompts/
│       ├── branding.md            # raibid-labs voice/tone
│       ├── review-checklist.md    # PR review guidelines
│       └── context.md             # Org-level context for Claude
├── mcp/
│   ├── org-servers.json           # Shared MCP server configurations
│   └── server-configs/
│       └── README.md              # MCP setup documentation
├── templates/
│   ├── repo-claude-config.json    # Base template for new repos
│   └── repo-types/
│       ├── rust-service.json      # For Rust services (grimware, raibid-ci)
│       ├── python-ml.json         # For ML/AI projects (dgx-*)
│       ├── typescript-docs.json   # For docs sites
│       ├── iac-k8s.json           # For K8s/infrastructure
│       ├── mcp-integration.json   # For MCP servers
│       ├── library.json           # For reusable libraries
│       ├── infrastructure.json    # For DevOps/tooling
│       └── docs.json              # For documentation repos
├── docs/
│   ├── SETUP.md                   # How to add config to a repo
│   ├── CUSTOMIZATION.md           # How to override for specific repos
│   └── MIGRATION.md               # Migrating existing repos
└── scripts/
    ├── init-repo.sh               # Bootstrap new repo with config
    ├── validate-repo.sh           # Check repo compliance
    ├── sync-to-repos.sh           # Distribute config updates
    ├── analyze-org.sh             # Analyze org repo patterns
    └── setup-github-actions.sh    # Setup CI/CD automation
```

---

## raibid-labs Organization Overview

**Tech Stack:**
- **Languages**: Rust, Python, TypeScript, Nushell, Just
- **Infrastructure**: Kubernetes, Docker, Terraform
- **AI/ML**: DGX workloads, CUDA, PyTorch
- **Focus Areas**: AI/ML research, infrastructure automation, developer tooling

**Repository Categories:**

### AI/ML Workloads (dgx-*)
High-performance ML/AI projects designed for DGX systems:
- `dgx-pixels` - Computer vision & image processing
- `dgx-*` repos - Various ML research projects
- **Template**: `python-ml.json`

### Core Infrastructure (raibid-*)
Foundational infrastructure and tooling:
- `raibid-ci` - CI/CD automation & workflows
- Core infrastructure services
- **Template**: `rust-service.json` or `iac-k8s.json`

### Experimental Projects (hack-*)
Research, prototypes, and experimental work:
- Quick iterations and proof-of-concepts
- Innovation sandbox
- **Template**: Flexible, often `library.json`

### Documentation & Resources
- `docs` - Centralized documentation site
- `workspace` - This org-wide config repo
- **Template**: `typescript-docs.json`

### Key Projects
- **grimware** - [Description based on repo analysis]
- **raibid-ci** - CI/CD automation platform
- **dgx-pixels** - Image processing on DGX
- **docs** - Organization documentation

**Total Repositories**: 22 non-fork repositories

---

## Usage in Individual Repos

Each repository in raibid-labs should have a `.claude/project.json` that references this config:

```json
{
  "name": "my-service",
  "description": "Description of this specific repo",
  "extends": "github:raibid-labs/workspace/.claude/base-project.json",
  "rules": {
    "org_rules": [
      "github:raibid-labs/workspace/.claude/rules/code-style.md",
      "github:raibid-labs/workspace/.claude/rules/architecture.md",
      "github:raibid-labs/workspace/.claude/rules/security.md"
    ],
    "repo_specific": [
      "./CONTRIBUTING.md",
      "./docs/ARCHITECTURE.md"
    ]
  },
  "context": {
    "org_context": "github:raibid-labs/workspace/.claude/prompts/branding.md",
    "readme": "./README.md"
  }
}
```

---

## Setup for New Repositories

### Automatic Setup (Recommended)

```bash
# From within a repo in raibid-labs
curl -fsSL https://raw.githubusercontent.com/raibid-labs/workspace/main/scripts/init-repo.sh | bash
```

### Manual Setup

1. Create `.claude/` directory in your repo
2. Copy the appropriate template config:
   ```bash
   # For a Rust service
   curl -o .claude/project.json \
     https://raw.githubusercontent.com/raibid-labs/workspace/main/templates/repo-types/rust-service.json

   # For a Python ML project
   curl -o .claude/project.json \
     https://raw.githubusercontent.com/raibid-labs/workspace/main/templates/repo-types/python-ml.json

   # For K8s infrastructure
   curl -o .claude/project.json \
     https://raw.githubusercontent.com/raibid-labs/workspace/main/templates/repo-types/iac-k8s.json
   ```
3. Update the `name` and `description` fields
4. Commit and push

---

## Configuration Inheritance

Repos can inherit and override org-level configuration:

```json
{
  "extends": "github:raibid-labs/workspace/.claude/base-project.json",
  "rules": {
    "org_rules": "inherit",     // Use all org rules
    "additional": [             // Add repo-specific rules
      "./docs/ARCHITECTURE.md",
      "./SECURITY.md"
    ]
  },
  "overrides": {                // Override specific org settings
    "language_specific": {
      "rust": {
        "edition": "2021",
        "features": ["async-std"]
      }
    }
  }
}
```

---

## Org-Wide Rules & Standards

All repositories should follow:
- ✅ Use org-approved MCP servers (defined in `mcp/org-servers.json`)
- ✅ Include `.claude/project.json` that extends base config
- ✅ Follow coding standards in `.claude/rules/code-style.md`
- ✅ Apply security best practices from `.claude/rules/security.md`
- ✅ Use raibid-labs branding/voice from `.claude/prompts/branding.md`
- ✅ Non-fork repos include standard files: README.md, LICENSE, CONTRIBUTING.md
- ✅ Follow SPARC methodology for feature development
- ✅ Use Claude Flow for complex multi-agent workflows

---

## MCP Servers

Shared MCP servers available to all repos:

### Claude Flow (Required)
```json
{
  "mcpServers": {
    "claude-flow": {
      "command": "npx",
      "args": ["-y", "claude-flow@alpha", "mcp", "start"],
      "env": {
        "CLAUDE_FLOW_ORG": "raibid-labs"
      }
    }
  }
}
```

### Optional MCP Servers
```json
{
  "ruv-swarm": {
    "command": "npx",
    "args": ["-y", "ruv-swarm", "mcp", "start"]
  },
  "flow-nexus": {
    "command": "npx",
    "args": ["-y", "flow-nexus@latest", "mcp", "start"]
  }
}
```

**Add MCP servers:**
```bash
# Claude Flow (required for SPARC)
claude mcp add claude-flow npx claude-flow@alpha mcp start

# Enhanced coordination (optional)
claude mcp add ruv-swarm npx ruv-swarm mcp start

# Cloud features (optional, requires registration)
claude mcp add flow-nexus npx flow-nexus@latest mcp start
```

---

## SPARC Methodology Integration

raibid-labs uses SPARC (Specification, Pseudocode, Architecture, Refinement, Completion) for systematic development.

### SPARC Commands

```bash
# List available modes
npx claude-flow sparc modes

# Execute specific mode
npx claude-flow sparc run <mode> "<task>"

# Run complete TDD workflow
npx claude-flow sparc tdd "<feature>"

# Get mode details
npx claude-flow sparc info <mode>
```

### SPARC Workflow Phases

1. **Specification** - Requirements analysis
   ```bash
   npx claude-flow sparc run spec-pseudocode "Add JWT authentication"
   ```

2. **Pseudocode** - Algorithm design
   ```bash
   npx claude-flow sparc run spec-pseudocode "Implement rate limiting"
   ```

3. **Architecture** - System design
   ```bash
   npx claude-flow sparc run architect "Design microservice architecture"
   ```

4. **Refinement** - TDD implementation
   ```bash
   npx claude-flow sparc tdd "User authentication service"
   ```

5. **Completion** - Integration
   ```bash
   npx claude-flow sparc run integration "Connect auth to API gateway"
   ```

### Batchtools Commands

```bash
# Parallel execution
npx claude-flow sparc batch <modes> "<task>"

# Full pipeline processing
npx claude-flow sparc pipeline "<task>"

# Multi-task processing
npx claude-flow sparc concurrent <mode> "<tasks-file>"
```

---

## Repository Types

Different repo types use specialized configs:

### Rust Services (`rust-service.json`)
For Rust-based services and tools:
- **Examples**: grimware, raibid-ci
- **Features**: Cargo integration, Rust 2021 edition, clippy rules
- **Testing**: `cargo test`, `cargo bench`

### Python ML Projects (`python-ml.json`)
For ML/AI workloads on DGX:
- **Examples**: dgx-pixels, dgx-* repos
- **Features**: PyTorch, CUDA support, Jupyter notebooks
- **Testing**: pytest, GPU-accelerated testing

### TypeScript Documentation (`typescript-docs.json`)
For documentation sites:
- **Examples**: docs repo
- **Features**: Markdown, MDX, static site generation
- **Testing**: Link checking, build validation

### Infrastructure as Code (`iac-k8s.json`)
For Kubernetes and infrastructure:
- **Examples**: K8s manifests, Terraform modules
- **Features**: YAML validation, Helm charts, Terraform
- **Testing**: Dry-run deployments, policy validation

### MCP Integration (`mcp-integration.json`)
For MCP server development:
- **Features**: MCP protocol compliance, TypeScript/Python
- **Testing**: MCP validation suite

### Libraries (`library.json`)
For reusable libraries across languages:
- **Features**: Language-specific package management
- **Testing**: Unit tests, integration tests, examples

Specify in your repo's `.claude/project.json`:

```json
{
  "extends": "github:raibid-labs/workspace/templates/repo-types/rust-service.json",
  "name": "my-rust-service",
  "description": "High-performance service in Rust"
}
```

---

## Updating Org Configuration

1. Make changes to this workspace repo
2. Create a PR for review
3. After merge, repos can pull latest:
   ```bash
   # Manual update
   ./scripts/sync-to-repos.sh

   # Or via GitHub Actions (if configured)
   gh workflow run sync-claude-config
   ```

---

## Validation

Check if a repo is compliant:

```bash
# From any raibid-labs repo
curl -fsSL https://raw.githubusercontent.com/raibid-labs/workspace/main/scripts/validate-repo.sh | bash

# Or run locally
cd workspace
./scripts/validate-repo.sh /path/to/repo
```

---

## Available Agents (54 Total)

### Core Development
`coder`, `reviewer`, `tester`, `planner`, `researcher`

### Swarm Coordination
`hierarchical-coordinator`, `mesh-coordinator`, `adaptive-coordinator`, `collective-intelligence-coordinator`, `swarm-memory-manager`

### Consensus & Distributed
`byzantine-coordinator`, `raft-manager`, `gossip-coordinator`, `consensus-builder`, `crdt-synchronizer`, `quorum-manager`, `security-manager`

### Performance & Optimization
`perf-analyzer`, `performance-benchmarker`, `task-orchestrator`, `memory-coordinator`, `smart-agent`

### GitHub & Repository
`github-modes`, `pr-manager`, `code-review-swarm`, `issue-tracker`, `release-manager`, `workflow-automation`, `project-board-sync`, `repo-architect`, `multi-repo-swarm`

### SPARC Methodology
`sparc-coord`, `sparc-coder`, `specification`, `pseudocode`, `architecture`, `refinement`

### Specialized Development
`backend-dev`, `mobile-dev`, `ml-developer`, `cicd-engineer`, `api-docs`, `system-architect`, `code-analyzer`, `base-template-generator`

### Testing & Validation
`tdd-london-swarm`, `production-validator`

### Migration & Planning
`migration-planner`, `swarm-init`

---

## Example: Full-Stack Development with SPARC

```bash
# 1. Initialize swarm coordination
npx claude-flow swarm init --topology mesh --max-agents 6

# 2. Run SPARC TDD workflow
npx claude-flow sparc tdd "REST API with authentication"

# 3. Agents coordinate automatically via hooks:
#    - Researcher: Analyze API patterns
#    - Architect: Design system architecture
#    - Coder: Implement endpoints
#    - Tester: Create test suite
#    - Reviewer: Review code quality
#    - DevOps: Setup CI/CD

# 4. Monitor progress
npx claude-flow swarm status

# 5. View results
npx claude-flow task results
```

---

## Contributing

Changes to org-wide configuration should:
1. Be discussed with engineering leadership
2. Have clear motivation and examples
3. Include migration guide for existing repos
4. Be backwards compatible when possible
5. Follow SPARC methodology for implementation

---

## Support

- **Workspace repo issues**: https://github.com/raibid-labs/workspace/issues
- **Per-repo issues**: Check that repo's `.claude/project.json`
- **SPARC documentation**: https://github.com/ruvnet/claude-flow
- **Claude Flow issues**: https://github.com/ruvnet/claude-flow/issues
- **Flow-Nexus Platform**: https://flow-nexus.ruv.io (optional cloud features)

---

## Documentation

- [SETUP.md](docs/SETUP.md) - Detailed setup instructions
- [CUSTOMIZATION.md](docs/CUSTOMIZATION.md) - Override patterns and customization
- [MIGRATION.md](docs/MIGRATION.md) - Migrating existing repos to org config

---

## Scripts

### `scripts/init-repo.sh`
Bootstrap a new repo with raibid-labs org config:
```bash
./scripts/init-repo.sh /path/to/new-repo rust-service
```

### `scripts/validate-repo.sh`
Check repo compliance with org standards:
```bash
./scripts/validate-repo.sh /path/to/repo
```

### `scripts/sync-to-repos.sh`
Distribute config updates to all repos:
```bash
./scripts/sync-to-repos.sh --dry-run  # Preview changes
./scripts/sync-to-repos.sh            # Apply updates
```

### `scripts/analyze-org.sh`
Analyze org repo patterns:
```bash
./scripts/analyze-org.sh > analysis.json
```

---

## Performance Benefits

With Claude Flow + SPARC:
- **84.8% SWE-Bench solve rate**
- **32.3% token reduction**
- **2.8-4.4x speed improvement**
- **27+ neural models**

---

## Advanced Features

- 🚀 Automatic Topology Selection
- ⚡ Parallel Execution (2.8-4.4x speed)
- 🧠 Neural Training & Pattern Recognition
- 📊 Bottleneck Analysis
- 🤖 Smart Auto-Spawning of Agents
- 🛡️ Self-Healing Workflows
- 💾 Cross-Session Memory
- 🔗 GitHub Integration
- 🎯 DGX Workload Optimization
- 🔒 K8s Security Best Practices

---

## Integration Tips

1. Start with basic swarm init for complex tasks
2. Scale agents gradually based on task complexity
3. Use shared memory for cross-agent context
4. Monitor progress with `swarm_status` tool
5. Train neural patterns from successful workflows
6. Enable hooks for automation
7. Use GitHub tools for repository management
8. Leverage DGX-specific optimizations for ML workloads
9. Apply K8s security policies for infrastructure repos

---

## Quick Reference

```bash
# Setup new repo
./scripts/init-repo.sh /path/to/repo rust-service

# Validate compliance
./scripts/validate-repo.sh /path/to/repo

# Run SPARC workflow
npx claude-flow sparc tdd "feature description"

# Add MCP server
claude mcp add claude-flow npx claude-flow@alpha mcp start

# Sync config updates
./scripts/sync-to-repos.sh

# Analyze org
./scripts/analyze-org.sh
```

---

## License

This workspace configuration is maintained by raibid-labs. See individual repositories for their specific licenses.

---

**Remember**: Claude Flow coordinates, Claude Code creates!

For questions or support, open an issue in this repository or reach out to the raibid-labs team.
