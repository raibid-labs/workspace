# Migrating to Organization Configuration

**Comprehensive guide for migrating existing repositories to raibid-labs org configuration**

## Table of Contents

1. [Overview](#overview)
2. [Pre-Migration Assessment](#pre-migration-assessment)
3. [Migration Strategies](#migration-strategies)
4. [Step-by-Step Migration Process](#step-by-step-migration-process)
5. [Handling Existing Configurations](#handling-existing-configurations)
6. [Conflict Resolution](#conflict-resolution)
7. [Testing & Validation](#testing--validation)
8. [Rollback Procedures](#rollback-procedures)
9. [Migration Examples](#migration-examples)
10. [Post-Migration Checklist](#post-migration-checklist)
11. [Troubleshooting](#troubleshooting)

---

## Overview

Migrating existing repositories to use raibid-labs organization configuration requires careful planning to preserve existing functionality while gaining the benefits of centralized configuration.

### Migration Benefits

- **Consistency**: Align with organization-wide standards
- **Maintenance**: Reduce configuration duplication
- **Updates**: Automatically receive org-wide improvements
- **Context**: Share knowledge across repositories
- **Efficiency**: Less per-repo configuration needed

### Migration Challenges

- Preserving repository-specific customizations
- Resolving conflicts between existing and org configs
- Maintaining backward compatibility
- Ensuring team workflows aren't disrupted
- Handling unique repository requirements

### Migration Timeline

```
Week 1: Assessment & Planning
├── Inventory existing configurations
├── Identify conflicts and customizations
└── Create migration plan

Week 2: Implementation
├── Backup existing configuration
├── Implement migration
└── Test thoroughly

Week 3: Validation & Rollout
├── Team testing
├── Address issues
└── Final deployment
```

---

## Pre-Migration Assessment

### Step 1: Audit Existing Configuration

```bash
#!/bin/bash
# audit-existing-config.sh

echo "=== Repository Configuration Audit ==="
REPO_NAME=$(basename $(pwd))
REPORT_FILE="migration-assessment-$(date +%Y%m%d).md"

cat > $REPORT_FILE << EOF
# Migration Assessment for $REPO_NAME

## Current Configuration

### Claude Configuration
EOF

# Check for existing .claude directory
if [ -d ".claude" ]; then
  echo "✅ .claude directory exists" >> $REPORT_FILE
  echo "### Files in .claude/:" >> $REPORT_FILE
  find .claude -type f -name "*.json" -o -name "*.md" | while read file; do
    echo "- $file ($(wc -l < $file) lines)" >> $REPORT_FILE
  done
else
  echo "❌ No .claude directory found" >> $REPORT_FILE
fi

# Check for project.json
if [ -f ".claude/project.json" ]; then
  echo "\n### project.json structure:" >> $REPORT_FILE
  echo '```json' >> $REPORT_FILE
  jq 'keys' .claude/project.json >> $REPORT_FILE
  echo '```' >> $REPORT_FILE
fi

# Check for MCP servers
if [ -f ".claude/project.json" ]; then
  MCP_COUNT=$(jq '.mcp_servers | length' .claude/project.json 2>/dev/null || echo 0)
  echo "\n### MCP Servers: $MCP_COUNT configured" >> $REPORT_FILE
  if [ $MCP_COUNT -gt 0 ]; then
    jq -r '.mcp_servers | keys[]' .claude/project.json >> $REPORT_FILE
  fi
fi

# Check for custom rules
echo "\n### Custom Rules:" >> $REPORT_FILE
find . -name "*.md" -path "*/rules/*" -o -name "CONTRIBUTING.md" -o -name "CONVENTIONS.md" | while read rule; do
  echo "- $rule" >> $REPORT_FILE
done

echo "\n✅ Assessment saved to: $REPORT_FILE"
```

### Step 2: Identify Customizations

```bash
#!/bin/bash
# identify-customizations.sh

echo "=== Identifying Repository Customizations ==="

# Extract custom settings
if [ -f ".claude/project.json" ]; then
  echo "\n## Custom Settings Found:"

  # Check for custom MCP servers
  echo "\n### MCP Servers:"
  jq -r '.mcp_servers | to_entries[] | "- \(.key): \(.value.command)"' .claude/project.json 2>/dev/null

  # Check for custom rules
  echo "\n### Custom Rules:"
  jq -r '.rules[]?' .claude/project.json 2>/dev/null | while read rule; do
    echo "- $rule"
  done

  # Check for knowledge sources
  echo "\n### Knowledge Sources:"
  jq -r '.knowledge_sources[]? | "- \(.type): \(.path)"' .claude/project.json 2>/dev/null

  # Check for environment variables
  echo "\n### Environment Variables:"
  jq -r '.env[]?' .claude/project.json 2>/dev/null
fi

# Identify repo-specific patterns
echo "\n## Repository Patterns:"
echo "- Primary language: $(gh repo view --json primaryLanguage -q .primaryLanguage)"
echo "- Total languages: $(gh repo view --json languages -q '.languages | keys | length')"
echo "- Has CI/CD: $([ -d .github/workflows ] && echo 'Yes' || echo 'No')"
echo "- Has tests: $([ -d tests ] || [ -d test ] && echo 'Yes' || echo 'No')"
echo "- Has docs: $([ -d docs ] && echo 'Yes' || echo 'No')"
```

### Step 3: Compatibility Check

```bash
#!/bin/bash
# check-compatibility.sh

echo "=== Checking Compatibility with Org Config ==="

# Download org config schema
TEMP_SCHEMA=$(mktemp)
curl -s https://raw.githubusercontent.com/raibid-labs/claude-org-config/main/schema.json > $TEMP_SCHEMA

# Validate current config against org schema
if [ -f ".claude/project.json" ]; then
  echo "Validating current configuration..."

  # Check for incompatible fields
  CURRENT_FIELDS=$(jq 'keys[]' .claude/project.json | tr '\n' ' ')
  echo "Current fields: $CURRENT_FIELDS"

  # Check for conflicts
  echo "\n## Potential Conflicts:"

  # Check if already extending something
  CURRENT_EXTENDS=$(jq -r '.extends // "none"' .claude/project.json)
  if [ "$CURRENT_EXTENDS" != "none" ]; then
    echo "⚠️  Already extends: $CURRENT_EXTENDS"
    echo "   Will need to resolve inheritance chain"
  fi

  # Check for hardcoded values that should use org defaults
  if jq -e '.code_style' .claude/project.json > /dev/null; then
    echo "⚠️  Has local code_style - should use org defaults"
  fi
fi

rm $TEMP_SCHEMA
```

---

## Migration Strategies

### Strategy 1: Clean Migration (Recommended for Simple Repos)

Best for repositories with minimal customization:

```json
{
  "migration_strategy": "clean",
  "steps": [
    "Backup existing configuration",
    "Remove .claude directory",
    "Apply org template",
    "Re-add essential customizations"
  ],
  "suitable_for": [
    "New repositories",
    "Standard services",
    "Minimal customization"
  ]
}
```

### Strategy 2: Incremental Migration (Recommended for Complex Repos)

Best for repositories with significant customization:

```json
{
  "migration_strategy": "incremental",
  "phases": [
    {
      "phase": 1,
      "action": "Add extends without removing existing",
      "duration": "1 week"
    },
    {
      "phase": 2,
      "action": "Move common rules to org config",
      "duration": "1 week"
    },
    {
      "phase": 3,
      "action": "Consolidate and cleanup",
      "duration": "1 week"
    }
  ]
}
```

### Strategy 3: Hybrid Migration (For Special Cases)

Best for repositories with unique requirements:

```json
{
  "migration_strategy": "hybrid",
  "approach": "Extend org config while maintaining repo-specific layer",
  "maintains": [
    "Custom MCP servers",
    "Specialized rules",
    "Unique workflows"
  ],
  "adopts": [
    "Org coding standards",
    "Common tools",
    "Shared context"
  ]
}
```

---

## Step-by-Step Migration Process

### Phase 1: Preparation

```bash
#!/bin/bash
# prepare-migration.sh

echo "=== Phase 1: Preparing for Migration ==="

# 1. Create migration branch
git checkout -b migration/org-config-adoption
echo "✅ Created migration branch"

# 2. Backup existing configuration
if [ -d ".claude" ]; then
  cp -r .claude .claude.backup.$(date +%Y%m%d-%H%M%S)
  tar -czf claude-config-backup-$(date +%Y%m%d).tar.gz .claude
  echo "✅ Backed up existing configuration"
fi

# 3. Document current state
cat > MIGRATION_NOTES.md << 'EOF'
# Migration to Org Configuration

## Pre-Migration State
- Date: $(date)
- Current config: $([ -d .claude ] && echo "Exists" || echo "None")
- Migration strategy: [SELECTED_STRATEGY]

## Customizations to Preserve
- [ ] Custom MCP servers
- [ ] Repository-specific rules
- [ ] Special environment variables
- [ ] Unique knowledge sources

## Expected Changes
- Will adopt org coding standards
- Will use shared MCP servers
- Will inherit common rules

## Testing Plan
- [ ] Verify Claude loads configuration
- [ ] Test existing workflows
- [ ] Check team-specific features
- [ ] Validate CI/CD integration
EOF

echo "✅ Created migration notes"

# 4. Download migration toolkit
mkdir -p .migration-tools
curl -o .migration-tools/migrate.sh \
  https://raw.githubusercontent.com/raibid-labs/claude-org-config/main/scripts/migrate.sh
chmod +x .migration-tools/migrate.sh
echo "✅ Downloaded migration toolkit"
```

### Phase 2: Migration Execution

```bash
#!/bin/bash
# execute-migration.sh

echo "=== Phase 2: Executing Migration ==="

# 1. Detect repository type
detect_repo_type() {
  if [ -f "Cargo.toml" ]; then
    echo "rust-service"
  elif [ -f "package.json" ]; then
    echo "typescript-service"
  elif [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    echo "python-service"
  elif [ -f "go.mod" ]; then
    echo "go-service"
  else
    echo "base-template"
  fi
}

REPO_TYPE=$(detect_repo_type)
echo "Detected repository type: $REPO_TYPE"

# 2. Create new configuration
cat > .claude/project.json << EOF
{
  "name": "$(basename $(pwd))",
  "description": "$(gh repo view --json description -q .description)",
  "extends": "github:raibid-labs/claude-org-config/templates/repo-types/${REPO_TYPE}.json",
  "migration": {
    "from_version": "standalone",
    "to_version": "org-config-1.0",
    "date": "$(date -I)",
    "preserved_settings": {}
  }
}
EOF

# 3. Merge existing customizations
if [ -f ".claude.backup.$(date +%Y%m%d)*/project.json" ]; then
  echo "Merging existing customizations..."

  # Extract custom MCP servers
  CUSTOM_MCP=$(jq '.mcp_servers' .claude.backup.*/project.json)
  if [ "$CUSTOM_MCP" != "null" ]; then
    jq --argjson mcp "$CUSTOM_MCP" '.mcp_servers = $mcp' .claude/project.json > tmp.json
    mv tmp.json .claude/project.json
    echo "✅ Preserved MCP servers"
  fi

  # Extract custom rules
  CUSTOM_RULES=$(jq '.rules[]?' .claude.backup.*/project.json | jq -R -s -c 'split("\n") | map(select(length > 0))')
  if [ "$CUSTOM_RULES" != "[]" ]; then
    jq --argjson rules "$CUSTOM_RULES" '.rules.repo_specific = $rules' .claude/project.json > tmp.json
    mv tmp.json .claude/project.json
    echo "✅ Preserved custom rules"
  fi
fi

echo "✅ Migration executed"
```

### Phase 3: Validation

```bash
#!/bin/bash
# validate-migration.sh

echo "=== Phase 3: Validating Migration ==="

# 1. Validate JSON structure
echo -n "Checking JSON validity... "
if jq . .claude/project.json > /dev/null 2>&1; then
  echo "✅"
else
  echo "❌ Invalid JSON"
  exit 1
fi

# 2. Verify extends is correct
echo -n "Checking org config extension... "
EXTENDS=$(jq -r '.extends' .claude/project.json)
if [[ $EXTENDS == *"raibid-labs/claude-org-config"* ]]; then
  echo "✅"
else
  echo "❌ Not extending org config"
  exit 1
fi

# 3. Test with Claude Code
echo "Testing with Claude Code..."
if command -v claude-code &> /dev/null; then
  claude-code --validate-config
  echo "✅ Configuration validated"
else
  echo "⚠️  Claude Code not installed, skipping runtime validation"
fi

# 4. Check for missing references
echo "Checking file references..."
jq -r '.rules.repo_specific[]?' .claude/project.json | while read file; do
  if [ -f "$file" ]; then
    echo "  ✅ $file"
  else
    echo "  ❌ Missing: $file"
  fi
done

# 5. Compare with backup
if ls .claude.backup.* > /dev/null 2>&1; then
  echo "\n## Configuration Comparison:"
  echo "### Fields in original but not in new:"
  diff <(jq 'keys[]' .claude.backup.*/project.json | sort) \
       <(jq 'keys[]' .claude/project.json | sort) | grep '<' || echo "None"

  echo "### Fields in new but not in original:"
  diff <(jq 'keys[]' .claude.backup.*/project.json | sort) \
       <(jq 'keys[]' .claude/project.json | sort) | grep '>' || echo "None"
fi

echo "\n✅ Validation complete"
```

---

## Handling Existing Configurations

### Merging Configuration Files

```javascript
// merge-configs.js
const fs = require('fs');

function mergeConfigurations(existing, orgConfig) {
  const merged = {
    ...orgConfig,
    name: existing.name,
    description: existing.description,
    extends: orgConfig.extends || "github:raibid-labs/claude-org-config/templates/repo-types/base-template.json"
  };

  // Merge rules
  if (existing.rules) {
    merged.rules = {
      org_rules: "inherit",
      repo_specific: Array.isArray(existing.rules) ? existing.rules : [existing.rules],
      ...orgConfig.rules
    };
  }

  // Merge MCP servers
  if (existing.mcp_servers) {
    merged.mcp_servers = {
      inherit_org: true,
      custom: existing.mcp_servers
    };
  }

  // Preserve custom knowledge sources
  if (existing.knowledge_sources) {
    merged.knowledge_sources = [
      ...(orgConfig.knowledge_sources || []),
      ...existing.knowledge_sources
    ];
  }

  // Keep environment variables
  if (existing.env) {
    merged.env = {
      ...orgConfig.env,
      ...existing.env
    };
  }

  return merged;
}

// Usage
const existing = JSON.parse(fs.readFileSync('.claude.backup/project.json'));
const orgConfig = JSON.parse(fs.readFileSync('.claude/project.json'));
const merged = mergeConfigurations(existing, orgConfig);
fs.writeFileSync('.claude/project.json', JSON.stringify(merged, null, 2));
```

### Preserving Custom Rules

```bash
#!/bin/bash
# preserve-custom-rules.sh

echo "=== Preserving Custom Rules ==="

# 1. Identify custom rule files
CUSTOM_RULES=()
if [ -d ".claude.backup" ]; then
  while IFS= read -r rule; do
    if [[ $rule != *"raibid-labs/claude-org-config"* ]]; then
      CUSTOM_RULES+=("$rule")
    fi
  done < <(jq -r '.rules[]?' .claude.backup/project.json 2>/dev/null)
fi

# 2. Copy custom rule files to new structure
if [ ${#CUSTOM_RULES[@]} -gt 0 ]; then
  mkdir -p .claude/custom-rules
  for rule in "${CUSTOM_RULES[@]}"; do
    if [ -f "$rule" ]; then
      cp "$rule" ".claude/custom-rules/$(basename $rule)"
      echo "✅ Preserved: $rule"
    fi
  done

  # 3. Update project.json to reference them
  jq --arg rules "$(printf '.claude/custom-rules/%s\n' "${CUSTOM_RULES[@]}")" \
    '.rules.repo_specific = ($rules | split("\n") | map(select(length > 0)))' \
    .claude/project.json > tmp.json
  mv tmp.json .claude/project.json
fi
```

### Migrating MCP Servers

```json
// Before migration
{
  "mcp_servers": {
    "custom-server": {
      "command": "node",
      "args": ["./custom-server.js"]
    },
    "database-context": {
      "command": "npx",
      "args": ["db-mcp-server"]
    }
  }
}

// After migration
{
  "extends": "github:raibid-labs/claude-org-config/templates/repo-types/base-template.json",
  "mcp_servers": {
    "inherit_org": true,  // Get org servers
    "custom": {          // Keep custom servers
      "custom-server": {
        "command": "node",
        "args": ["./custom-server.js"]
      },
      "database-context": {
        "command": "npx",
        "args": ["db-mcp-server"]
      }
    }
  }
}
```

---

## Conflict Resolution

### Common Conflicts and Solutions

#### Conflict: Duplicate MCP Servers

```json
{
  "conflict_resolution": {
    "mcp_servers": {
      "strategy": "merge_prefer_local",
      "duplicates": {
        "repo-context": {
          "use": "local",
          "reason": "Local version has repo-specific configuration"
        }
      }
    }
  }
}
```

#### Conflict: Incompatible Rules

```json
{
  "conflict_resolution": {
    "rules": {
      "incompatible": [
        {
          "org_rule": "use-tabs",
          "repo_rule": "use-spaces",
          "resolution": "override_with_repo",
          "justification": "Historical codebase uses spaces"
        }
      ]
    }
  }
}
```

#### Conflict: Version Mismatches

```json
{
  "compatibility": {
    "org_config_version": "1.0.0",
    "repo_requires": "0.9.0",
    "resolution": {
      "use_compatibility_mode": true,
      "adapter": "./adapters/v0.9-to-v1.0.js"
    }
  }
}
```

### Automated Conflict Resolution

```javascript
// resolve-conflicts.js
function resolveConflicts(orgConfig, repoConfig) {
  const conflicts = [];
  const resolutions = {};

  // Check for rule conflicts
  if (orgConfig.rules && repoConfig.rules) {
    const orgRules = new Set(orgConfig.rules);
    const repoRules = new Set(repoConfig.rules);

    repoRules.forEach(rule => {
      if (orgRules.has(rule)) {
        conflicts.push({
          type: 'rule',
          item: rule,
          resolution: 'keep_both'
        });
      }
    });
  }

  // Check for MCP server conflicts
  if (orgConfig.mcp_servers && repoConfig.mcp_servers) {
    Object.keys(repoConfig.mcp_servers).forEach(server => {
      if (orgConfig.mcp_servers[server]) {
        conflicts.push({
          type: 'mcp_server',
          item: server,
          resolution: 'prefer_repo'
        });
        resolutions[`mcp_servers.${server}`] = repoConfig.mcp_servers[server];
      }
    });
  }

  return { conflicts, resolutions };
}
```

---

## Testing & Validation

### Automated Testing Suite

```bash
#!/bin/bash
# test-migration.sh

echo "=== Running Migration Tests ==="

# Test suite
TESTS_PASSED=0
TESTS_FAILED=0

# Test 1: Configuration loads
test_config_loads() {
  echo -n "Test: Configuration loads... "
  if jq . .claude/project.json > /dev/null 2>&1; then
    echo "✅ PASS"
    ((TESTS_PASSED++))
  else
    echo "❌ FAIL"
    ((TESTS_FAILED++))
  fi
}

# Test 2: Extends org config
test_extends_org() {
  echo -n "Test: Extends org config... "
  EXTENDS=$(jq -r '.extends' .claude/project.json)
  if [[ $EXTENDS == *"raibid-labs"* ]]; then
    echo "✅ PASS"
    ((TESTS_PASSED++))
  else
    echo "❌ FAIL"
    ((TESTS_FAILED++))
  fi
}

# Test 3: Custom settings preserved
test_customizations_preserved() {
  echo -n "Test: Customizations preserved... "
  if [ -f ".claude.backup/project.json" ]; then
    OLD_MCP_COUNT=$(jq '.mcp_servers | length' .claude.backup/project.json 2>/dev/null || echo 0)
    NEW_MCP_COUNT=$(jq '.mcp_servers.custom | length' .claude/project.json 2>/dev/null || echo 0)
    if [ $OLD_MCP_COUNT -eq $NEW_MCP_COUNT ]; then
      echo "✅ PASS"
      ((TESTS_PASSED++))
    else
      echo "❌ FAIL (MCP servers: $OLD_MCP_COUNT -> $NEW_MCP_COUNT)"
      ((TESTS_FAILED++))
    fi
  else
    echo "⚠️  SKIP (no backup)"
  fi
}

# Test 4: File references valid
test_file_references() {
  echo -n "Test: File references valid... "
  MISSING=0
  jq -r '.rules.repo_specific[]?' .claude/project.json 2>/dev/null | while read file; do
    if [ ! -f "$file" ]; then
      ((MISSING++))
    fi
  done
  if [ $MISSING -eq 0 ]; then
    echo "✅ PASS"
    ((TESTS_PASSED++))
  else
    echo "❌ FAIL ($MISSING missing files)"
    ((TESTS_FAILED++))
  fi
}

# Test 5: Claude Code validation
test_claude_validation() {
  echo -n "Test: Claude Code validation... "
  if command -v claude-code &> /dev/null; then
    if claude-code --validate-config > /dev/null 2>&1; then
      echo "✅ PASS"
      ((TESTS_PASSED++))
    else
      echo "❌ FAIL"
      ((TESTS_FAILED++))
    fi
  else
    echo "⚠️  SKIP (Claude Code not installed)"
  fi
}

# Run all tests
test_config_loads
test_extends_org
test_customizations_preserved
test_file_references
test_claude_validation

# Summary
echo "\n=== Test Summary ==="
echo "Passed: $TESTS_PASSED"
echo "Failed: $TESTS_FAILED"

if [ $TESTS_FAILED -eq 0 ]; then
  echo "✅ All tests passed!"
  exit 0
else
  echo "❌ Some tests failed. Review before proceeding."
  exit 1
fi
```

### Integration Testing

```bash
#!/bin/bash
# integration-test.sh

echo "=== Integration Testing ==="

# Test 1: CI/CD still works
echo "Test: CI/CD Pipeline"
if [ -d ".github/workflows" ]; then
  gh workflow run test --repo $(gh repo view --json nameWithOwner -q .nameWithOwner)
  echo "✅ CI/CD triggered successfully"
fi

# Test 2: Development workflow
echo "Test: Development Workflow"
claude-code --prompt "Show me the repository structure and explain the coding standards"

# Test 3: Team collaboration
echo "Test: Team Collaboration"
git add .claude/
git commit -m "test: migration to org config"
git push origin migration/org-config-adoption

# Create test PR
gh pr create \
  --draft \
  --title "[TEST] Migration to org config" \
  --body "Testing migration. DO NOT MERGE until validated."
```

---

## Rollback Procedures

### Quick Rollback

```bash
#!/bin/bash
# rollback-quick.sh

echo "=== Quick Rollback ==="

# Check for backup
if [ ! -d ".claude.backup."* ]; then
  echo "❌ No backup found!"
  exit 1
fi

# Restore from most recent backup
LATEST_BACKUP=$(ls -d .claude.backup.* | sort -r | head -1)
echo "Restoring from: $LATEST_BACKUP"

# Remove current config
rm -rf .claude

# Restore backup
cp -r "$LATEST_BACKUP" .claude

echo "✅ Rolled back to previous configuration"

# Clean up migration branch
git checkout main
git branch -D migration/org-config-adoption

echo "✅ Rollback complete"
```

### Partial Rollback

```bash
#!/bin/bash
# rollback-partial.sh

echo "=== Partial Rollback ==="

# Keep org extension but restore customizations
if [ -f ".claude.backup/project.json" ]; then
  # Extract customizations from backup
  CUSTOM_MCP=$(jq '.mcp_servers' .claude.backup/project.json)
  CUSTOM_RULES=$(jq '.rules' .claude.backup/project.json)

  # Apply to current config
  jq --argjson mcp "$CUSTOM_MCP" --argjson rules "$CUSTOM_RULES" \
    '.mcp_servers.custom = $mcp | .rules.repo_specific = $rules' \
    .claude/project.json > tmp.json
  mv tmp.json .claude/project.json

  echo "✅ Restored customizations while keeping org config"
fi
```

### Emergency Rollback

```bash
#!/bin/bash
# emergency-rollback.sh

echo "🚨 EMERGENCY ROLLBACK 🚨"

# 1. Restore from git
git checkout main -- .claude/

# 2. If that fails, restore from backup tarball
if [ -f "claude-config-backup-*.tar.gz" ]; then
  BACKUP_TAR=$(ls claude-config-backup-*.tar.gz | sort -r | head -1)
  tar -xzf "$BACKUP_TAR"
  echo "✅ Restored from tarball: $BACKUP_TAR"
fi

# 3. If all else fails, remove config
if [ $? -ne 0 ]; then
  echo "⚠️  Removing all Claude configuration"
  rm -rf .claude
  echo "❌ Configuration removed. Manual reconfiguration required."
fi

# 4. Notify team
echo "🔔 Notifying team of rollback..."
gh issue create \
  --title "🚨 Emergency rollback of Claude config migration" \
  --body "Migration rolled back due to critical issues. Please review before attempting again."
```

---

## Migration Examples

### Example 1: Simple Service Migration

```bash
# Before: Standalone configuration
.claude/
├── project.json (minimal, custom)
└── rules.md

# After: Org-integrated configuration
.claude/
├── project.json (extends org config)
├── custom-rules/
│   └── api-conventions.md (preserved)
└── migration-log.md
```

**Migration script:**
```bash
#!/bin/bash
curl -fsSL https://raw.githubusercontent.com/raibid-labs/claude-org-config/main/scripts/migrate-simple.sh | bash
```

### Example 2: Complex Monorepo Migration

```json
// Complex migration configuration
{
  "name": "platform-monorepo",
  "migration": {
    "strategy": "incremental",
    "phases": [
      {
        "phase": 1,
        "scope": "shared-libraries",
        "extends": "github:raibid-labs/claude-org-config/templates/repo-types/library.json"
      },
      {
        "phase": 2,
        "scope": "services",
        "extends": "github:raibid-labs/claude-org-config/templates/repo-types/service.json"
      },
      {
        "phase": 3,
        "scope": "infrastructure",
        "extends": "github:raibid-labs/claude-org-config/templates/repo-types/infrastructure.json"
      }
    ]
  },
  "workspaces": {
    "packages/*": "library-template",
    "services/*": "service-template",
    "infrastructure/*": "infra-template"
  }
}
```

### Example 3: Legacy System Migration

```bash
#!/bin/bash
# migrate-legacy.sh

# Special handling for legacy systems
echo "=== Migrating Legacy System ==="

# 1. Create compatibility layer
cat > .claude/compatibility.json << 'EOF'
{
  "legacy_mappings": {
    "old_rule_system": "new_rule_system",
    "deprecated_mcp": "modern_mcp"
  },
  "adapters": [
    "./adapters/legacy-to-modern.js"
  ]
}
EOF

# 2. Gradual migration plan
cat > .claude/migration-plan.md << 'EOF'
# Legacy System Migration Plan

## Phase 1 (Weeks 1-2)
- Add org config alongside legacy
- Run in compatibility mode
- Monitor for issues

## Phase 2 (Weeks 3-4)
- Migrate team workflows
- Update documentation
- Train team members

## Phase 3 (Weeks 5-6)
- Remove legacy configuration
- Full org config adoption
- Performance optimization
EOF
```

---

## Post-Migration Checklist

### Immediate Tasks (Day 1)

- [ ] Verify configuration loads in Claude Code
- [ ] Test primary development workflows
- [ ] Check CI/CD pipelines still function
- [ ] Ensure MCP servers connect properly
- [ ] Validate file references are correct
- [ ] Confirm team can access repository
- [ ] Document any immediate issues

### Week 1 Tasks

- [ ] Monitor team feedback
- [ ] Address any workflow disruptions
- [ ] Fine-tune customizations
- [ ] Update repository documentation
- [ ] Create team training materials
- [ ] Schedule team onboarding session
- [ ] Review and optimize configuration

### Month 1 Tasks

- [ ] Collect metrics on improvement
- [ ] Document lessons learned
- [ ] Share migration experience with org
- [ ] Optimize for team-specific needs
- [ ] Plan for future updates
- [ ] Remove backup files if stable
- [ ] Close migration tracking issue

### Success Metrics

```bash
#!/bin/bash
# measure-success.sh

echo "=== Migration Success Metrics ==="

# Metric 1: Configuration complexity reduction
echo "## Configuration Complexity"
echo -n "Before: "
[ -f .claude.backup/project.json ] && wc -l .claude.backup/project.json
echo -n "After: "
wc -l .claude/project.json

# Metric 2: Shared vs custom rules
echo "## Rule Distribution"
SHARED=$(jq '.rules.org_rules' .claude/project.json)
CUSTOM=$(jq '.rules.repo_specific | length' .claude/project.json)
echo "Shared rules: $SHARED"
echo "Custom rules: $CUSTOM"

# Metric 3: Development velocity
echo "## Development Metrics"
echo "PRs since migration: $(gh pr list --state all --search 'created:>2024-01-01' --json number | jq length)"
echo "Avg PR review time: [Calculate from PR data]"

# Metric 4: Team satisfaction
echo "## Team Feedback"
echo "Run: gh issue view [MIGRATION_FEEDBACK_ISSUE]"
```

---

## Troubleshooting

### Common Migration Issues

#### Issue: "Configuration not recognized after migration"

**Solution:**
```bash
# Verify extends path
jq '.extends' .claude/project.json

# Should output: github:raibid-labs/claude-org-config/...
# If not, fix the path
```

#### Issue: "Lost custom MCP servers"

**Solution:**
```bash
# Restore from backup
jq '.mcp_servers' .claude.backup/project.json > mcp-backup.json

# Merge into new config
jq --slurpfile mcp mcp-backup.json '.mcp_servers.custom = $mcp[0]' .claude/project.json > tmp.json
mv tmp.json .claude/project.json
```

#### Issue: "Team workflows broken"

**Solution:**
```bash
# Create compatibility mode
cat >> .claude/project.json << 'EOF'
{
  "compatibility_mode": {
    "enabled": true,
    "support_legacy_commands": true,
    "aliases": {
      "old_command": "new_command"
    }
  }
}
EOF
```

#### Issue: "Merge conflicts in migration PR"

**Solution:**
```bash
# Resolve conflicts favoring migration
git checkout migration/org-config-adoption
git rebase main

# If complex conflicts
git checkout main -- .
git checkout migration/org-config-adoption -- .claude/

# Manually merge necessary changes
```

### Getting Migration Help

1. **Check migration guide:**
   ```bash
   open https://github.com/raibid-labs/claude-org-config/blob/main/docs/MIGRATION.md
   ```

2. **Run diagnostics:**
   ```bash
   curl -fsSL https://raw.githubusercontent.com/raibid-labs/claude-org-config/main/scripts/diagnose-migration.sh | bash
   ```

3. **Get support:**
   ```bash
   gh issue create \
     --repo raibid-labs/claude-org-config \
     --label "migration-help" \
     --title "Migration help: [your issue]"
   ```

---

## Summary

Successful migration requires:
1. **Careful assessment** of existing configuration
2. **Appropriate strategy** selection
3. **Preservation** of essential customizations
4. **Thorough testing** before deployment
5. **Clear rollback** procedures
6. **Team communication** throughout

Remember:
- Always backup before migrating
- Test thoroughly in a branch
- Migrate incrementally for complex repos
- Document your migration process
- Share learnings with the team

For additional resources:
- [SETUP.md](./SETUP.md) - New repository setup
- [CUSTOMIZATION.md](./CUSTOMIZATION.md) - Customization guide
- [Organization Config Repository](https://github.com/raibid-labs/claude-org-config)
- [Migration Support Channel](slack://raibid-labs/claude-migration)