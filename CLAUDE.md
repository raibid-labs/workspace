# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Repository Purpose

This is the **raibid-labs workspace** - the centralized Claude configuration repository for the entire raibid-labs GitHub organization (22+ repositories). It provides shared configuration, rules, templates, and tooling that all raibid-labs repos inherit.

**Key Function**: This repo defines org-wide standards, not application code. When working here, you're modifying configuration that affects all raibid-labs projects.

---

## Common Commands

### Repository Management Scripts

```bash
# Bootstrap a new repo with org config
./scripts/init-repo.sh /path/to/repo [rust-service|python-ml|typescript-docs|iac-k8s|mcp-integration]

# Validate repo compliance with org standards
./scripts/validate-repo.sh /path/to/repo

# Sync org config updates to all repos
./scripts/sync-to-repos.sh --dry-run  # Preview changes
./scripts/sync-to-repos.sh            # Apply updates

# Analyze org repository patterns
./scripts/analyze-org.sh > analysis.md

# Setup GitHub Actions for automation
./scripts/setup-github-actions.sh
```

### SPARC Methodology Commands

```bash
# List available SPARC modes
npx claude-flow sparc modes

# Run complete TDD workflow
npx claude-flow sparc tdd "feature description"

# Execute specific SPARC phase
npx claude-flow sparc run spec-pseudocode "task"
npx claude-flow sparc run architect "task"

# Parallel execution
npx claude-flow sparc batch <modes> "task"
npx claude-flow sparc pipeline "task"
```

### Testing Configuration

```bash
# Validate a template JSON file
jq . templates/repo-types/rust-service.json

# Test init script without applying
./scripts/init-repo.sh --dry-run /path/to/test-repo

# Validate all shell scripts
shellcheck scripts/*.sh
```

---

## Architecture & Structure

### Configuration Inheritance Model

```
workspace/.claude/base-project.json (org-wide base)
    ↓ extends
templates/repo-types/*.json (typed templates)
    ↓ extends
individual-repo/.claude/project.json (repo-specific)
```

**Key Principle**: Changes to `base-project.json` affect ALL repos. Changes to templates affect repos of that type. Always consider blast radius.

### Repository Organization Categories

The org has three naming patterns that dictate template usage:

1. **`dgx-*`** repos: DGX/GPU workloads → Use `python-ml.json`
2. **`hack-*`** repos: Experimental projects → Use flexible templates
3. **`raibid-*`** repos: Core infrastructure → Use `rust-service.json` or `iac-k8s.json`

### Template Files Architecture

Nine templates in `templates/repo-types/`:

- **`rust-service.json`**: Rust services (grimware, raibid-ci)
- **`python-ml.json`**: ML/AI projects with DGX optimization (dgx-pixels, dgx-music)
- **`typescript-docs.json`**: Documentation sites (docs repo)
- **`iac-k8s.json`**: Kubernetes/infrastructure (mop, hack-k8s)
- **`mcp-integration.json`**: MCP server development (ardour-mcp)
- **`library.json`**: Reusable libraries
- **`infrastructure.json`**: DevOps tooling
- **`docs.json`**: Pure documentation projects
- **`repo-claude-config.json`**: Generic fallback template

Each template:
- Extends `base-project.json`
- Defines type-specific build/test commands
- Includes language-specific rules
- Specifies appropriate MCP servers
- Provides workflow examples

### Rules Architecture

Four core rule files in `.claude/rules/`:

- **`code-style.md`**: Language-specific conventions (Rust, Python, TypeScript, Nushell)
- **`architecture.md`**: Service patterns, API design, container/K8s standards
- **`security.md`**: Secret management, dependency scanning, GPU/ML security
- **`conventions.md`**: Naming, commits (conventional), testing (80% coverage)

Three prompt files in `.claude/prompts/`:

- **`branding.md`**: raibid-labs voice/tone, terminology, engineering values
- **`review-checklist.md`**: PR review guidelines and quality gates
- **`context.md`**: Full org overview, tech stack, inter-repo dependencies

### MCP Server Configuration

`mcp/org-servers.json` defines shared MCP servers:

- **claude-flow** (required): SPARC orchestration, 54 agents
- **supermemory** (optional): Cross-session memory
- **mermaid** (optional): Architecture diagrams
- Additional: filesystem, github, git, jupyter, kubernetes, etc.

**Critical**: MCP tools coordinate strategy, Claude Code Task tool executes with real agents.

---

## Key Patterns & Conventions

### File Organization Rules

**NEVER save working files to root folder**. Organization structure:

```
/src/       - Source code
/tests/     - Test files
/docs/      - Documentation
/config/    - Configuration
/scripts/   - Utility scripts
/examples/  - Example code
```

### Concurrent Execution Pattern

**Golden Rule**: "1 Message = All Related Operations"

```bash
# ✅ CORRECT: Batch all operations in one message
[Single Message]:
  TodoWrite { todos: [5-10 todos] }
  Task("agent1", "...", "type1")
  Task("agent2", "...", "type2")
  Write "file1.ts"
  Write "file2.ts"
  Bash "mkdir -p dirs"

# ❌ WRONG: Multiple messages
Message 1: TodoWrite
Message 2: Task
Message 3: Write
```

### Template Modification Workflow

When modifying templates:

1. **Understand blast radius**: Which repos inherit this template?
2. **Test locally**: Validate JSON syntax with `jq`
3. **Consider migration**: Will existing repos need updates?
4. **Document changes**: Update template comments
5. **Sync selectively**: Use `sync-to-repos.sh` with filters

### Agent Coordination Protocol

When spawning agents via Task tool, they MUST follow hooks:

```bash
# Before work
npx claude-flow hooks pre-task --description "[task]"

# During work
npx claude-flow hooks post-edit --file "[file]"

# After work
npx claude-flow hooks post-task --task-id "[task]"
```

---

## Testing & Validation

### Validate Configuration Files

```bash
# Check JSON syntax
jq empty .claude/base-project.json
jq empty templates/repo-types/*.json

# Validate shell scripts
shellcheck scripts/*.sh

# Test script dry-run
./scripts/init-repo.sh --dry-run --verbose /tmp/test-repo
```

### Test Template Application

```bash
# Create test repo
mkdir -p /tmp/test-repo && cd /tmp/test-repo
git init

# Apply template
/path/to/workspace/scripts/init-repo.sh . rust-service

# Verify generated config
cat .claude/project.json
jq '.extends' .claude/project.json  # Should reference workspace
```

### Compliance Validation

```bash
# Check if repo follows org standards
./scripts/validate-repo.sh /path/to/repo

# Expected checks:
# - .claude/project.json exists
# - Extends base-project.json
# - Has required files (README, LICENSE, CONTRIBUTING)
# - MCP servers match org standards
```

---

## Important Constraints

### When Modifying base-project.json

- **Breaking changes require migration guide** in docs/MIGRATION.md
- **Backwards compatibility preferred** - use feature flags if needed
- **Test with at least 3 different repo types** before committing
- **Document in CHANGELOG** (if exists) or commit message

### When Creating New Templates

1. **Base it on existing patterns** from org analysis
2. **Include all required fields**: name, description, extends, rules, context
3. **Define clear build/test commands** in comments
4. **Add to template decision matrix** in docs/SETUP.md
5. **Update README.md** repo types section

### When Modifying Rules

- **Rules affect all repos** that inherit them
- **Be specific not generic** - "Use rustfmt with edition 2021" not "Format code well"
- **Include examples** - Show correct and incorrect patterns
- **Consider enforcement** - Can this be checked in CI?

### Shell Script Standards

All scripts must:
- Start with `#!/usr/bin/env bash`
- Use `set -euo pipefail`
- Include `--help` flag
- Support `--dry-run` mode
- Return proper exit codes (0=success, 1=error)
- Use color-coded output (GREEN/RED/YELLOW)

---

## Updating Org-Wide Configuration

### Standard Update Flow

```bash
# 1. Make changes to workspace repo
git checkout -b feat/update-config
# ... edit files ...
git add .
git commit -m "feat: update python-ml template for PyTorch 2.0"

# 2. Push and create PR
git push -u origin feat/update-config
gh pr create --title "feat: Update python-ml template"

# 3. After merge, sync to repos
./scripts/sync-to-repos.sh --repos "dgx-*"  # Target specific repos
# or
./scripts/sync-to-repos.sh  # All repos
```

### Emergency Hotfix

```bash
# For critical fixes (security, broken configs)
git checkout main
git pull
# ... make minimal fix ...
git add .
git commit -m "fix: critical security rule update"
git push

# Immediate sync (skip PR for emergencies)
./scripts/sync-to-repos.sh --force
```

---

## Automation & CI/CD

### GitHub Actions Setup

```bash
# Generate workflows for:
# - Validation on PRs
# - Auto-sync on config changes
# - Weekly compliance audits
./scripts/setup-github-actions.sh --all

# Selective setup
./scripts/setup-github-actions.sh --validation-only
./scripts/setup-github-actions.sh --sync-only
```

### Available Workflows (after setup)

- **validate-config.yml**: Runs on PR to validate JSON/shell scripts
- **sync-repos.yml**: Auto-syncs config to repos after merge to main
- **compliance-audit.yml**: Weekly check of all repos
- **dispatch-update.yml**: Manual trigger for org-wide updates

---

## raibid-labs Tech Stack Context

### Primary Languages & Frameworks

- **Rust**: Services, infrastructure, CLI tools (grimware, raibid-ci)
- **Python**: ML/AI workloads on DGX (dgx-*, ardour-mcp)
- **TypeScript**: Documentation sites (docs)
- **Nushell**: Cross-platform scripting (replacing Bash)
- **Just**: Task automation (replacing Make)

### Infrastructure Stack

- **Kubernetes**: Container orchestration (mop, hack-k8s)
- **Jsonnet/Tanka**: K8s templating
- **Docker**: Containerization
- **GitHub Actions**: CI/CD

### AI/ML Stack

- **PyTorch**: Deep learning framework
- **CUDA**: GPU acceleration
- **Jupyter**: Interactive development
- **DGX Systems**: Hardware platform

### Key Dependencies

- **Claude Flow** (required): SPARC orchestration, multi-agent coordination
- **MCP Protocol**: Inter-tool communication
- **GitHub CLI** (`gh`): Repository automation

---

## Available Agents (54 Total)

When using Task tool, these agents are available:

**Core Development**: coder, reviewer, tester, planner, researcher
**SPARC Methodology**: sparc-coord, sparc-coder, specification, pseudocode, architecture, refinement
**Specialized Development**: backend-dev, mobile-dev, ml-developer, cicd-engineer, api-docs, system-architect
**GitHub Integration**: github-modes, pr-manager, code-review-swarm, issue-tracker, release-manager
**Performance**: perf-analyzer, performance-benchmarker, task-orchestrator
**Swarm Coordination**: hierarchical-coordinator, mesh-coordinator, adaptive-coordinator
**Consensus & Distributed**: byzantine-coordinator, raft-manager, gossip-coordinator

Full list in `.claude/base-project.json` → agents section.

---

## Performance Benchmarks

With Claude Flow + SPARC integration:

- **84.8% SWE-Bench solve rate** (up from ~45%)
- **32.3% token reduction** (cost savings)
- **2.8-4.4x development speed** improvement
- **54 specialized agents** for complex tasks

---

## Common Workflows

### Adding Support for New Language

1. Update `.claude/rules/code-style.md` with language standards
2. Create new template in `templates/repo-types/[language]-service.json`
3. Add language-specific MCP servers to `mcp/org-servers.json` (if needed)
4. Update `docs/SETUP.md` template decision matrix
5. Test with sample repo before org-wide rollout

### Updating Security Policies

1. Edit `.claude/rules/security.md`
2. Update affected templates with new security tools
3. Create migration guide if breaking changes
4. Sync to all repos: `./scripts/sync-to-repos.sh`
5. Run compliance audit: Check validation across repos

### Deprecating Old Patterns

1. Add deprecation notice to relevant files
2. Create transition guide in `docs/MIGRATION.md`
3. Update templates to new pattern
4. Give repos 2 weeks notice before enforcement
5. Use validation script to track adoption

---

## Troubleshooting

### "Template not found" error

```bash
# Verify template exists
ls -la templates/repo-types/
# Check spelling in extends path
```

### "Cannot extend base-project.json"

```bash
# Verify GitHub access
gh auth status
# Check repo visibility (public vs private)
gh repo view raibid-labs/workspace
```

### Validation script failures

```bash
# Run with verbose mode
./scripts/validate-repo.sh --verbose /path/to/repo
# Check individual validation steps in script
```

### Sync script not updating repos

```bash
# Verify GitHub token has repo scope
gh auth refresh -s repo
# Check for .gitignore blocking .claude/
# Try with --force flag (use cautiously)
```

---

## Support & Documentation

**Primary Documentation**:
- `docs/SETUP.md` - Complete setup guide with examples
- `docs/CUSTOMIZATION.md` - Override patterns and customization
- `docs/MIGRATION.md` - Migrating existing repos
- `docs/BOOTSTRAP_REPORT.md` - Initial org configuration report

**External Resources**:
- SPARC Methodology: https://github.com/ruvnet/claude-flow
- MCP Protocol: https://modelcontextprotocol.io
- Claude Code: https://docs.claude.com/claude-code

**For Issues**:
- Workspace config issues: https://github.com/raibid-labs/workspace/issues
- SPARC/Claude Flow: https://github.com/ruvnet/claude-flow/issues
- Repo-specific: Check that repo's issue tracker

---

## Remember

- This repo defines **standards for 22+ other repos** - changes have wide impact
- Use **SPARC methodology** for systematic development workflows
- **Batch operations** in single messages for parallel execution
- **Validate before syncing** to avoid breaking downstream repos
- **Document decisions** - future maintainers will thank you
