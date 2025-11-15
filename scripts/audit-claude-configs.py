#!/usr/bin/env python3
"""Audit Claude Code configurations across all raibid-labs repositories."""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple

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

def get_active_repos() -> List[str]:
    """Get list of active (non-archived) repositories."""
    result = subprocess.run(
        ["gh", "repo", "list", ORG, "--limit", "100", "--json", "name,isArchived"],
        capture_output=True,
        text=True,
        check=True
    )
    repos = json.loads(result.stdout)
    return sorted([r["name"] for r in repos if not r["isArchived"]])

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

def check_config(repo_name: str, repo_dir: Path) -> Dict:
    """Check repository configuration status."""
    config_file = repo_dir / ".claude" / "project.json"

    result = {
        "name": repo_name,
        "cloned": repo_dir.exists(),
        "has_config": config_file.exists(),
        "extends_base": False,
        "repo_type": None,
        "status": "unknown",
        "issue": None
    }

    if not result["cloned"]:
        result["status"] = "not_cloned"
        return result

    if repo_name == "workspace":
        result["status"] = "workspace"
        result["issue"] = "This is the base config repository"
        return result

    result["repo_type"] = detect_repo_type(repo_dir)

    if not result["has_config"]:
        result["status"] = "missing_config"
        result["issue"] = "No .claude/project.json found"
        return result

    # Check if config extends base
    try:
        with open(config_file) as f:
            config = json.load(f)
            extends = config.get("extends", "")

            if "workspace" in extends and "base-project.json" in extends:
                result["extends_base"] = True
                result["status"] = "ok"
            elif extends:
                result["status"] = "wrong_extends"
                result["issue"] = f"Extends: {extends}"
            else:
                result["status"] = "no_extends"
                result["issue"] = "No 'extends' field"
    except json.JSONDecodeError:
        result["status"] = "invalid_json"
        result["issue"] = "Invalid JSON in config file"
    except Exception as e:
        result["status"] = "error"
        result["issue"] = str(e)

    return result

def create_config_template(repo_name: str, repo_type: str) -> dict:
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

def main():
    print(f"{Colors.BLUE}{'='*70}{Colors.NC}")
    print(f"{Colors.BLUE}  Raibid Labs Claude Configuration Audit{Colors.NC}")
    print(f"{Colors.BLUE}{'='*70}{Colors.NC}\n")

    # Get repositories
    print("Fetching repository list from GitHub...")
    repos = get_active_repos()
    print(f"{Colors.GREEN}Found {len(repos)} active repositories{Colors.NC}\n")

    # Audit each repository
    results = []
    for i, repo in enumerate(repos, 1):
        repo_dir = WORKSPACE_DIR / repo
        result = check_config(repo, repo_dir)
        results.append(result)

    # Categorize results
    ok_repos = [r for r in results if r["status"] == "ok"]
    missing_config = [r for r in results if r["status"] == "missing_config"]
    wrong_extends = [r for r in results if r["status"] == "wrong_extends"]
    no_extends = [r for r in results if r["status"] == "no_extends"]
    not_cloned = [r for r in results if r["status"] == "not_cloned"]
    workspace_repos = [r for r in results if r["status"] == "workspace"]
    errors = [r for r in results if r["status"] in ["invalid_json", "error"]]

    # Print summary
    print(f"\n{Colors.BLUE}{'='*70}{Colors.NC}")
    print(f"{Colors.BLUE}  Summary{Colors.NC}")
    print(f"{Colors.BLUE}{'='*70}{Colors.NC}\n")

    print(f"Total repositories: {Colors.BLUE}{len(repos)}{Colors.NC}")
    print(f"{Colors.GREEN}✓{Colors.NC} Correct configuration: {Colors.GREEN}{len(ok_repos)}{Colors.NC}")
    print(f"{Colors.YELLOW}⚠{Colors.NC} Missing .claude/project.json: {Colors.YELLOW}{len(missing_config)}{Colors.NC}")
    print(f"{Colors.YELLOW}⚠{Colors.NC} Wrong 'extends' value: {Colors.YELLOW}{len(wrong_extends)}{Colors.NC}")
    print(f"{Colors.YELLOW}⚠{Colors.NC} No 'extends' field: {Colors.YELLOW}{len(no_extends)}{Colors.NC}")
    print(f"{Colors.BLUE}ℹ{Colors.NC}  Not cloned locally: {len(not_cloned)}")
    print(f"{Colors.BLUE}ℹ{Colors.NC}  Workspace repository: {len(workspace_repos)}")
    print(f"{Colors.RED}✗{Colors.NC} Errors: {Colors.RED}{len(errors)}{Colors.NC}\n")

    # Detailed output
    if missing_config:
        print(f"{Colors.YELLOW}Repositories missing .claude/project.json:{Colors.NC}")
        for r in missing_config:
            print(f"  - {r['name']} ({r['repo_type']})")
        print()

    if wrong_extends or no_extends:
        print(f"{Colors.YELLOW}Repositories with incorrect extends:{Colors.NC}")
        for r in wrong_extends + no_extends:
            print(f"  - {r['name']}: {r['issue']}")
        print()

    if errors:
        print(f"{Colors.RED}Repositories with errors:{Colors.NC}")
        for r in errors:
            print(f"  - {r['name']}: {r['issue']}")
        print()

    if ok_repos:
        print(f"{Colors.GREEN}Repositories with correct configuration:{Colors.NC}")
        for r in ok_repos:
            print(f"  - {r['name']}")
        print()

    # Save detailed report
    report_file = WORKSPACE_DIR / "workspace" / "claude-config-audit-report.json"
    with open(report_file, "w") as f:
        json.dump({
            "summary": {
                "total": len(repos),
                "ok": len(ok_repos),
                "missing_config": len(missing_config),
                "wrong_extends": len(wrong_extends),
                "no_extends": len(no_extends),
                "not_cloned": len(not_cloned),
                "errors": len(errors)
            },
            "results": results
        }, f, indent=2)

    print(f"{Colors.GREEN}✓ Detailed report saved to: {report_file}{Colors.NC}\n")

    # Offer to fix
    needs_fix = len(missing_config) + len(wrong_extends) + len(no_extends)
    if needs_fix > 0:
        print(f"{Colors.YELLOW}{needs_fix} repositories need configuration updates{Colors.NC}")
        print(f"\nTo apply fixes, run:")
        print(f"  python3 scripts/fix-claude-configs.py")

    print(f"\n{Colors.BLUE}{'='*70}{Colors.NC}")

if __name__ == "__main__":
    main()
