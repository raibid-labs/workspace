# Code Style Guide - Raibid Labs

## Overview
This document defines code style standards across all Raibid Labs repositories, based on observed patterns in production codebases (grimware, raibid-ci, dgx-*, ardour-mcp, docs).

---

## Language-Specific Standards

### Rust

**Formatting**: Use `rustfmt` with default settings
```toml
# rustfmt.toml
edition = "2021"
max_width = 100
tab_spaces = 4
```

**Linting**: Use `clippy` with pedantic warnings
```toml
# Cargo.toml or .clippy.toml
[lints.clippy]
pedantic = "warn"
nursery = "warn"
cargo = "warn"
```

**Conventions**:
- **Naming**:
  - `snake_case` for functions, variables, modules
  - `PascalCase` for types, traits, enums
  - `SCREAMING_SNAKE_CASE` for constants
  - `'a`, `'b` for lifetimes (short, descriptive)

```rust
// ✅ Good
const MAX_BUFFER_SIZE: usize = 1024;

pub struct ConfigManager<'a> {
    config_path: &'a Path,
}

impl<'a> ConfigManager<'a> {
    pub fn load_config(&self) -> Result<Config> {
        // Implementation
    }
}

// ❌ Bad
const maxBufferSize: usize = 1024; // Wrong case
pub struct configManager { } // Wrong case
```

**Error Handling**:
- Use `Result<T, E>` for fallible operations
- Use `anyhow` for application errors, `thiserror` for library errors
- Avoid `.unwrap()` in production code

```rust
// ✅ Good
use anyhow::{Context, Result};

pub fn process_file(path: &Path) -> Result<Data> {
    let content = std::fs::read_to_string(path)
        .context("Failed to read configuration file")?;
    parse_content(&content)
}

// ❌ Bad
pub fn process_file(path: &Path) -> Data {
    let content = std::fs::read_to_string(path).unwrap(); // Will panic
    parse_content(&content).unwrap()
}
```

**Module Organization**:
```
src/
├── lib.rs or main.rs
├── config/
│   ├── mod.rs
│   ├── parser.rs
│   └── validator.rs
├── services/
│   ├── mod.rs
│   └── api.rs
└── utils/
    ├── mod.rs
    └── helpers.rs
```

**Documentation**:
- All public items must have doc comments
- Use `///` for item documentation, `//!` for module documentation
- Include examples for complex functions

```rust
/// Parses a configuration file and validates its contents.
///
/// # Arguments
/// * `path` - Path to the configuration file
///
/// # Errors
/// Returns an error if the file cannot be read or parsed.
///
/// # Examples
/// ```
/// let config = parse_config(Path::new("config.toml"))?;
/// ```
pub fn parse_config(path: &Path) -> Result<Config> {
    // Implementation
}
```

---

### Python

**Formatting**: Use `black` with default settings
```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py311']
```

**Linting**: Use `ruff` (faster) or `pylint` + `mypy`
```toml
# pyproject.toml
[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W", "C90", "UP"]
target-version = "py311"

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
```

**Conventions**:
- **Naming**:
  - `snake_case` for functions, variables, modules
  - `PascalCase` for classes
  - `SCREAMING_SNAKE_CASE` for constants
  - Prefix private with `_`

```python
# ✅ Good
MAX_RETRIES = 3

class DataProcessor:
    def __init__(self, config_path: Path):
        self._config = self._load_config(config_path)

    def _load_config(self, path: Path) -> dict:
        """Private method for loading config."""
        pass

    def process_data(self, data: list[dict]) -> pd.DataFrame:
        """Public API for data processing."""
        pass

# ❌ Bad
maxRetries = 3  # Wrong case
class dataProcessor:  # Wrong case
    def loadConfig(self): pass  # Wrong case, missing type hints
```

**Type Hints**:
- Always use type hints for function signatures
- Use `typing` module for complex types
- Use `|` syntax for unions (Python 3.10+)

```python
from typing import Optional, Union
from pathlib import Path

# ✅ Good
def load_model(
    path: Path,
    device: str = "cuda",
    precision: str | None = None
) -> torch.nn.Module:
    """Load a PyTorch model from disk."""
    pass

# ❌ Bad
def load_model(path, device="cuda"):  # Missing type hints
    pass
```

**Error Handling**:
- Use specific exceptions, not bare `except`
- Log errors appropriately
- Use context managers for resources

```python
import logging

logger = logging.getLogger(__name__)

# ✅ Good
def process_file(path: Path) -> dict:
    try:
        with path.open() as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {path}: {e}")
        raise ValueError(f"Invalid configuration file: {path}") from e

# ❌ Bad
def process_file(path):
    try:
        f = open(path)  # No context manager
        return json.load(f)
    except:  # Bare except
        print("Error!")  # No logging
        return {}  # Silent failure
```

**Module Organization** (DGX/ML Projects):
```
project/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── transformer.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── loader.py
│   └── utils/
│       ├── __init__.py
│       └── metrics.py
├── tests/
├── notebooks/  # Jupyter notebooks for research
└── pyproject.toml
```

**Docstrings**: Use Google or NumPy style
```python
def train_model(
    model: nn.Module,
    data_loader: DataLoader,
    epochs: int = 10
) -> dict[str, float]:
    """Train a PyTorch model on the given dataset.

    Args:
        model: The neural network model to train
        data_loader: DataLoader containing training data
        epochs: Number of training epochs (default: 10)

    Returns:
        Dictionary containing training metrics (loss, accuracy)

    Raises:
        ValueError: If epochs is less than 1
        RuntimeError: If CUDA is unavailable when required

    Example:
        >>> model = MyModel()
        >>> loader = DataLoader(dataset, batch_size=32)
        >>> metrics = train_model(model, loader, epochs=5)
    """
    pass
```

---

### TypeScript

**Formatting**: Use `prettier` with standard config
```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5",
  "tabWidth": 2,
  "printWidth": 100
}
```

**Linting**: Use `eslint` with TypeScript plugin
```json
// .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-requiring-type-checking",
    "prettier"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "project": "./tsconfig.json"
  }
}
```

**Conventions**:
- **Naming**:
  - `camelCase` for functions, variables
  - `PascalCase` for classes, interfaces, types
  - `SCREAMING_SNAKE_CASE` for constants
  - Prefix interfaces with `I` only if needed for disambiguation

```typescript
// ✅ Good
const MAX_RETRY_ATTEMPTS = 3;

interface UserConfig {
  name: string;
  email: string;
}

class ConfigManager {
  private readonly configPath: string;

  constructor(configPath: string) {
    this.configPath = configPath;
  }

  public async loadConfig(): Promise<UserConfig> {
    // Implementation
  }
}

// ❌ Bad
const max_retry_attempts = 3; // Wrong case
interface user_config { } // Wrong case
class config_manager { } // Wrong case
```

**Type Safety**:
- Enable strict mode in `tsconfig.json`
- Avoid `any`, use `unknown` if needed
- Use union types and type guards

```typescript
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true
  }
}

// ✅ Good
type Result<T> = { success: true; data: T } | { success: false; error: string };

function isSuccessResult<T>(result: Result<T>): result is { success: true; data: T } {
  return result.success;
}

async function fetchData(url: string): Promise<Result<Data>> {
  try {
    const response = await fetch(url);
    const data = await response.json() as Data;
    return { success: true, data };
  } catch (error) {
    return { success: false, error: String(error) };
  }
}

// ❌ Bad
async function fetchData(url: string): Promise<any> {  // any is forbidden
  const response = await fetch(url);
  return response.json();  // No error handling
}
```

**Module Organization** (Documentation Sites):
```
src/
├── components/
│   ├── common/
│   │   └── Button.tsx
│   └── layout/
│       └── Header.tsx
├── pages/
│   ├── index.tsx
│   └── docs/
│       └── [slug].tsx
├── styles/
│   └── globals.scss
└── utils/
    └── api.ts
```

---

### Shell/Nushell

**Nushell Preference**: Use Nushell over Bash for new scripts
- Cross-platform compatibility
- Data-oriented pipelines
- Better error handling
- Structured output (tables, JSON)

**Nushell Conventions**:
```nu
#!/usr/bin/env nu

# Configuration management script
# Usage: ./config.nu [command]

def main [] {
  print "Config management tool"
  print "Commands: load, save, validate"
}

# Load configuration from file
def "main load" [
  path: path  # Path to config file
  --format: string = "json"  # Format: json, yaml, toml
] {
  if not ($path | path exists) {
    error make { msg: $"Config file not found: ($path)" }
  }

  open $path | from $format
}

# Save configuration to file
def "main save" [
  config: record  # Configuration to save
  path: path  # Output path
  --format: string = "json"
] {
  $config | to $format | save -f $path
  print $"Config saved to ($path)"
}

# Validate configuration
def "main validate" [config: record] {
  let required = ["name", "version", "type"]

  $required | each { |key|
    if not ($key in $config) {
      error make { msg: $"Missing required key: ($key)" }
    }
  }

  print "✓ Configuration valid"
}
```

**Shell Script Conventions** (when Nushell not possible):
```bash
#!/usr/bin/env bash
set -euo pipefail  # Exit on error, undefined vars, pipe failures
IFS=$'\n\t'        # Safe word splitting

# Script configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly CONFIG_FILE="${SCRIPT_DIR}/config.json"

# Logging function
log() {
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" >&2
}

# Error handler
error() {
  log "ERROR: $*"
  exit 1
}

# Main logic
main() {
  local config_path="${1:-$CONFIG_FILE}"

  if [[ ! -f "$config_path" ]]; then
    error "Config file not found: $config_path"
  fi

  log "Loading config from $config_path"
  # Implementation
}

main "$@"
```

---

### Just (Task Runner)

**Justfile Patterns**:
```just
# Set shell to nushell for cross-platform compatibility
set shell := ["nu", "-c"]

# Default recipe
default:
  @just --list

# Build project
build:
  cargo build --release

# Run tests
test:
  cargo test --all-features

# Lint code
lint:
  cargo clippy -- -D warnings
  cargo fmt --check

# Format code
fmt:
  cargo fmt

# Check everything before commit
check: lint test
  @echo "✓ All checks passed"

# Clean build artifacts
clean:
  cargo clean

# Run with specific profile
run profile="dev":
  cargo run --profile {{profile}}

# Build docker image
docker-build tag="latest":
  docker build -t raibid/service:{{tag}} .

# Deploy to environment
deploy env="staging":
  just docker-build {{env}}
  kubectl apply -f k8s/{{env}}/
```

---

## Multi-Language Projects

**Project Structure** (e.g., grimware pattern):
```
project/
├── rust/           # Rust core library
│   ├── Cargo.toml
│   └── src/
├── python/         # Python bindings/tools
│   ├── pyproject.toml
│   └── src/
├── kotlin/         # Mobile/Android
│   └── app/
├── scripts/        # Automation scripts
│   ├── build.nu
│   └── deploy.nu
├── Justfile        # Unified task runner
├── Dockerfile      # Container definition
└── README.md
```

**Justfile for Multi-Language**:
```just
set shell := ["nu", "-c"]

# Build all components
build-all:
  just build-rust
  just build-python
  just build-kotlin

# Rust component
build-rust:
  cd rust && cargo build --release

# Python component
build-python:
  cd python && poetry build

# Kotlin component
build-kotlin:
  cd kotlin && ./gradlew build

# Test all
test-all:
  just test-rust
  just test-python
  just test-kotlin

# Unified CI check
ci: build-all test-all lint-all
```

---

## Pre-commit Hooks

**Install pre-commit** in all repositories:
```yaml
# .pre-commit-config.yaml
repos:
  # Rust
  - repo: local
    hooks:
      - id: cargo-fmt
        name: cargo fmt
        entry: cargo fmt --check
        language: system
        types: [rust]

      - id: cargo-clippy
        name: cargo clippy
        entry: cargo clippy -- -D warnings
        language: system
        types: [rust]

  # Python
  - repo: https://github.com/psf/black
    rev: 23.12.0
    hooks:
      - id: black

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff

  # TypeScript
  - repo: https://github.com/pre-commit/mirrors-prettier
    rev: v4.0.0-alpha.8
    hooks:
      - id: prettier
        types_or: [javascript, jsx, ts, tsx]

  # Generic
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

---

## Editor Configuration

**EditorConfig** (all projects):
```ini
# .editorconfig
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.{rs,toml}]
indent_style = space
indent_size = 4

[*.{py,nu}]
indent_style = space
indent_size = 4

[*.{js,ts,tsx,jsx,json,yaml,yml}]
indent_style = space
indent_size = 2

[Makefile]
indent_style = tab
```

---

## Code Review Checklist

Before submitting PR, ensure:
- [ ] Code formatted with language-specific formatter
- [ ] Linter passes with no warnings
- [ ] All tests pass
- [ ] New code has tests (aim for 80%+ coverage)
- [ ] Documentation updated
- [ ] No secrets/credentials in code
- [ ] Dependencies are pinned versions
- [ ] Pre-commit hooks pass

---

## References

- Rust: https://doc.rust-lang.org/book/
- Python: https://peps.python.org/pep-0008/
- TypeScript: https://www.typescriptlang.org/docs/handbook/
- Nushell: https://www.nushell.sh/book/
- Just: https://just.systems/man/en/
