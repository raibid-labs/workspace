#!/usr/bin/env bash
set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
ORG="raibid-labs"
BASE_CONFIG_URL="https://raw.githubusercontent.com/raibid-labs/workspace/main/.claude/base-project.json"
WORKSPACE_DIR="/home/beengud/raibid-labs"
DRY_RUN=${DRY_RUN:-false}

# Counters
TOTAL_REPOS=0
REPOS_WITH_CONFIG=0
REPOS_FIXED=0
REPOS_CREATED=0
REPOS_SKIPPED=0

# Arrays to track repos
declare -a FIXED_REPOS
declare -a CREATED_REPOS
declare -a SKIPPED_REPOS
declare -a ERROR_REPOS

echo -e "${BLUE}==================================================================${NC}"
echo -e "${BLUE}  Raibid Labs Claude Configuration Audit and Fix${NC}"
echo -e "${BLUE}==================================================================${NC}"
echo ""

if [ "$DRY_RUN" = "true" ]; then
    echo -e "${YELLOW}Running in DRY RUN mode - no changes will be made${NC}"
    echo ""
fi

# Function to detect repository type based on files and structure
detect_repo_type() {
    local repo_dir=$1

    # Check for specific markers
    if [ -f "$repo_dir/Cargo.toml" ]; then
        echo "rust-service"
    elif [ -f "$repo_dir/package.json" ]; then
        local pkg_content=$(cat "$repo_dir/package.json")
        if echo "$pkg_content" | grep -q "@modelcontextprotocol/sdk"; then
            echo "mcp-integration"
        elif echo "$pkg_content" | grep -q "vitepress\|docusaurus\|mkdocs"; then
            echo "typescript-docs"
        else
            echo "library"
        fi
    elif [ -f "$repo_dir/pyproject.toml" ] || [ -f "$repo_dir/setup.py" ]; then
        if echo "$repo_dir" | grep -q "^dgx-"; then
            echo "python-ml"
        else
            echo "library"
        fi
    elif [ -d "$repo_dir/terraform" ] || [ -d "$repo_dir/k8s" ] || [ -d "$repo_dir/kubernetes" ]; then
        echo "iac-k8s"
    elif [ -f "$repo_dir/mkdocs.yml" ] || [ -f "$repo_dir/docusaurus.config.js" ]; then
        echo "docs"
    else
        echo "library"  # Default fallback
    fi
}

# Function to create .claude/project.json
create_claude_config() {
    local repo_dir=$1
    local repo_name=$2
    local repo_type=$3

    local config_dir="$repo_dir/.claude"
    local config_file="$config_dir/project.json"

    # Create .claude directory if it doesn't exist
    if [ "$DRY_RUN" = "false" ]; then
        mkdir -p "$config_dir"
    fi

    # Determine primary language
    local primary_lang="unknown"
    case $repo_type in
        rust-service) primary_lang="rust" ;;
        python-ml) primary_lang="python" ;;
        typescript-docs) primary_lang="typescript" ;;
        mcp-integration) primary_lang="typescript" ;;
        iac-k8s) primary_lang="hcl" ;;
        docs) primary_lang="markdown" ;;
        *) primary_lang="unknown" ;;
    esac

    # Create the config file
    cat > "$config_file" << EOF
{
  "\$schema": "https://claude.ai/schemas/project-config.json",
  "version": "1.0.0",
  "extends": "$BASE_CONFIG_URL",
  "description": "Claude Code configuration for $repo_name",

  "project": {
    "name": "$repo_name",
    "type": "$repo_type",
    "repository": "https://github.com/$ORG/$repo_name"
  },

  "language": {
    "primary": "$primary_lang"
  },

  "customization": {
    "mcpServers": {},
    "workflows": {},
    "agents": []
  }
}
EOF

    echo -e "  ${GREEN}✓${NC} Created .claude/project.json (type: $repo_type, language: $primary_lang)"
}

# Function to check and fix existing config
check_and_fix_config() {
    local repo_dir=$1
    local repo_name=$2
    local config_file="$repo_dir/.claude/project.json"

    # Read the current config
    local current_extends=$(jq -r '.extends // "none"' "$config_file" 2>/dev/null || echo "invalid")

    if [ "$current_extends" = "invalid" ]; then
        echo -e "  ${RED}✗${NC} Invalid JSON in .claude/project.json"
        ERROR_REPOS+=("$repo_name")
        return 1
    fi

    # Check if it extends the base config
    if [[ "$current_extends" == *"workspace"* ]] && [[ "$current_extends" == *"base-project.json"* ]]; then
        echo -e "  ${GREEN}✓${NC} Already extends base configuration correctly"
        return 0
    elif [ "$current_extends" = "none" ] || [ "$current_extends" = "null" ]; then
        echo -e "  ${YELLOW}⚠${NC}  Missing 'extends' field"

        if [ "$DRY_RUN" = "false" ]; then
            # Add extends field
            local temp_file=$(mktemp)
            jq ". + {\"extends\": \"$BASE_CONFIG_URL\"}" "$config_file" > "$temp_file"
            mv "$temp_file" "$config_file"
            echo -e "  ${GREEN}✓${NC} Added extends field"
        else
            echo -e "  ${BLUE}[DRY RUN]${NC} Would add extends field"
        fi

        FIXED_REPOS+=("$repo_name")
        ((REPOS_FIXED++))
        return 0
    else
        echo -e "  ${YELLOW}⚠${NC}  Extends different config: $current_extends"

        if [ "$DRY_RUN" = "false" ]; then
            # Update extends field
            local temp_file=$(mktemp)
            jq ".extends = \"$BASE_CONFIG_URL\"" "$config_file" > "$temp_file"
            mv "$temp_file" "$config_file"
            echo -e "  ${GREEN}✓${NC} Updated extends field"
        else
            echo -e "  ${BLUE}[DRY RUN]${NC} Would update extends field"
        fi

        FIXED_REPOS+=("$repo_name")
        ((REPOS_FIXED++))
        return 0
    fi
}

# Get list of all non-archived repos
echo "Fetching repository list from GitHub..."
REPOS=$(gh repo list $ORG --limit 100 --json name,isArchived | jq -r '.[] | select(.isArchived == false) | .name' | sort)

echo -e "${GREEN}Found $(echo "$REPOS" | wc -l) active repositories${NC}"
echo ""

# Process each repository
for repo in $REPOS; do
    ((TOTAL_REPOS++))

    echo -e "${BLUE}[$TOTAL_REPOS] Processing: $repo${NC}"

    repo_dir="$WORKSPACE_DIR/$repo"

    # Check if repo is cloned locally
    if [ ! -d "$repo_dir" ]; then
        echo -e "  ${YELLOW}⚠${NC}  Not cloned locally - skipping"
        SKIPPED_REPOS+=("$repo (not cloned)")
        ((REPOS_SKIPPED++))
        echo ""
        continue
    fi

    # Skip the workspace repo itself
    if [ "$repo" = "workspace" ]; then
        echo -e "  ${BLUE}ℹ${NC}  Skipping workspace repository (this is the base config repo)"
        SKIPPED_REPOS+=("$repo (workspace)")
        ((REPOS_SKIPPED++))
        echo ""
        continue
    fi

    config_file="$repo_dir/.claude/project.json"

    if [ -f "$config_file" ]; then
        ((REPOS_WITH_CONFIG++))
        echo -e "  ${GREEN}✓${NC} Has .claude/project.json"
        check_and_fix_config "$repo_dir" "$repo"
    else
        echo -e "  ${YELLOW}⚠${NC}  Missing .claude/project.json"

        # Detect repo type
        repo_type=$(detect_repo_type "$repo_dir")
        echo -e "  ${BLUE}ℹ${NC}  Detected type: $repo_type"

        if [ "$DRY_RUN" = "false" ]; then
            create_claude_config "$repo_dir" "$repo" "$repo_type"
            CREATED_REPOS+=("$repo")
            ((REPOS_CREATED++))
        else
            echo -e "  ${BLUE}[DRY RUN]${NC} Would create .claude/project.json (type: $repo_type)"
            CREATED_REPOS+=("$repo")
            ((REPOS_CREATED++))
        fi
    fi

    echo ""
done

# Generate summary report
echo -e "${BLUE}==================================================================${NC}"
echo -e "${BLUE}  Summary Report${NC}"
echo -e "${BLUE}==================================================================${NC}"
echo ""
echo -e "Total repositories processed: ${BLUE}$TOTAL_REPOS${NC}"
echo -e "Repositories with existing config: ${GREEN}$REPOS_WITH_CONFIG${NC}"
echo -e "Configurations created: ${GREEN}$REPOS_CREATED${NC}"
echo -e "Configurations fixed: ${YELLOW}$REPOS_FIXED${NC}"
echo -e "Repositories skipped: ${YELLOW}$REPOS_SKIPPED${NC}"
echo -e "Errors encountered: ${RED}${#ERROR_REPOS[@]}${NC}"
echo ""

if [ ${#CREATED_REPOS[@]} -gt 0 ]; then
    echo -e "${GREEN}Configurations Created:${NC}"
    for repo in "${CREATED_REPOS[@]}"; do
        echo -e "  - $repo"
    done
    echo ""
fi

if [ ${#FIXED_REPOS[@]} -gt 0 ]; then
    echo -e "${YELLOW}Configurations Fixed:${NC}"
    for repo in "${FIXED_REPOS[@]}"; do
        echo -e "  - $repo"
    done
    echo ""
fi

if [ ${#SKIPPED_REPOS[@]} -gt 0 ]; then
    echo -e "${YELLOW}Repositories Skipped:${NC}"
    for repo in "${SKIPPED_REPOS[@]}"; do
        echo -e "  - $repo"
    done
    echo ""
fi

if [ ${#ERROR_REPOS[@]} -gt 0 ]; then
    echo -e "${RED}Repositories with Errors:${NC}"
    for repo in "${ERROR_REPOS[@]}"; do
        echo -e "  - $repo"
    done
    echo ""
fi

if [ "$DRY_RUN" = "false" ]; then
    echo -e "${GREEN}✓ All changes have been applied${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Review the changes in each repository"
    echo "  2. Commit and push changes for each repository"
    echo "  3. Or use scripts/commit-all-configs.sh to commit all at once"
else
    echo -e "${BLUE}Dry run complete - no changes were made${NC}"
    echo ""
    echo "To apply changes, run:"
    echo "  ./scripts/audit-and-fix-claude-configs.sh"
fi

echo -e "${BLUE}==================================================================${NC}"
