# Claude Organization Configuration - Complete Bootstrap Package

**Version**: 1.0  
**Created**: 2025-11-12  
**Purpose**: Bootstrap centralized Claude configuration for an entire GitHub organization

---

## 📦 Package Contents

This file contains everything you need to set up org-wide Claude configuration:

1. [Quick Start Instructions](#-quick-start-instructions)
2. [File 1: README.md for Config Repo](#file-1-readmemd-for-config-repo)
3. [File 2: Bootstrap Prompt for Claude Code](#file-2-bootstrap-prompt-for-claude-code)
4. [File 3: Detailed Quick Start Guide](#file-3-detailed-quick-start-guide)
5. [How to Extract Files](#-how-to-extract-files)

---

## 🚀 Quick Start Instructions

**What you'll do:**
1. Create/navigate to your `claude-org-config` repository
2. Copy the README (File 1) into your repo
3. Start Claude Code and paste the Bootstrap Prompt (File 2)
4. Follow the interactive process to analyze and configure all repos

**Prerequisites:**
- GitHub org with repos you want to configure
- `gh` CLI installed and authenticated
- Claude Code installed

**Estimated time:** 15-30 minutes (depending on org size)

---

# File 1: README.md for Config Repo

**Save as:** `README.md` in your `claude-org-config` repository

```markdown
# Claude Organization Configuration

**Centralized Claude configuration, rules, and context for the entire GitHub organization.**

## Purpose

This repository provides:
- **Shared configuration** that all repos can inherit
- **Org-wide rules** for code style, architecture, and conventions
- **Branding & flavor** to maintain consistency across projects
- **MCP server configs** for org-level tooling
- **Cross-repo context** for Claude to understand the full organization

## Repository Structure

```
claude-org-config/
├── .claude/
│   ├── base-project.json      # Base configuration for all repos
│   ├── rules/
│   │   ├── code-style.md      # Coding standards
│   │   ├── architecture.md    # Architecture patterns
│   │   └── conventions.md     # Naming, structure conventions
│   └── prompts/
│       ├── branding.md        # Org voice/tone
│       └── review-checklist.md
├── mcp/
│   ├── org-servers.json       # Shared MCP server configurations
│   └── server-configs/
├── templates/
│   ├── repo-claude-config.json  # Template for new repos
│   └── repo-types/              # Config by repo type
│       ├── service.json
│       ├── library.json
│       └── infrastructure.json
├── docs/
│   ├── SETUP.md               # How to add this config to a repo
│   └── CUSTOMIZATION.md       # How to override for specific repos
└── scripts/
    ├── sync-to-repos.sh       # Distribute config updates
    ├── validate-repo.sh       # Check repo compliance
    └── init-repo.sh           # Bootstrap new repo
```

## Usage in Individual Repos

Each repository in the org should have a `.claude/project.json` that references this config:

```json
{
  "name": "my-service",
  "description": "Description of this specific repo",
  "extends": "github:yourorg/claude-org-config/.claude/base-project.json",
  "rules": {
    "org_rules": [
      "github:yourorg/claude-org-config/.claude/rules/code-style.md",
      "github:yourorg/claude-org-config/.claude/rules/architecture.md"
    ],
    "repo_specific": [
      "./CONTRIBUTING.md"
    ]
  },
  "context": {
    "org_context": "github:yourorg/claude-org-config/.claude/prompts/branding.md"
  }
}
```

## Setup for New Repositories

### Automatic Setup (Recommended)

```bash
# From within a repo in the org
curl -fsSL https://raw.githubusercontent.com/yourorg/claude-org-config/main/scripts/init-repo.sh | bash
```

### Manual Setup

1. Create `.claude/` directory in your repo
2. Copy the template config:
   ```bash
   curl -o .claude/project.json \
     https://raw.githubusercontent.com/yourorg/claude-org-config/main/templates/repo-claude-config.json
   ```
3. Update the `name` and `description` fields
4. Commit and push

## Configuration Inheritance

Repos can inherit and override org-level configuration:

```json
{
  "extends": "github:yourorg/claude-org-config/.claude/base-project.json",
  "rules": {
    "org_rules": "inherit",  // Use all org rules
    "additional": [          // Add repo-specific rules
      "./docs/ARCHITECTURE.md"
    ]
  },
  "overrides": {            // Override specific org settings
    "style": "repo-specific-style"
  }
}
```

## Org-Wide Rules & Standards

All repositories should follow:
- ✅ Use org-approved MCP servers (defined in `mcp/org-servers.json`)
- ✅ Include `.claude/project.json` that extends base config
- ✅ Follow coding standards in `.claude/rules/code-style.md`
- ✅ Apply org branding/voice from `.claude/prompts/branding.md`
- ✅ Non-fork repos include standard files: README.md, LICENSE, CONTRIBUTING.md

## MCP Servers

Shared MCP servers available to all repos:

```json
{
  "mcpServers": {
    "org-context": {
      "command": "npx",
      "args": ["-y", "@yourorg/org-context-server"],
      "env": {
        "GITHUB_ORG": "yourorg"
      }
    },
    "repo-standards": {
      "command": "npx",
      "args": ["-y", "@yourorg/standards-validator"]
    }
  }
}
```

## Updating Org Configuration

1. Make changes to this repo
2. Create a PR for review
3. After merge, repos can pull latest:
   ```bash
   # Manual update
   ./scripts/sync-to-repos.sh
   
   # Or via GitHub Actions (if configured)
   gh workflow run sync-claude-config
   ```

## Validation

Check if a repo is compliant:

```bash
# From any org repo
curl -fsSL https://raw.githubusercontent.com/yourorg/claude-org-config/main/scripts/validate-repo.sh | bash
```

## Repository Types

Different repo types can use specialized configs:

- **Service repos**: `templates/repo-types/service.json`
- **Library repos**: `templates/repo-types/library.json`
- **Infrastructure**: `templates/repo-types/infrastructure.json`

Specify in your repo's `.claude/project.json`:

```json
{
  "extends": "github:yourorg/claude-org-config/templates/repo-types/service.json",
  "name": "my-service"
}
```

## Contributing

Changes to org-wide configuration should:
1. Be discussed with engineering leadership
2. Have clear motivation and examples
3. Include migration guide for existing repos
4. Be backwards compatible when possible

## Questions?

- See [docs/SETUP.md](docs/SETUP.md) for detailed setup instructions
- See [docs/CUSTOMIZATION.md](docs/CUSTOMIZATION.md) for override patterns
- Open an issue for org-wide config questions
```

---

# File 2: Bootstrap Prompt for Claude Code

**Usage:** Copy this entire section and paste it into Claude Code

```markdown
# CLAUDE CODE BOOTSTRAP PROMPT

## Context

I have created a new GitHub repository called `claude-org-config` (or similar name) that will contain centralized Claude configuration for my entire GitHub organization. I need you to:

1. **Analyze all repositories** in my GitHub organization to understand common patterns
2. **Bootstrap the `claude-org-config` repository** with appropriate structure and content
3. **Create `.claude/project.json` files** in each existing repo that reference the org-level config

## My GitHub Organization Details

- **Organization name**: [YOUR_ORG_NAME]
- **Config repo name**: [YOUR_CONFIG_REPO_NAME] (e.g., `claude-org-config`)
- **Number of repos (approx)**: [NUMBER]
- **My GitHub token**: Available in environment as `GITHUB_TOKEN` or `GH_TOKEN`

## Step 1: Analyze Organization Repositories

First, discover and analyze all repositories in the organization:

```bash
# List all repos in the org (non-archived, excluding forks by default)
gh repo list [ORG_NAME] --limit 1000 --json name,description,primaryLanguage,isPrivate,isFork,languages,createdAt,updatedAt
```

For each repository, analyze:
- **Primary language(s)** - to create language-specific rules
- **Repository type** - service, library, infrastructure, docs, etc.
- **Common patterns** - shared dependencies, naming conventions, structure
- **Existing `.claude/` configs** - what's already there
- **Tech stack** - frameworks, tools, platforms

**Output a summary table** showing:
- Repo name
- Type (service/library/infra/etc)
- Primary language
- Has existing .claude config? (yes/no)
- Key characteristics

## Step 2: Create the Config Repository Structure

In the `claude-org-config` repository, create this structure:

```
claude-org-config/
├── README.md                          # Already provided, enhance based on org analysis
├── .claude/
│   ├── base-project.json              # Base config all repos inherit
│   ├── rules/
│   │   ├── code-style.md              # Extract from existing repos
│   │   ├── architecture.md            # Common architecture patterns
│   │   ├── security.md                # Security best practices
│   │   └── conventions.md             # Naming, structure conventions
│   └── prompts/
│       ├── branding.md                # Org voice/tone
│       ├── review-checklist.md        # What to check in PRs
│       └── context.md                 # Org-level context for Claude
├── mcp/
│   ├── org-servers.json               # Shared MCP server configurations
│   └── server-configs/
│       └── README.md
├── templates/
│   ├── repo-claude-config.json        # Base template for new repos
│   └── repo-types/
│       ├── typescript-service.json    # For TS/Node services
│       ├── python-service.json        # For Python services
│       ├── go-service.json            # For Go services
│       ├── library.json               # For libraries
│       ├── infrastructure.json        # For IaC/Kubernetes repos
│       └── docs.json                  # For documentation repos
├── docs/
│   ├── SETUP.md                       # How to add config to a repo
│   ├── CUSTOMIZATION.md               # How to override
│   └── MIGRATION.md                   # Migrating existing repos
└── scripts/
    ├── sync-to-repos.sh               # Distribute updates
    ├── validate-repo.sh               # Check compliance
    ├── init-repo.sh                   # Bootstrap new repo
    └── analyze-org.sh                 # Repo analysis script
```

### Critical Files to Generate

#### 1. `.claude/base-project.json`
Based on org analysis, create a base configuration with:
- Common MCP servers used across repos
- Shared rules all repos should follow
- Org-level context
- Default knowledge sources

```json
{
  "schema_version": "1.0",
  "name": "org-base-config",
  "description": "Base Claude configuration for all [ORG_NAME] repositories",
  "rules": [
    "github:[ORG_NAME]/claude-org-config/.claude/rules/code-style.md",
    "github:[ORG_NAME]/claude-org-config/.claude/rules/architecture.md",
    "github:[ORG_NAME]/claude-org-config/.claude/rules/conventions.md"
  ],
  "context": {
    "org_branding": "github:[ORG_NAME]/claude-org-config/.claude/prompts/branding.md",
    "org_standards": "github:[ORG_NAME]/claude-org-config/.claude/prompts/context.md"
  },
  "mcp_servers": {
    // Based on analysis, include commonly used MCP servers
  },
  "preferred_tools": [
    // List based on org analysis
  ]
}
```

#### 2. `.claude/rules/code-style.md`
Extract from existing repos and create unified style guide:
- Language-specific conventions (identified from analysis)
- Common linting/formatting tools
- Preferred patterns
- Anti-patterns to avoid

#### 3. `.claude/prompts/branding.md`
Create org voice/personality:
```markdown
# [ORG_NAME] Voice & Branding

When working on [ORG_NAME] code:

## Tone
- [Based on existing docs/README analysis]

## Terminology
- We say "X" not "Y"
- [Extract from existing repos]

## Code Philosophy
- [Principles extracted from analysis]

## Communication Style
- [For commit messages, PR descriptions, etc.]
```

#### 4. `templates/repo-types/*.json`
Create type-specific templates based on the languages/types found:
- One template per major repo type identified
- Include appropriate rules, context, and tooling
- Add type-specific conventions

## Step 3: Initialize Each Repository

For each repository in the organization (excluding forks and the config repo itself):

1. **Clone or checkout the repo** (or use GitHub API)
2. **Create `.claude/` directory** if it doesn't exist
3. **Generate `.claude/project.json`** that:
   - Extends appropriate template from `claude-org-config`
   - Includes repo-specific name/description
   - References existing CONTRIBUTING.md, README.md if present
   - Adds repo-specific context

Example generated config:
```json
{
  "name": "repo-name",
  "description": "Actual description from GitHub",
  "extends": "github:[ORG_NAME]/claude-org-config/templates/repo-types/[TYPE].json",
  "rules": {
    "org_rules": "inherit",
    "repo_specific": [
      "./CONTRIBUTING.md",
      "./docs/ARCHITECTURE.md"
    ]
  },
  "context": {
    "readme": "./README.md"
  }
}
```

4. **Create a branch** `feat/add-claude-org-config`
5. **Commit the changes**
6. **Create a Pull Request** (optional - can batch these)

## Step 4: Generate Supporting Scripts

Create shell scripts in `scripts/`:

### `scripts/init-repo.sh`
Bash script to bootstrap a new repo with org config

### `scripts/validate-repo.sh`
Check if a repo is compliant with org standards:
- Has `.claude/project.json`
- Extends org config
- Includes required files
- MCP servers match org standards

### `scripts/sync-to-repos.sh`
Update all repos when org config changes

## Step 5: Documentation

Generate comprehensive docs:

### `docs/SETUP.md`
Step-by-step guide for adding org config to a new/existing repo

### `docs/CUSTOMIZATION.md`
How to override org settings for specific repo needs

### `docs/MIGRATION.md`
How to migrate existing `.claude/` configs to use org config

## Execution Plan

Execute this in phases:

**Phase 1: Discovery**
```bash
# Analyze the org
gh repo list [ORG] --limit 1000 --json name,languages,description,primaryLanguage,isPrivate,isFork > org-repos.json

# Analyze each repo for patterns
# Create summary table
```

**Phase 2: Bootstrap Config Repo**
```bash
cd [CONFIG_REPO]
# Create structure
# Generate base configs based on analysis
# Create type templates
# Write rules and prompts
```

**Phase 3: Initialize Repos**
```bash
# For each repo:
# - Clone
# - Create .claude/project.json
# - Create PR
```

**Phase 4: Validation**
```bash
# Run validate-repo.sh on all repos
# Generate compliance report
```

## Important Considerations

1. **Do NOT modify forks** - skip repositories where `isFork: true`
2. **Handle existing `.claude/` configs** - merge rather than replace
3. **Respect private repos** - ensure tokens have appropriate access
4. **Batch PRs** - maybe do 5-10 at a time, not all at once
5. **Type detection** - use smart heuristics for repo type classification

## Output Format

For each phase, provide:
1. **Summary of findings** (tables, statistics)
2. **Generated files** (show content or save to filesystem)
3. **Actions taken** (commands executed)
4. **Next steps** (what I should review/approve)
5. **Validation results** (compliance report)

## Questions to Ask Me

Before proceeding, ask me:
1. Which GitHub org should I analyze?
2. What's the exact name of the config repo?
3. Should I auto-create PRs or just prepare branches?
4. Are there specific repos to exclude beyond forks?
5. Should I include archived repositories?
6. What MCP servers are you currently using that should be org-wide?

---

## Ready to Start?

Once you have the answers above, execute this plan. Start with Phase 1 (Discovery) and show me the analysis before proceeding to Phase 2.
```

---

# File 3: Detailed Quick Start Guide

**Reference:** Use this for step-by-step execution

```markdown
# Quick Start Guide

## What You Have

This package contains:
1. **README.md** - Documentation for your `claude-org-config` repository
2. **bootstrap-org-config.md** - Comprehensive prompt for Claude Code
3. **This guide** - Step-by-step instructions

## Getting Started

### Step 1: Set Up the Config Repository

```bash
# Navigate to your claude-org-config repo
cd /path/to/claude-org-config

# Copy the README from File 1 above
# (manually copy and paste, or extract using the instructions below)

# Edit with your actual org name
# Replace [YOUR_ORG_NAME] placeholders
sed -i '' 's/yourorg/YOUR_ACTUAL_ORG/g' README.md

# Commit
git add README.md
git commit -m "docs: initialize org config repo"
git push
```

### Step 2: Prepare Your Environment

Make sure you have:

```bash
# GitHub CLI installed and authenticated
gh auth status

# Verify org access
gh repo list YOUR_ORG --limit 5

# Ensure you have appropriate permissions
# - Read access to all repos you want to analyze
# - Write access to create .claude/ configs
```

### Step 3: Start Claude Code

```bash
# Option A: From the config repo
cd /path/to/claude-org-config
claude-code

# Option B: From a workspace containing all repos
cd /path/to/org-workspace
claude-code
```

### Step 4: Run the Bootstrap Prompt

Copy File 2 (the bootstrap prompt) and paste it into Claude Code, then answer these questions:

1. **GitHub org name**: `your-org-name`
2. **Config repo name**: `claude-org-config` (or whatever you named it)
3. **Auto-create PRs**: `no` (review first) or `yes` (if confident)
4. **Exclude repos**: List any repos to skip beyond forks
5. **Include archived**: Usually `no`
6. **Org-wide MCP servers**: List any MCP servers everyone should use

Example conversation:
```
You: [paste the bootstrap prompt]

Claude Code: I see you want to bootstrap your org config. Let me ask a few questions:
1. Which GitHub org should I analyze?

You: acme-corp

Claude Code: 2. What's the exact name of the config repo?

You: claude-org-config

[... continue answering ...]
```

### Step 5: Review Phase 1 (Discovery)

Claude Code will analyze all repos and show you:
- Summary table of all repos
- Detected patterns
- Proposed categorization
- Common languages/frameworks

**Review this carefully** before proceeding to Phase 2.

### Step 6: Execute Phase 2 (Bootstrap Config Repo)

Claude Code will create:
- Directory structure
- Base configuration files
- Rules and prompts
- Templates for different repo types
- Scripts for management

**Review the generated files** and make adjustments to:
- Branding/voice in `.claude/prompts/branding.md`
- Code style rules in `.claude/rules/code-style.md`
- Any org-specific conventions

### Step 7: Execute Phase 3 (Initialize Repos)

Claude Code will:
- Create `.claude/project.json` in each repo
- Choose appropriate template based on analysis
- Create branches/PRs

**Review the PRs** before merging.

### Step 8: Validate

Run validation to check compliance:

```bash
# From the config repo
./scripts/validate-repo.sh /path/to/some-repo

# Or validate all repos
for repo in ../*/; do
  ./scripts/validate-repo.sh "$repo"
done
```

## Customization After Bootstrap

### Adding New Rules

```bash
cd claude-org-config
# Edit or create new rule files
vim .claude/rules/new-rule.md

# Update base-project.json to reference it
vim .claude/base-project.json
```

### Creating New Repo Type Templates

```bash
cd claude-org-config/templates/repo-types
cp typescript-service.json rust-service.json
# Edit rust-service.json with Rust-specific config
```

### Updating Existing Repos

After changing org config:

```bash
# Manual sync
./scripts/sync-to-repos.sh

# Or trigger via GitHub Actions if you set that up
gh workflow run sync-claude-config --repo your-org/some-repo
```

## Common Issues & Solutions

### "Permission denied" when accessing repos
```bash
# Check your GitHub token has correct scopes
gh auth refresh -s repo,read:org

# Or set PAT with appropriate permissions
export GITHUB_TOKEN=ghp_...
```

### "Too many repos to process"
Edit the prompt to process in batches:
```bash
# Process first 20 repos
gh repo list YOUR_ORG --limit 20

# Then next 20
gh repo list YOUR_ORG --limit 20 --skip 20
```

### Existing `.claude/` configs conflict
Claude Code should merge, but review carefully:
- Back up existing configs first
- Ensure repo-specific rules are preserved
- Check that overrides work as expected

## Next Steps

After bootstrap:

1. **Add to org onboarding docs** - new repos should use this config
2. **Set up GitHub Actions** - auto-sync config updates
3. **Create MCP server** - for cross-repo context (advanced)
4. **Schedule validation** - weekly checks for compliance
5. **Document exceptions** - some repos might need special config

## Getting Help

- **Config repo issues**: Open issue in `claude-org-config` repo
- **Per-repo issues**: Check that repo's `.claude/project.json`
- **Claude Code issues**: See https://docs.claude.com/claude-code
- **MCP server issues**: Check `mcp/org-servers.json`

## Example: End-to-End Flow

```bash
# 1. Set up
cd ~/code/acme-corp/claude-org-config
# (copy README from File 1)
git add README.md && git commit -m "docs: init" && git push

# 2. Start Claude Code
claude-code

# 3. Paste bootstrap prompt (File 2) and answer questions

# 4. Review Phase 1 output
# (Claude shows repo analysis table)

# 5. Approve Phase 2
You: "Looks good, proceed with Phase 2"

# 6. Review generated configs
# (Claude creates all files)

# 7. Approve Phase 3 (or do manually)
You: "Create PRs for first 5 repos as a test"

# 8. Review PRs on GitHub, merge when satisfied

# 9. Roll out to remaining repos

# 10. Set up automation
cd scripts
./setup-github-actions.sh  # If Claude generates this
```

## Pro Tips

- **Start small**: Test with 2-3 repos before rolling out org-wide
- **Use repo types**: Categorize repos to avoid one-size-fits-all config
- **Version your config**: Tag releases of claude-org-config
- **Document deviations**: If a repo needs special config, document why
- **Automate validation**: Run in CI to catch drift
- **Iterate**: Start simple, add rules/structure as patterns emerge

Ready? Start with Step 1! 🚀
```

---

## 📝 How to Extract Files

### Method 1: Manual Copy/Paste

1. **For README.md**: Copy everything between the triple backticks in "File 1"
2. **For Bootstrap Prompt**: Copy everything between the triple backticks in "File 2"
3. **For Quick Start**: Copy everything between the triple backticks in "File 3"

### Method 2: Script Extraction

Save this package file as `claude-org-config-package.md`, then run:

```bash
# Extract README
sed -n '/^# File 1: README.md/,/^---$/p' claude-org-config-package.md | \
  sed '1d;$d' | sed '1,/^```markdown$/d' | sed '/^```$/,$d' > README.md

# Extract Bootstrap Prompt
sed -n '/^# File 2: Bootstrap Prompt/,/^---$/p' claude-org-config-package.md | \
  sed '1d;$d' | sed '1,/^```markdown$/d' | sed '/^```$/,$d' > bootstrap-prompt.md

# Extract Quick Start
sed -n '/^# File 3: Detailed Quick Start/,/^---$/p' claude-org-config-package.md | \
  sed '1d;$d' | sed '1,/^```markdown$/d' | sed '/^```$/,$d' > QUICKSTART.md
```

### Method 3: Use this simple extraction script

```bash
#!/bin/bash
# save as extract.sh and run: bash extract.sh claude-org-config-package.md

FILE=$1

echo "Extracting File 1: README.md..."
awk '/^# File 1: README.md/,/^---$/' "$FILE" | \
  sed -n '/^```markdown$/,/^```$/p' | sed '1d;$d' > README.md

echo "Extracting File 2: bootstrap-prompt.md..."
awk '/^# File 2: Bootstrap Prompt/,/^---$/' "$FILE" | \
  sed -n '/^```markdown$/,/^```$/p' | sed '1d;$d' > bootstrap-prompt.md

echo "Extracting File 3: QUICKSTART.md..."
awk '/^# File 3: Detailed Quick Start/,/^---$/' "$FILE" | \
  sed -n '/^```markdown$/,/^```$/p' | sed '1d;$d' > QUICKSTART.md

echo "Done! Files extracted:"
ls -lh README.md bootstrap-prompt.md QUICKSTART.md
```

---

## 🎯 What to Do Now

1. **This file is already saved** to `~/Downloads/claude-org-config-complete-package.md`
2. **Navigate to your config repo**: `cd /path/to/claude-org-config`
3. **Extract the README**:
   ```bash
   # Copy the README section from File 1, or use extraction script
   # Edit to replace 'yourorg' with your actual org name
   ```
4. **Start Claude Code**: `claude-code`
5. **Paste the Bootstrap Prompt** (from File 2) into Claude Code
6. **Follow the Quick Start Guide** (File 3) for detailed steps

---

## 📚 Additional Resources

- **Claude Code docs**: https://docs.claude.com/claude-code
- **MCP documentation**: https://modelcontextprotocol.io
- **GitHub CLI**: https://cli.github.com

---

## 📄 License

This bootstrap package is provided as-is for organizational use. Modify as needed for your org's requirements.

---

**Questions or issues?** Open a discussion in your `claude-org-config` repository after bootstrap.
