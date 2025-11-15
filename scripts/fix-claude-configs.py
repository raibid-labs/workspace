#!/usr/bin/env python3
"""Fix Claude Code configurations across all raibid-labs repositories."""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

# Configuration
ORG = "raibid-labs"
WORKSPACE_DIR = Path("/home/beengud/raibid-labs")
BASE_CONFIG_URL = "https://raw.githubusercontent.com/raibid-labs/workspace/main/.claude/base-project.json"

# Colors
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

def detect_repo_type(repo_dir: Path) -> str:
    """Detect repository type based on files and structure."""
    if (repo_dir / "Cargo.toml").exists():
        return "rust-service"
    elif (repo_dir / "package.json").exists():
        try:
            with open(repo_dir / "package.json") as f:
                pkg = json.load(f)
                deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                if "@modelcontextprotocol/sdk" in deps:
                    return "mcp-integration"
                elif any(x in deps for x in ["vitepress", "docusaurus"]):
                    return "typescript-docs"
        except:
            pass
        return "library"
    elif (repo_dir / "pyproject.toml").exists() or (repo_dir / "setup.py").exists():
        if repo_dir.name.startswith("dgx-"):
            return "python-ml"
        return "library"
    elif (repo_dir / "terraform").is_dir() or (repo_dir / "k8s").is_dir():
        return "iac-k8s"
    elif (repo_dir / "mkdocs.yml").exists():
        return "docs"
    return "library"

def detect_primary_language(repo_type: str) -> str:
    """Detect primary language based on repo type."""
    mapping = {
        "rust-service": "rust",
        "python-ml": "python",
        "typescript-docs": "typescript",
        "mcp-integration": "typescript",
        "iac-k8s": "hcl",
        "docs": "markdown",
    }
    return mapping.get(repo_type, "unknown")

def create_config(repo_name: str, repo_type: str) -> dict:
    """Create a config template for a repository."""
    primary_lang = detect_primary_language(repo_type)

    return {
        "$schema": "https://claude.ai/schemas/project-config.json",
        "version": "1.0.0",
        "extends": BASE_CONFIG_URL,
        "description": f"Claude Code configuration for {repo_name}",
        "project": {
            "name": repo_name,
            "type": repo_type,
            "repository": f"https://github.com/{ORG}/{repo_name}"
        },
        "language": {
            "primary": primary_lang
        },
        "customization": {
            "mcpServers": {},
            "workflows": {},
            "agents": []
        }
    }

def fix_repository(repo_name: str, repo_dir: Path, dry_run: bool = False) -> str:
    """Fix configuration for a single repository."""
    config_file = repo_dir / ".claude" / "project.json"
    config_dir = repo_dir / ".claude"

    # Skip workspace
    if repo_name == "workspace":
        return "skipped"

    # Skip if not cloned
    if not repo_dir.exists():
        return "not_cloned"

    repo_type = detect_repo_type(repo_dir)

    # Create or fix config
    if not config_file.exists():
        # Create new config
        if not dry_run:
            config_dir.mkdir(exist_ok=True)
            config = create_config(repo_name, repo_type)
            with open(config_file, "w") as f:
                json.dump(config, f, indent=2)
                f.write("\n")  # Add trailing newline
        return "created"
    else:
        # Fix existing config
        try:
            with open(config_file) as f:
                config = json.load(f)

            extends = config.get("extends", "")

            # Check if extends is correct
            if "workspace" in extends and "base-project.json" in extends:
                return "ok"

            # Fix extends field
            if not dry_run:
                config["extends"] = BASE_CONFIG_URL
                with open(config_file, "w") as f:
                    json.dump(config, f, indent=2)
                    f.write("\n")

            return "fixed"

        except json.JSONDecodeError:
            return "error"

def main():
    # Parse arguments
    dry_run = "--dry-run" in sys.argv
    verbose = "--verbose" in sys.argv or "-v" in sys.argv

    print(f"{Colors.BLUE}{'='*70}{Colors.NC}")
    print(f"{Colors.BLUE}  Raibid Labs Claude Configuration Fix{Colors.NC}")
    print(f"{Colors.BLUE}{'='*70}{Colors.NC}\n")

    if dry_run:
        print(f"{Colors.YELLOW}Running in DRY RUN mode - no changes will be made{Colors.NC}\n")

    # Load audit report
    report_file = WORKSPACE_DIR / "workspace" / "claude-config-audit-report.json"

    if not report_file.exists():
        print(f"{Colors.RED}Error: Audit report not found. Run audit script first:{Colors.NC}")
        print("  python3 scripts/audit-claude-configs.py")
        sys.exit(1)

    with open(report_file) as f:
        report = json.load(f)

    results = report["results"]

    # Filter repos that need fixing
    to_fix = [r for r in results
              if r["status"] in ["missing_config", "wrong_extends", "no_extends"]
              and r["cloned"]]

    print(f"Found {Colors.YELLOW}{len(to_fix)}{Colors.NC} repositories that need fixing\n")

    if not to_fix:
        print(f"{Colors.GREEN}✓ All repositories are correctly configured!{Colors.NC}")
        return

    # Fix each repository
    fixed_count = 0
    created_count = 0
    error_count = 0
    skipped_count = 0

    for i, repo_info in enumerate(to_fix, 1):
        repo_name = repo_info["name"]
        repo_dir = WORKSPACE_DIR / repo_name

        print(f"[{i}/{len(to_fix)}] {repo_name}...", end=" ")

        result = fix_repository(repo_name, repo_dir, dry_run=dry_run)

        if result == "created":
            print(f"{Colors.GREEN}✓ Created{Colors.NC}")
            created_count += 1
            if verbose:
                print(f"       Type: {repo_info['repo_type']}")
        elif result == "fixed":
            print(f"{Colors.YELLOW}✓ Fixed{Colors.NC}")
            fixed_count += 1
            if verbose:
                print(f"       Issue: {repo_info.get('issue', 'Unknown')}")
        elif result == "ok":
            print(f"{Colors.GREEN}✓ Already OK{Colors.NC}")
        elif result == "error":
            print(f"{Colors.RED}✗ Error{Colors.NC}")
            error_count += 1
        elif result == "not_cloned":
            print(f"{Colors.BLUE}ℹ Skipped (not cloned){Colors.NC}")
            skipped_count += 1
        elif result == "skipped":
            print(f"{Colors.BLUE}ℹ Skipped{Colors.NC}")
            skipped_count += 1

    # Summary
    print(f"\n{Colors.BLUE}{'='*70}{Colors.NC}")
    print(f"{Colors.BLUE}  Summary{Colors.NC}")
    print(f"{Colors.BLUE}{'='*70}{Colors.NC}\n")

    print(f"{Colors.GREEN}✓{Colors.NC} Configurations created: {Colors.GREEN}{created_count}{Colors.NC}")
    print(f"{Colors.YELLOW}✓{Colors.NC} Configurations fixed: {Colors.YELLOW}{fixed_count}{Colors.NC}")
    if error_count > 0:
        print(f"{Colors.RED}✗{Colors.NC} Errors: {Colors.RED}{error_count}{Colors.NC}")
    if skipped_count > 0:
        print(f"{Colors.BLUE}ℹ{Colors.NC}  Skipped: {skipped_count}")

    if dry_run:
        print(f"\n{Colors.BLUE}Dry run complete - no changes were made{Colors.NC}")
        print(f"\nTo apply changes, run:")
        print(f"  python3 scripts/fix-claude-configs.py")
    else:
        print(f"\n{Colors.GREEN}✓ All changes have been applied{Colors.NC}")
        print(f"\nNext steps:")
        print(f"  1. Run audit again to verify: python3 scripts/audit-claude-configs.py")
        print(f"  2. Review changes in each repository")
        print(f"  3. Commit changes to each repository")

    print(f"\n{Colors.BLUE}{'='*70}{Colors.NC}")

if __name__ == "__main__":
    main()
