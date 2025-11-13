# Development Conventions - Raibid Labs

## Overview
This document defines organizational conventions for repository structure, naming, commits, documentation, and testing across all Raibid Labs projects.

---

## Repository Naming

### Prefix Conventions

**Production Services & Tools**:
```
raibid-*     # Core infrastructure and production tools
  raibid-ci         # CI/CD platform
  raibid-cli        # Official CLI tool
  raibid-labs-mcp   # MCP server implementation
```

**GPU/AI Workloads**:
```
dgx-*        # DGX-specific AI/ML workloads
  dgx-pixels       # Pixel processing/generation
  dgx-music        # Music generation/processing
  dgx-spark        # Hardware configuration
```

**Experimental Projects**:
```
hack-*       # Research and experimental work
  hack-agent-lightning  # AI agent research
  hack-k8s              # Kubernetes experiments
  hack-bevy             # Game engine exploration
  hack-browser          # Browser tool experiments
```

**Integration Projects**:
```
*-mcp        # Model Context Protocol integrations
  ardour-mcp          # Ardour DAW integration
  raibid-labs-mcp     # Organization MCP server
```

**Naming Rules**:
- Use lowercase with hyphens (kebab-case)
- Be descriptive but concise (2-3 words max)
- Prefix indicates category/purpose
- Avoid redundant terms (e.g., "raibid-raibid-tool")

**Examples**:
```
✅ Good:
  raibid-api-gateway
  dgx-training-pipeline
  hack-neural-compression

❌ Bad:
  RaibidAPIGateway      (camelCase)
  dgx_model_trainer     (snake_case)
  experimental-project  (no prefix)
  the-raibid-tool      (unnecessary article)
```

---

## File Naming

### Source Files

**Rust**:
```
mod.rs                  # Module entry point
lib.rs or main.rs       # Crate entry point
config.rs               # Configuration
models.rs               # Data models
utils.rs or helpers.rs  # Utility functions
```

**Python**:
```
__init__.py            # Package entry point
__main__.py            # Module entry point (python -m)
config.py              # Configuration
models.py              # Data models
utils.py or helpers.py # Utility functions
```

**TypeScript**:
```
index.ts               # Module entry point
config.ts              # Configuration
types.ts               # Type definitions
utils.ts or helpers.ts # Utility functions
```

### Configuration Files

```
Justfile                   # Task runner (preferred)
Makefile                   # Legacy task runner (migrate to Just)
Dockerfile                 # Container definition
Dockerfile.dev             # Development container
docker-compose.yml         # Multi-container development
.env.example               # Environment template (commit)
.env                       # Actual secrets (never commit)
pyproject.toml            # Python project config
Cargo.toml                # Rust project config
package.json              # Node.js project config
tsconfig.json             # TypeScript config
.editorconfig             # Editor settings
.gitignore                # Git ignore rules
.pre-commit-config.yaml   # Pre-commit hooks
```

---

## Directory Structure

### Standard Repository Layout

```
project-root/
├── .github/
│   ├── workflows/           # CI/CD workflows
│   │   ├── ci.yml
│   │   ├── release.yml
│   │   └── security.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── question.md
│   └── PULL_REQUEST_TEMPLATE.md
├── .claude/                # Claude Code configuration
│   ├── project.json
│   └── rules/
│       ├── code-style.md
│       ├── architecture.md
│       ├── security.md
│       └── conventions.md
├── src/                    # Source code
│   ├── main.rs            # Rust entry point
│   ├── lib.rs             # Library entry
│   └── modules/           # Feature modules
├── tests/                  # Test files
│   ├── integration/       # Integration tests
│   └── unit/              # Unit tests
├── docs/                   # Documentation
│   ├── architecture.md
│   ├── api.md
│   └── deployment.md
├── scripts/                # Build/deployment scripts
│   ├── build.nu
│   ├── test.nu
│   └── deploy.nu
├── config/                 # Configuration files
│   ├── dev.yaml
│   ├── staging.yaml
│   └── production.yaml
├── k8s/                    # Kubernetes manifests
│   ├── base/
│   └── overlays/
│       ├── dev/
│       ├── staging/
│       └── production/
├── docker/                 # Dockerfiles (if multiple)
│   ├── Dockerfile.rust
│   ├── Dockerfile.python
│   └── Dockerfile.web
├── examples/               # Usage examples
├── .gitignore
├── .editorconfig
├── .pre-commit-config.yaml
├── Justfile               # Task runner
├── Dockerfile             # Container definition
├── README.md              # Project overview
├── LICENSE                # License file
├── CHANGELOG.md           # Version history
└── CONTRIBUTING.md        # Contribution guide
```

### Multi-Language Projects

```
project-root/
├── rust/                  # Rust core
│   ├── Cargo.toml
│   └── src/
├── python/                # Python bindings/tools
│   ├── pyproject.toml
│   └── src/
├── typescript/            # Web frontend
│   ├── package.json
│   └── src/
├── shared/                # Shared resources
│   ├── schemas/          # API schemas
│   └── docs/
└── Justfile              # Unified task runner
```

---

## Commit Message Format

### Conventional Commits (Required)

**Format**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
```
feat      # New feature
fix       # Bug fix
docs      # Documentation changes
style     # Code style/formatting (no logic change)
refactor  # Code restructuring (no feature/fix)
perf      # Performance improvement
test      # Adding/updating tests
build     # Build system/dependencies
ci        # CI/CD configuration
chore     # Maintenance tasks
revert    # Revert previous commit
```

**Examples**:
```bash
# Feature
feat(api): add user authentication endpoint

Implement JWT-based authentication for the API.
- Add /auth/login endpoint
- Add /auth/refresh endpoint
- Add JWT middleware

Closes #123

# Bug fix
fix(parser): handle empty input correctly

Previously, empty input caused a panic. Now returns
an appropriate error message.

Fixes #456

# Breaking change
feat(api)!: change response format to JSON:API

BREAKING CHANGE: API responses now follow JSON:API spec.
Clients must update to parse the new format.

Closes #789
```

**Commit Rules**:
- Use imperative mood ("add" not "added" or "adds")
- First line max 72 characters
- Separate subject from body with blank line
- Wrap body at 72 characters
- Reference issues/PRs in footer
- Use `BREAKING CHANGE:` for breaking changes
- Capitalize first letter of subject
- No period at end of subject

**Scope Examples** (optional but recommended):
```
feat(auth): ...       # Authentication module
fix(db): ...         # Database layer
docs(readme): ...    # README file
test(api): ...       # API tests
ci(github): ...      # GitHub Actions
```

---

## Branch Naming

### Branch Patterns

```
main or master         # Production-ready code
develop               # Development integration branch (if using Gitflow)
feature/<name>        # New features
fix/<name>            # Bug fixes
hotfix/<name>         # Production hotfixes
release/<version>     # Release preparation
chore/<name>          # Maintenance tasks
docs/<name>           # Documentation updates
refactor/<name>       # Code refactoring
```

**Examples**:
```
✅ Good:
  feature/user-authentication
  fix/memory-leak-in-parser
  hotfix/critical-security-patch
  release/v1.2.0
  docs/api-documentation

❌ Bad:
  new-feature               (no type prefix)
  fix_bug                   (underscore instead of hyphen)
  feature/USER-AUTH         (uppercase)
  johns-branch              (personal name, no context)
```

---

## Pull Request & Issue Templates

### Pull Request Template

```markdown
# .github/PULL_REQUEST_TEMPLATE.md

## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to break)
- [ ] Documentation update
- [ ] Refactoring (no functional changes)
- [ ] Performance improvement
- [ ] Dependency update

## Related Issues
Closes #<issue-number>

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] All tests pass locally
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Dependent changes merged/documented
- [ ] No secrets/credentials in code

## Screenshots (if applicable)

## Additional Notes
```

### Issue Templates

**Bug Report**:
```markdown
# .github/ISSUE_TEMPLATE/bug_report.md

---
name: Bug Report
about: Report a bug to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

## Description
Clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 22.04]
- Version: [e.g., v1.2.3]
- Browser: [if applicable]
- Rust/Python/Node version:

## Additional Context
Logs, screenshots, etc.
```

**Feature Request**:
```markdown
# .github/ISSUE_TEMPLATE/feature_request.md

---
name: Feature Request
about: Suggest a new feature
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

## Problem Statement
What problem does this feature solve?

## Proposed Solution
How should this feature work?

## Alternatives Considered
What other approaches did you consider?

## Additional Context
Mockups, examples, etc.
```

---

## Documentation Requirements

### README.md (Required)

Every repository MUST have a comprehensive README:

```markdown
# Project Name

Brief description (1-2 sentences)

[![CI](https://github.com/raibid-labs/project/workflows/CI/badge.svg)](https://github.com/raibid-labs/project/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Features
- Feature 1
- Feature 2
- Feature 3

## Quick Start

### Prerequisites
- Rust 1.75+ / Python 3.11+ / Node 20+
- Docker (optional)
- Kubernetes (for deployment)

### Installation
```bash
# Clone repository
git clone https://github.com/raibid-labs/project.git
cd project

# Build
just build

# Run tests
just test

# Run locally
just run
```

## Usage

### Basic Example
```rust
// Code example
```

### Advanced Usage
See [docs/](docs/) for detailed documentation.

## Development

### Project Structure
```
src/
  ├── main.rs
  └── ...
```

### Available Commands
```bash
just build    # Build project
just test     # Run tests
just lint     # Run linters
just fmt      # Format code
```

## Deployment
See [docs/deployment.md](docs/deployment.md)

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md)

## License
[MIT License](LICENSE)

## Contact
- Issues: https://github.com/raibid-labs/project/issues
- Email: team@raibid-labs.io
```

### CONTRIBUTING.md (Required)

```markdown
# Contributing to Project Name

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Run tests and linters
6. Commit with conventional commits
7. Push and create a PR

## Development Setup

### Prerequisites
- Tools list

### Setup
```bash
# Setup commands
```

## Code Standards
- Follow [code-style.md](.claude/rules/code-style.md)
- Follow [architecture.md](.claude/rules/architecture.md)
- Follow [security.md](.claude/rules/security.md)

## Testing
- Write tests for new features
- Aim for 80%+ coverage
- All tests must pass before merge

## Commit Guidelines
Use [Conventional Commits](https://www.conventionalcommits.org/)

## Pull Request Process
1. Update documentation
2. Add tests
3. Ensure CI passes
4. Get 1+ approvals
5. Squash and merge

## Code Review
- Be respectful and constructive
- Focus on code, not people
- Suggest improvements clearly
- Approve when satisfied

## Questions?
Open an issue or contact maintainers.
```

### CHANGELOG.md (Required)

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New features in progress

### Changed
- Changes to existing features

### Deprecated
- Soon-to-be removed features

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security improvements

## [1.2.0] - 2024-01-15

### Added
- User authentication system (#123)
- API rate limiting (#145)

### Fixed
- Memory leak in parser (#156)

## [1.1.0] - 2024-01-01

### Added
- Initial release

[Unreleased]: https://github.com/raibid-labs/project/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/raibid-labs/project/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/raibid-labs/project/releases/tag/v1.1.0
```

---

## Testing Requirements

### Test Organization

```
tests/
├── integration/          # Integration tests
│   ├── api_test.rs
│   └── database_test.rs
├── unit/                 # Unit tests
│   ├── parser_test.rs
│   └── validator_test.rs
└── fixtures/             # Test data
    ├── input.json
    └── expected.json
```

### Test Coverage Goals

- **Minimum**: 70% code coverage
- **Target**: 80%+ code coverage
- **Critical paths**: 100% coverage
- **New code**: Must include tests

### Test Naming

```rust
// Rust
#[test]
fn test_parses_valid_input() { }

#[test]
fn test_returns_error_on_invalid_input() { }

#[test]
fn test_handles_empty_input() { }
```

```python
# Python
def test_parses_valid_input():
    pass

def test_returns_error_on_invalid_input():
    pass

def test_handles_empty_input():
    pass
```

**Naming Pattern**: `test_<action>_<condition>`

---

## Version Numbering

### Semantic Versioning (Required)

**Format**: `MAJOR.MINOR.PATCH` (e.g., `1.2.3`)

- **MAJOR**: Breaking changes (incompatible API)
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

**Pre-release versions**:
- `1.0.0-alpha.1` - Alpha release
- `1.0.0-beta.2` - Beta release
- `1.0.0-rc.1` - Release candidate

**Examples**:
```
0.1.0  # Initial development
1.0.0  # First stable release
1.1.0  # New feature added
1.1.1  # Bug fix
2.0.0  # Breaking change
```

---

## License Requirements

**All repositories MUST include a LICENSE file.**

**Recommended**: MIT License (permissive, widely used)

```
MIT License

Copyright (c) 2024 Raibid Labs

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**Alternative**: Apache 2.0 (for patent protection)

---

## CI/CD Standards

### GitHub Actions Workflow (Required)

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:

jobs:
  test:
    name: Test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup environment
        run: |
          # Setup commands

      - name: Run tests
        run: just test

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  lint:
    name: Lint
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run linters
        run: just lint

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Dependency audit
        run: just audit

      - name: Container scan
        run: trivy image ...
```

---

## References

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
