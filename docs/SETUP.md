# Setting Up Organization-Wide Claude Configuration

**Complete guide for integrating raibid-labs org config into new and existing repositories**

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Setup](#quick-setup)
4. [Template Selection Guide](#template-selection-guide)
5. [Step-by-Step Setup Instructions](#step-by-step-setup-instructions)
6. [Configuration Examples](#configuration-examples)
7. [Verification & Testing](#verification--testing)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Setup Options](#advanced-setup-options)

---

## Overview

The raibid-labs organization configuration provides centralized Claude settings, rules, and context that all repositories can inherit. This ensures consistency across projects while allowing repo-specific customization.

### Benefits of Using Org Config

- **Consistency**: Uniform coding standards and conventions across all repos
- **Efficiency**: No need to duplicate common rules and settings
- **Maintainability**: Update org-wide rules in one place
- **Flexibility**: Override or extend for specific repo needs
- **Context Sharing**: Claude understands the full organization structure

### How It Works

```
┌─────────────────────────────┐
│  raibid-labs/claude-org-    │  ← Central config repository
│  config                      │
└──────────┬──────────────────┘
           │ extends
    ┌──────▼──────┬─────────────┬──────────────┐
    │  repo-1     │   repo-2    │   repo-3     │ ← Individual repos
    │ .claude/    │  .claude/   │  .claude/    │   inherit config
    └─────────────┴─────────────┴──────────────┘
```

---

## Prerequisites

Before setting up org config in a repository:

1. **Access to raibid-labs organization**
   ```bash
   # Verify GitHub access
   gh auth status
   gh repo list raibid-labs --limit 3
   ```

2. **Clone the target repository**
   ```bash
   git clone https://github.com/raibid-labs/your-repo.git
   cd your-repo
   ```

3. **Ensure you have write permissions**
   ```bash
   # Check your permissions
   gh repo view --json viewerPermission
   ```

4. **Have Claude Code installed** (optional but recommended for testing)
   ```bash
   # Install if needed
   npm install -g @anthropic/claude-code
   ```

---

## Quick Setup

### Automatic Setup (Recommended)

For new repositories, use the init script:

```bash
# From within your repository
curl -fsSL https://raw.githubusercontent.com/raibid-labs/claude-org-config/main/scripts/init-repo.sh | bash
```

This will:
1. Create `.claude/` directory
2. Generate appropriate `project.json`
3. Select the right template based on repo analysis
4. Create a branch with changes
5. Open a PR for review

### Manual Quick Setup

```bash
# Create .claude directory
mkdir -p .claude

# Download the appropriate template (e.g., for a Rust service)
curl -o .claude/project.json \
  https://raw.githubusercontent.com/raibid-labs/claude-org-config/main/templates/repo-types/rust-service.json

# Edit to add your repo-specific details
vim .claude/project.json

# Commit changes
git add .claude/
git commit -m "feat: add raibid-labs claude configuration"
git push origin main
```

---

## Template Selection Guide

Choose the right template based on your repository type:

### Repository Type Decision Tree

```
Is your repo primarily...
│
├── A microservice or API?
│   ├── Written in Rust? → use `rust-service.json`
│   ├── Written in TypeScript/Node? → use `typescript-service.json`
│   ├── Written in Python? → use `python-service.json`
│   └── Written in Go? → use `go-service.json`
│
├── A library or SDK?
│   ├── Rust library? → use `rust-library.json`
│   ├── TypeScript/JavaScript? → use `typescript-library.json`
│   └── Python package? → use `python-library.json`
│
├── Infrastructure or DevOps?
│   ├── Terraform? → use `infrastructure-terraform.json`
│   ├── Kubernetes? → use `infrastructure-k8s.json`
│   └── CI/CD pipelines? → use `infrastructure-cicd.json`
│
├── Machine Learning or Data?
│   ├── ML model? → use `python-ml.json`
│   └── Data pipeline? → use `python-data-pipeline.json`
│
├── Documentation?
│   └── → use `documentation.json`
│
└── Other/Unsure?
    └── → use `base-template.json` and customize
```

### Template Comparison

| Template | Primary Language | Key Features | Best For |
|----------|-----------------|--------------|-----------|
| `rust-service` | Rust | Async/await patterns, error handling, performance | API servers, microservices |
| `rust-library` | Rust | Documentation focus, examples, benchmarks | Crates, shared libraries |
| `python-ml` | Python | Jupyter support, data processing, model training | ML projects, research |
| `python-service` | Python | FastAPI/Flask patterns, async support | Web services, APIs |
| `typescript-service` | TypeScript | Express/NestJS patterns, testing | Node.js services |
| `go-service` | Go | Concurrency patterns, error handling | High-performance services |
| `infrastructure-*` | YAML/HCL | IaC best practices, security | DevOps, cloud resources |

---

## Step-by-Step Setup Instructions

### Step 1: Analyze Your Repository

First, understand your repository's characteristics:

```bash
# Check primary language
gh repo view --json primaryLanguage

# List all languages
gh repo view --json languages

# Check for existing config
ls -la .claude/

# Review repo structure
tree -L 2 -I 'node_modules|target|dist|build'
```

### Step 2: Create `.claude` Directory

```bash
# Create the configuration directory
mkdir -p .claude

# If you have existing configs, back them up
if [ -d .claude ]; then
  cp -r .claude .claude.backup.$(date +%Y%m%d)
fi
```

### Step 3: Select and Download Template

Based on your analysis, choose the appropriate template:

```bash
# Set variables
REPO_TYPE="rust-service"  # Change based on your repo type
ORG_NAME="raibid-labs"
CONFIG_REPO="claude-org-config"

# Download the template
curl -o .claude/project.json \
  "https://raw.githubusercontent.com/${ORG_NAME}/${CONFIG_REPO}/main/templates/repo-types/${REPO_TYPE}.json"
```

### Step 4: Customize the Configuration

Edit `.claude/project.json` with your repo-specific information:

```json
{
  "name": "your-repo-name",
  "description": "Specific description of what this repo does",
  "extends": "github:raibid-labs/claude-org-config/templates/repo-types/rust-service.json",
  "rules": {
    "org_rules": "inherit",
    "repo_specific": [
      "./CONTRIBUTING.md",
      "./docs/ARCHITECTURE.md",
      "./docs/API.md"
    ]
  },
  "context": {
    "readme": "./README.md",
    "examples": "./examples/",
    "tests": "./tests/"
  },
  "knowledge_sources": [
    {
      "type": "folder",
      "path": "docs/",
      "description": "Repository documentation"
    },
    {
      "type": "file",
      "path": "Cargo.toml",
      "description": "Dependencies and project metadata"
    }
  ],
  "repo_specific": {
    "environment_variables": [
      "DATABASE_URL",
      "API_KEY",
      "LOG_LEVEL"
    ],
    "primary_frameworks": [
      "tokio",
      "axum",
      "sqlx"
    ],
    "testing_approach": "unit + integration + property-based"
  }
}
```

### Step 5: Add Repository-Specific Documentation

Create additional context files if needed:

```bash
# Create repo-specific rules (if needed)
cat > .claude/repo-rules.md << 'EOF'
# Repository-Specific Rules

## Database Conventions
- Always use migrations for schema changes
- Never commit .env files
- Use prepared statements for all queries

## API Design
- Follow RESTful conventions
- Version all APIs (v1, v2, etc.)
- Include OpenAPI documentation
EOF

# Update project.json to reference it
jq '.rules.repo_specific += ["./.claude/repo-rules.md"]' .claude/project.json > tmp.json
mv tmp.json .claude/project.json
```

### Step 6: Validate the Configuration

Test that your configuration is valid:

```bash
# Download and run validation script
curl -fsSL https://raw.githubusercontent.com/raibid-labs/claude-org-config/main/scripts/validate-repo.sh | bash

# Or manually check
echo "Checking configuration..."

# Verify JSON is valid
jq . .claude/project.json > /dev/null 2>&1 && echo "✓ Valid JSON" || echo "✗ Invalid JSON"

# Check that extends path exists
EXTENDS=$(jq -r '.extends' .claude/project.json)
echo "Extends: $EXTENDS"

# Verify referenced files exist
jq -r '.rules.repo_specific[]?' .claude/project.json | while read file; do
  if [ -f "$file" ]; then
    echo "✓ Found: $file"
  else
    echo "✗ Missing: $file"
  fi
done
```

### Step 7: Test with Claude Code

```bash
# Start Claude Code in your repo
claude-code

# Test that org config is loaded
# Ask Claude: "What are the organization's coding standards?"
# Claude should reference the org-wide rules
```

### Step 8: Commit and Push

```bash
# Create a feature branch
git checkout -b feat/add-claude-org-config

# Stage changes
git add .claude/

# Commit with descriptive message
git commit -m "feat: integrate raibid-labs claude organization configuration

- Add .claude/project.json extending org-wide config
- Select rust-service template for this API service
- Include repo-specific documentation references
- Configure knowledge sources for better context"

# Push the branch
git push origin feat/add-claude-org-config

# Create a pull request
gh pr create \
  --title "Add Claude organization configuration" \
  --body "Integrates raibid-labs org-wide Claude configuration for consistency across repos" \
  --base main
```

---

## Configuration Examples

### Example 1: Rust Microservice

```json
{
  "name": "payment-service",
  "description": "Payment processing microservice using Stripe API",
  "extends": "github:raibid-labs/claude-org-config/templates/repo-types/rust-service.json",
  "rules": {
    "org_rules": "inherit",
    "repo_specific": [
      "./docs/PAYMENT_FLOW.md",
      "./docs/PCI_COMPLIANCE.md"
    ]
  },
  "context": {
    "api_docs": "./openapi.yaml",
    "migrations": "./migrations/",
    "integration_tests": "./tests/integration/"
  },
  "mcp_servers": {
    "stripe-context": {
      "command": "npx",
      "args": ["-y", "@stripe/mcp-server"],
      "env": {
        "STRIPE_API_KEY": "${STRIPE_TEST_KEY}"
      }
    }
  },
  "security_notes": "This service handles PCI data. Follow security guidelines strictly."
}
```

### Example 2: Python ML Model

```json
{
  "name": "fraud-detection-model",
  "description": "Machine learning model for fraud detection using XGBoost",
  "extends": "github:raibid-labs/claude-org-config/templates/repo-types/python-ml.json",
  "rules": {
    "org_rules": "inherit",
    "repo_specific": [
      "./notebooks/README.md",
      "./docs/MODEL_CARD.md",
      "./docs/FEATURE_ENGINEERING.md"
    ]
  },
  "context": {
    "notebooks": "./notebooks/",
    "data_pipeline": "./src/pipeline/",
    "model_configs": "./configs/"
  },
  "knowledge_sources": [
    {
      "type": "folder",
      "path": "notebooks/experiments/",
      "description": "Experiment notebooks with results"
    }
  ],
  "ml_specific": {
    "framework": "xgboost",
    "metrics": ["precision", "recall", "f1", "auc"],
    "data_sources": ["transaction_db", "user_behavior_logs"]
  }
}
```

### Example 3: Infrastructure Repository

```json
{
  "name": "kubernetes-platform",
  "description": "Kubernetes manifests and Helm charts for raibid-labs platform",
  "extends": "github:raibid-labs/claude-org-config/templates/repo-types/infrastructure-k8s.json",
  "rules": {
    "org_rules": "inherit",
    "repo_specific": [
      "./docs/DEPLOYMENT_GUIDE.md",
      "./docs/DISASTER_RECOVERY.md",
      "./SECURITY.md"
    ]
  },
  "context": {
    "helm_charts": "./charts/",
    "environments": "./environments/",
    "scripts": "./scripts/"
  },
  "infrastructure": {
    "clusters": ["production", "staging", "development"],
    "cloud_provider": "AWS",
    "monitoring": "Prometheus + Grafana",
    "cicd": "GitHub Actions + ArgoCD"
  }
}
```

### Example 4: Documentation Repository

```json
{
  "name": "engineering-handbook",
  "description": "Engineering team documentation and best practices",
  "extends": "github:raibid-labs/claude-org-config/templates/repo-types/documentation.json",
  "rules": {
    "org_rules": "inherit",
    "repo_specific": [
      "./STYLE_GUIDE.md",
      "./CONTRIBUTION_GUIDE.md"
    ]
  },
  "context": {
    "onboarding": "./onboarding/",
    "processes": "./processes/",
    "architecture": "./architecture/",
    "runbooks": "./runbooks/"
  },
  "documentation": {
    "format": "markdown",
    "site_generator": "mkdocs",
    "deploy_to": "GitHub Pages"
  }
}
```

### Example 5: Multi-Language Monorepo

```json
{
  "name": "platform-monorepo",
  "description": "Monorepo containing multiple services and shared libraries",
  "extends": "github:raibid-labs/claude-org-config/templates/repo-types/base-template.json",
  "rules": {
    "org_rules": "inherit",
    "repo_specific": [
      "./docs/MONOREPO_STRUCTURE.md",
      "./docs/BUILD_GUIDE.md",
      "./packages/README.md"
    ]
  },
  "context": {
    "services": "./services/",
    "packages": "./packages/",
    "tools": "./tools/",
    "configs": "./configs/"
  },
  "workspace_config": {
    "package_manager": "pnpm",
    "build_tool": "nx",
    "languages": ["typescript", "rust", "python"],
    "services": [
      "api-gateway",
      "auth-service",
      "notification-service",
      "analytics-engine"
    ]
  },
  "knowledge_sources": [
    {
      "type": "folder",
      "path": "services/",
      "description": "All microservices"
    },
    {
      "type": "folder",
      "path": "packages/",
      "description": "Shared libraries and utilities"
    }
  ]
}
```

---

## Verification & Testing

### Verification Checklist

After setup, verify everything works correctly:

```bash
#!/bin/bash
# Save as verify-setup.sh

echo "🔍 Verifying Claude Configuration Setup"
echo "======================================="

# 1. Check .claude directory exists
if [ -d ".claude" ]; then
  echo "✅ .claude directory exists"
else
  echo "❌ .claude directory missing"
  exit 1
fi

# 2. Check project.json exists and is valid
if [ -f ".claude/project.json" ]; then
  echo "✅ project.json exists"
  if jq . .claude/project.json > /dev/null 2>&1; then
    echo "✅ project.json is valid JSON"
  else
    echo "❌ project.json is invalid JSON"
    exit 1
  fi
else
  echo "❌ project.json missing"
  exit 1
fi

# 3. Check extends field
EXTENDS=$(jq -r '.extends' .claude/project.json)
if [[ $EXTENDS == *"raibid-labs/claude-org-config"* ]]; then
  echo "✅ Extends raibid-labs org config"
else
  echo "❌ Does not extend org config"
  exit 1
fi

# 4. Check referenced files exist
echo ""
echo "Checking referenced files..."
jq -r '.rules.repo_specific[]?' .claude/project.json 2>/dev/null | while read file; do
  if [ -f "$file" ]; then
    echo "  ✅ $file"
  else
    echo "  ⚠️  $file (missing - create if needed)"
  fi
done

# 5. Check for common repo files
echo ""
echo "Checking standard files..."
for file in README.md LICENSE CONTRIBUTING.md; do
  if [ -f "$file" ]; then
    echo "  ✅ $file"
  else
    echo "  ⚠️  $file (consider adding)"
  fi
done

echo ""
echo "✨ Setup verification complete!"
```

### Testing with Claude Code

Test your configuration:

```bash
# Start Claude Code
claude-code

# Test commands to verify org config is working:
# 1. "What are the organization's coding standards?"
# 2. "Show me the repository structure"
# 3. "What MCP servers are available?"
# 4. "What are the security requirements for this repo?"
```

### Integration Testing

Create a test file to verify Claude understands the context:

```bash
# Create a test prompt
cat > .claude-test-prompt.md << 'EOF'
Please verify that you can access:
1. Organization-wide rules
2. Repository-specific configuration
3. MCP server configurations
4. Knowledge sources

For each, provide a brief example of what you can see.
EOF

# Run with Claude Code
claude-code --prompt .claude-test-prompt.md
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: "Cannot find extended configuration"

**Symptoms:**
- Claude doesn't recognize org rules
- Error messages about missing extends path

**Solution:**
```bash
# Verify the extends path is correct
EXTENDS=$(jq -r '.extends' .claude/project.json)
echo "Current extends: $EXTENDS"

# Should be: github:raibid-labs/claude-org-config/...
# Fix if needed:
jq '.extends = "github:raibid-labs/claude-org-config/templates/repo-types/rust-service.json"' \
  .claude/project.json > tmp.json && mv tmp.json .claude/project.json
```

#### Issue: "JSON parsing error in project.json"

**Symptoms:**
- Claude fails to load configuration
- Validation script reports invalid JSON

**Solution:**
```bash
# Validate and format JSON
jq . .claude/project.json > .claude/project.json.formatted
mv .claude/project.json.formatted .claude/project.json

# Common fixes:
# - Remove trailing commas
# - Ensure all strings are quoted
# - Check for unmatched brackets
```

#### Issue: "MCP servers not loading"

**Symptoms:**
- MCP commands not available in Claude
- Server connection errors

**Solution:**
```bash
# Check MCP server configuration
jq '.mcp_servers' .claude/project.json

# Verify server commands are available
npx -y @raibid-labs/context-server --version

# Test server directly
npx -y @raibid-labs/context-server test
```

#### Issue: "Conflicting rules between org and repo"

**Symptoms:**
- Contradictory guidance from Claude
- Unclear which rules apply

**Solution:**
```json
{
  "rules": {
    "org_rules": "inherit",
    "repo_specific": ["./docs/OVERRIDES.md"],
    "overrides": {
      "naming_convention": "repo-specific-convention",
      "testing_framework": "vitest"  // Override org default
    }
  },
  "priority": "repo_specific"  // repo rules take precedence
}
```

#### Issue: "Missing referenced files"

**Symptoms:**
- Warning about missing context files
- Incomplete understanding of repo

**Solution:**
```bash
# List all referenced files
jq -r '.rules.repo_specific[]?, .context[]?' .claude/project.json | while read file; do
  if [ ! -f "$file" ]; then
    echo "Missing: $file"
    # Create placeholder or remove reference
    touch "$file" || \
    jq "del(.rules.repo_specific[] | select(. == \"$file\"))" .claude/project.json > tmp.json
  fi
done
```

### Debug Mode

Enable verbose output for troubleshooting:

```bash
# Create debug configuration
cat > .claude/debug.json << 'EOF'
{
  "extends": "./.claude/project.json",
  "debug": {
    "verbose": true,
    "log_level": "debug",
    "show_inheritance_chain": true,
    "validate_references": true
  }
}
EOF

# Run Claude with debug config
CLAUDE_CONFIG=.claude/debug.json claude-code
```

### Getting Help

If issues persist:

1. **Check org config repo issues**
   ```bash
   gh issue list --repo raibid-labs/claude-org-config
   ```

2. **Open a new issue**
   ```bash
   gh issue create \
     --repo raibid-labs/claude-org-config \
     --title "Setup issue: [brief description]" \
     --body "Repo: $(gh repo view --json name -q .name)\nIssue: [details]\nSteps tried: [what you tried]"
   ```

3. **Contact the platform team**
   - Slack: #claude-config-help
   - Email: platform@raibid-labs.io

---

## Advanced Setup Options

### Using GitHub Actions for Setup

Automate setup with GitHub Actions:

```yaml
# .github/workflows/setup-claude-config.yml
name: Setup Claude Configuration

on:
  workflow_dispatch:
    inputs:
      template:
        description: 'Template type'
        required: true
        type: choice
        options:
          - rust-service
          - python-ml
          - typescript-service
          - infrastructure-k8s
          - auto-detect

jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Auto-detect template if needed
        if: inputs.template == 'auto-detect'
        id: detect
        run: |
          # Detection logic based on files present
          if [ -f "Cargo.toml" ]; then
            echo "template=rust-service" >> $GITHUB_OUTPUT
          elif [ -f "pyproject.toml" ] || [ -f "setup.py" ]; then
            echo "template=python-service" >> $GITHUB_OUTPUT
          elif [ -f "package.json" ]; then
            echo "template=typescript-service" >> $GITHUB_OUTPUT
          else
            echo "template=base-template" >> $GITHUB_OUTPUT
          fi

      - name: Setup Claude Config
        env:
          TEMPLATE: ${{ inputs.template == 'auto-detect' && steps.detect.outputs.template || inputs.template }}
        run: |
          curl -fsSL https://raw.githubusercontent.com/raibid-labs/claude-org-config/main/scripts/init-repo.sh | \
            bash -s -- --template "$TEMPLATE"

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          commit-message: 'feat: add claude organization configuration'
          title: 'Add Claude organization configuration'
          body: |
            Automated setup of raibid-labs Claude configuration.

            Template: ${{ env.TEMPLATE }}

            Please review and merge if appropriate.
          branch: feat/claude-org-config
```

### Custom Setup Scripts

Create repo-specific setup scripts:

```bash
#!/bin/bash
# custom-setup.sh

# Detect repo characteristics
detect_repo_type() {
  if [ -f "Cargo.toml" ]; then
    if grep -q '\[lib\]' Cargo.toml; then
      echo "rust-library"
    else
      echo "rust-service"
    fi
  elif [ -f "setup.py" ] && [ -d "notebooks" ]; then
    echo "python-ml"
  elif [ -f "package.json" ]; then
    if grep -q '"private": true' package.json; then
      echo "typescript-service"
    else
      echo "typescript-library"
    fi
  else
    echo "base-template"
  fi
}

# Setup with detected type
REPO_TYPE=$(detect_repo_type)
echo "Detected repository type: $REPO_TYPE"

# Download and customize template
curl -o .claude/project.json \
  "https://raw.githubusercontent.com/raibid-labs/claude-org-config/main/templates/repo-types/${REPO_TYPE}.json"

# Add repo-specific customizations
REPO_NAME=$(basename $(pwd))
REPO_DESC=$(gh repo view --json description -q .description)

jq --arg name "$REPO_NAME" --arg desc "$REPO_DESC" \
  '.name = $name | .description = $desc' \
  .claude/project.json > tmp.json && mv tmp.json .claude/project.json

# Add local documentation references
for doc in README.md CONTRIBUTING.md docs/ARCHITECTURE.md; do
  if [ -f "$doc" ]; then
    jq --arg doc "./$doc" '.rules.repo_specific += [$doc]' \
      .claude/project.json > tmp.json && mv tmp.json .claude/project.json
  fi
done

echo "✅ Setup complete! Please review .claude/project.json"
```

### Bulk Setup for Multiple Repos

Setup org config across multiple repositories:

```bash
#!/bin/bash
# bulk-setup.sh

# List of repos to configure
REPOS=(
  "payment-service"
  "user-service"
  "notification-service"
  "analytics-engine"
)

ORG="raibid-labs"
BRANCH="feat/claude-org-config"

for repo in "${REPOS[@]}"; do
  echo "Setting up $repo..."

  # Clone repo
  gh repo clone "$ORG/$repo" "/tmp/$repo"
  cd "/tmp/$repo"

  # Create branch
  git checkout -b "$BRANCH"

  # Run setup
  curl -fsSL https://raw.githubusercontent.com/raibid-labs/claude-org-config/main/scripts/init-repo.sh | bash

  # Commit and push
  git add .claude/
  git commit -m "feat: add claude organization configuration"
  git push origin "$BRANCH"

  # Create PR
  gh pr create \
    --title "Add Claude organization configuration" \
    --body "Automated setup of org-wide Claude configuration" \
    --base main

  echo "✅ Completed $repo"
  cd ..
done
```

### Validation in CI/CD

Add validation to your CI pipeline:

```yaml
# .github/workflows/validate-claude-config.yml
name: Validate Claude Configuration

on:
  pull_request:
    paths:
      - '.claude/**'
  push:
    branches: [main]
    paths:
      - '.claude/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Validate JSON structure
        run: |
          jq . .claude/project.json > /dev/null

      - name: Check org config extension
        run: |
          EXTENDS=$(jq -r '.extends' .claude/project.json)
          if [[ $EXTENDS != *"raibid-labs/claude-org-config"* ]]; then
            echo "Error: Must extend raibid-labs org config"
            exit 1
          fi

      - name: Verify referenced files
        run: |
          jq -r '.rules.repo_specific[]?' .claude/project.json | while read file; do
            if [ ! -f "$file" ]; then
              echo "Warning: Referenced file missing: $file"
            fi
          done

      - name: Run org validation script
        run: |
          curl -fsSL https://raw.githubusercontent.com/raibid-labs/claude-org-config/main/scripts/validate-repo.sh | bash
```

---

## Summary

Setting up raibid-labs org configuration ensures:
- Consistent Claude behavior across all repositories
- Shared knowledge and context
- Easier onboarding for new projects
- Centralized maintenance of standards

Remember to:
1. Choose the right template for your repo type
2. Customize for repo-specific needs
3. Validate the configuration
4. Test with Claude Code
5. Keep configuration up to date

For additional help, see:
- [CUSTOMIZATION.md](./CUSTOMIZATION.md) - How to override and extend
- [MIGRATION.md](./MIGRATION.md) - Migrating existing configurations
- [Organization Config Repository](https://github.com/raibid-labs/claude-org-config)