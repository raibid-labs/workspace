# Raibid Labs - Organization Context & Technical Overview

## Organization Overview

**Raibid Labs** is a modern technology organization focused on high-performance AI/ML infrastructure, developer tooling, and experimental research. We operate at the intersection of cutting-edge hardware (DGX systems), modern systems programming (Rust), and machine learning workloads (Python).

**Core Values:**
- **Experimentation-first**: Rapid prototyping in "hack-*" repositories
- **Performance-conscious**: Optimize for DGX/GPU workloads
- **Open by default**: 54.5% public repositories, open source mindset
- **Modern tooling**: Just, Nushell, containerization, K8s-native

**Scale (as of 2025-11-13):**
- 22 active repositories (excludes 6 forks, 8 newly created)
- 14 repositories with significant code
- 4 primary languages: Rust, Python, TypeScript, Shell/Nushell
- 3 major focus areas: AI/ML, Infrastructure, Developer Tools

---

## Technology Stack Summary

### Primary Languages by Use Case

| Language | Repos | Primary Use Cases | Key Libraries/Frameworks |
|----------|-------|-------------------|--------------------------|
| **Rust** | 4 | Infrastructure, CLI tools, performance-critical | tokio, axum, serde, clap, PyO3 |
| **Python** | 4 | AI/ML, data processing, rapid prototyping | PyTorch, NumPy, FastAPI, pytest |
| **TypeScript** | 2 | Web frontends, documentation sites | React, Docusaurus/VitePress |
| **Nushell** | 10 | Cross-platform scripting, automation | Built-in data pipelines |

### Supporting Technologies (Ubiquitous)

**Build & Automation:**
- **Just** (36.4% of repos): Task runner, replacement for Make
- **Nushell** (45.5% of repos): Cross-platform shell with structured data
- **Docker** (18.2% of repos): Containerization
- **GitHub Actions**: CI/CD automation

**Infrastructure:**
- **Kubernetes**: Container orchestration (IaC via Jsonnet/Starlark)
- **Jsonnet/CUE**: Configuration templating for K8s
- **Starlark**: Bazel build configuration

**ML/AI:**
- **PyTorch**: Deep learning framework
- **ONNX/TensorRT**: Model optimization and inference
- **DGX hardware**: NVIDIA GPU clusters (A100, Spark)

---

## Repository Categorization

### Active Production Repositories (9)

| Repository | Type | Stack | Purpose | Status |
|------------|------|-------|---------|--------|
| **grimware** | Library/Service | Rust, Kotlin, HTML | Multi-language project, mobile support | Active |
| **docs** | Documentation | TypeScript, SCSS | Organization documentation site | Active |
| **dgx-pixels** | AI/ML Service | Python, Rust | DGX pixel processing/generation | Active |
| **dgx-music** | AI/ML Service | Python | DGX music processing/generation | Active |
| **raibid-ci** | Infrastructure | Rust, Nushell | CI/CD platform | Active |
| **mop** | Infrastructure | Jsonnet, Python | Kubernetes IaC | Active |
| **ardour-mcp** | Tool | Python | MCP integration for Ardour DAW | Active |
| **xptui** | Tool/CLI | Shell, Rust, TypeScript | Terminal UI application | Active |
| **dgx-spark** | Infrastructure | Shell, Python | DGX hardware configuration | Active |

### Experimental/Research Repositories (4)

| Repository | Stack | Purpose | Status |
|------------|-------|---------|--------|
| **hack-agent-lightning** | Python | AI agent research (private) | Experimental |
| **hack-k8s** | Nushell, Jsonnet | K8s management experiments | Experimental |
| **hack-research** | Rust | Pure Rust research | Experimental |
| **hack-bevy** | Rust, WGSL | Bevy game engine experiments | Experimental |
| **hack** | TypeScript, Python | Full-stack prototyping | Experimental |

### Newly Initialized Repositories (8)

Pending architecture/implementation:
- **raibid-labs-mcp**: MCP server development
- **workspace**: Organization meta-repository
- **hack-browser**: Browser-related tooling
- **sparky**: Purpose TBD
- **raibid-cli**: CLI tool
- **osai**: AI service
- **skunkworks**: Private experiments
- **agents**: AI agent development

---

## Common Patterns Across Repositories

### 1. Naming Conventions

**Established Patterns:**
- `dgx-*`: DGX-optimized AI/ML workloads (dgx-pixels, dgx-music, dgx-spark)
- `hack-*`: Experimental/research projects (low stability, high iteration)
- `raibid-*`: Production infrastructure/tools (high stability, documented APIs)
- `*-mcp`: Model Context Protocol integrations

**Guidelines:**
```
dgx-{workload}     → GPU-accelerated ML service
hack-{tech}        → Experimental project exploring {tech}
raibid-{tool}      → Production-grade tool/infrastructure
{integration}-mcp  → MCP server for {integration}
```

### 2. Repository Structure

**Standard Directory Layout:**
```
{repo}/
├── src/               # Source code
├── tests/             # Unit + integration tests
├── benches/           # Performance benchmarks (Rust)
├── docs/              # Extended documentation
├── examples/          # Usage examples
├── scripts/           # Utility scripts (Nushell preferred)
├── Justfile           # Task definitions (build, test, deploy)
├── Dockerfile         # Container image
├── .github/
│   └── workflows/     # CI/CD pipelines
├── README.md          # Quick start, architecture
├── CONTRIBUTING.md    # Development guide
└── ARCHITECTURE.md    # System design (for complex projects)
```

**Rust Projects:**
```
{repo}/
├── Cargo.toml         # Package manifest
├── Cargo.lock         # Dependency lock (committed)
├── src/
│   ├── main.rs        # Binary entry point
│   ├── lib.rs         # Library root (if library)
│   └── {modules}/     # Module structure
├── tests/             # Integration tests
└── benches/           # Criterion benchmarks
```

**Python Projects:**
```
{repo}/
├── pyproject.toml     # Poetry/uv config
├── src/{package}/     # Source code
├── tests/             # Pytest tests
├── notebooks/         # Jupyter notebooks (exploratory)
└── requirements.txt   # Pinned dependencies (or use poetry.lock)
```

### 3. Build Tool Standardization

**Justfile Tasks (Common):**
```just
# Standard task names across all repos
default:
    @just --list

# Development
dev:
    # Start development server/environment

build:
    # Build artifacts (cargo build, npm build, etc.)

test:
    # Run test suite

lint:
    # Run linters (clippy, ruff, eslint)

format:
    # Format code (rustfmt, black, prettier)

# CI/CD
ci: lint test build
    # Run all CI checks

# Deployment
deploy:
    # Deploy to staging/production

# Cleanup
clean:
    # Remove build artifacts
```

**Nushell Scripts (Automation):**
- Cross-platform compatibility (Windows, macOS, Linux)
- Structured data pipelines (JSON, CSV, tables)
- Error handling with `try`/`catch`
- Integration with Just tasks

### 4. Multi-Language Projects

**Python + Rust Pattern** (4 repos):
```
Performance-critical path:
  Python (high-level API, ML framework integration)
    ↓ calls
  Rust (compute-intensive operations, unsafe FFI)
    ↓ returns
  Python (result processing, I/O)

Implementation:
- Use PyO3 for Rust bindings
- Python handles: I/O, ML frameworks (PyTorch), orchestration
- Rust handles: Hot loops, memory-unsafe APIs, concurrency
```

**Example: dgx-pixels**
```python
# Python: High-level API
def process_images(images: List[np.ndarray]) -> List[np.ndarray]:
    # Preprocessing in Python (NumPy)
    preprocessed = [preprocess(img) for img in images]

    # Hot path in Rust (via PyO3)
    results = rust_process_batch(preprocessed)

    # Postprocessing in Python
    return [postprocess(res) for res in results]
```

### 5. Infrastructure as Code (IaC) Stack

**Kubernetes-Native Architecture:**
```
Configuration:
  Jsonnet/CUE templates
    ↓ generates
  YAML manifests
    ↓ applied via
  kubectl/Tanka
    ↓ deploys to
  K8s cluster
```

**Key Repositories:**
- **mop**: Jsonnet-based K8s configs (likely using Tanka)
- **hack-k8s**: Nushell-based K8s management scripts
- **raibid-ci**: CI/CD with K8s integration

**Common Tools:**
- **Jsonnet**: DRY K8s configuration (primary)
- **Starlark**: Bazel build rules (secondary)
- **Tanka**: Jsonnet-to-K8s deployment tool
- **Nushell scripts**: K8s cluster management (logs, rollouts)

### 6. DGX/GPU Workload Optimization

**DGX Repository Pattern:**
```
dgx-{workload}/
├── src/
│   ├── inference/       # Model inference pipeline
│   ├── training/        # Distributed training (if applicable)
│   └── serving/         # HTTP/gRPC API
├── models/              # Model weights (large files, LFS)
├── configs/
│   ├── fp16.yaml        # Mixed-precision config
│   └── multi_gpu.yaml   # Multi-GPU setup
├── benchmarks/          # Performance metrics
└── k8s/                 # K8s manifests (GPU resources)
```

**Performance Optimization Checklist:**
- [ ] Mixed-precision inference (FP16/FP32)
- [ ] Batch processing (maximize GPU utilization)
- [ ] Multi-GPU scaling (DistributedDataParallel)
- [ ] Memory-efficient pipelines (gradient checkpointing)
- [ ] TensorRT/ONNX optimization (if inference-heavy)
- [ ] Fallback to CPU (graceful degradation)

**Example: dgx-pixels Architecture**
```
HTTP Request → FastAPI
                 ↓
            Batch accumulator (32-64 images)
                 ↓
            GPU inference (PyTorch + Rust kernels)
                 ↓
            Postprocessing (Python)
                 ↓
            HTTP Response
```

---

## Inter-Repository Relationships

### Dependency Graph

```
┌─────────────────────────────────────────────┐
│         raibid-ci (CI/CD Platform)          │
│  Provides: Build pipelines, container       │
│            registry, deployment automation  │
└──────────────────┬──────────────────────────┘
                   │ uses
        ┌──────────┴──────────┐
        ↓                     ↓
┌───────────────┐    ┌────────────────┐
│ dgx-pixels    │    │ grimware       │
│ (ML Service)  │    │ (Rust Library) │
└───────┬───────┘    └────────┬───────┘
        │                     │
        │ depends on          │ uses
        ↓                     ↓
┌─────────────────────────────────────┐
│           mop (K8s IaC)             │
│  Provides: K8s manifests, configs   │
└─────────────────────────────────────┘
```

**Key Relationships:**

1. **raibid-ci → All Repos**
   - Provides CI/CD pipelines
   - Container image building
   - Deployment automation

2. **mop → Service Repos**
   - K8s manifests for services
   - Configuration management
   - Infrastructure definitions

3. **grimware → Other Rust Projects**
   - Shared Rust libraries (potentially)
   - Common patterns/utilities

4. **docs → All Repos**
   - Central documentation hub
   - API documentation aggregation
   - Architecture decision records

5. **{service}-mcp → External Systems**
   - ardour-mcp → Ardour DAW
   - raibid-labs-mcp → (TBD integrations)

### Shared Configuration

**Organization-Wide Standards:**
```
.github/
├── workflows/           # Reusable GitHub Actions
│   ├── rust-ci.yml      # Rust project CI template
│   ├── python-ci.yml    # Python project CI template
│   └── docker-build.yml # Container build template
└── CODEOWNERS           # Automatic reviewer assignment

.claude/
├── project.json         # Claude Code configuration
└── prompts/             # Organization-wide prompts
    ├── branding.md
    ├── review-checklist.md
    └── context.md

.pre-commit-config.yaml  # Pre-commit hooks (format, lint)
```

---

## Development Workflow

### Typical Feature Development Flow

```
1. Create issue in GitHub
   ↓
2. Branch from main (feat/*, fix/*, refactor/*)
   ↓
3. Implement with TDD
   - Write test (red)
   - Implement (green)
   - Refactor
   ↓
4. Local validation
   $ just lint test build
   ↓
5. Commit with Conventional Commits
   feat(scope): description
   ↓
6. Push and create PR
   ↓
7. CI/CD runs (raibid-ci)
   - Lint, test, build
   - Security scan
   - Performance benchmarks (if applicable)
   ↓
8. Code review (2 reviewers for large changes)
   ↓
9. Merge to main (squash or merge commit)
   ↓
10. Auto-deploy to staging (raibid-ci)
    ↓
11. Manual promotion to production
```

### Local Development Setup

**Prerequisites:**
```bash
# Install core tools
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh  # Rust
curl -sSf https://rye.astral.sh/get | bash                     # Python (uv/rye)
npm install -g pnpm                                              # Node.js
curl -LO https://github.com/casey/just/releases/download/...   # Just
cargo install nu                                                 # Nushell

# Clone organization repos
gh repo clone raibid-labs/{repo}

# Setup repo
cd {repo}
just setup    # Initialize environment (virtual env, deps, etc.)
just dev      # Start development server
```

**Environment Variables:**
```bash
# .env (never committed)
DGX_API_KEY=...
K8S_CONTEXT=staging
RUST_LOG=info
```

### Testing Strategy

**Test Pyramid:**
```
        /\
       /  \  E2E (5-10%)
      /────\
     / Inte \  Integration (20-30%)
    /─  gra ─\
   /   tion   \
  /────────────\
 /   Unit Tests \  Unit (60-80%)
/_________________\
```

**Test Organization:**
- **Unit tests**: In `src/` modules (`#[cfg(test)]` in Rust, `/tests` in Python)
- **Integration tests**: `/tests/integration/`
- **E2E tests**: `/tests/e2e/` (separate from unit/integration)
- **Benchmarks**: `/benches/` (Rust), `/benchmarks/` (Python)

**Running Tests:**
```bash
# All tests
just test

# Specific test types
cargo test --lib          # Unit tests (Rust)
cargo test --test '*'     # Integration tests (Rust)
pytest tests/unit         # Unit tests (Python)
pytest tests/integration  # Integration tests (Python)

# With coverage
cargo tarpaulin --out Html  # Rust
pytest --cov=src --cov-report=html  # Python
```

---

## Key Technologies Deep Dive

### Rust Ecosystem

**Standard Libraries:**
- **tokio**: Async runtime (preferred over async-std)
- **serde**: Serialization (JSON, YAML, MessagePack)
- **clap**: CLI argument parsing (derive API)
- **anyhow/thiserror**: Error handling
- **tracing**: Structured logging

**Web Services:**
- **axum**: Web framework (preferred over actix-web)
- **tower**: Middleware (rate limiting, auth)
- **reqwest**: HTTP client

**Performance:**
- **rayon**: Data parallelism
- **crossbeam**: Lock-free concurrency
- **parking_lot**: Faster mutexes

**Python Interop:**
- **PyO3**: Rust bindings for Python (dgx-pixels, ardour-mcp)

### Python Ecosystem

**Core Libraries:**
- **PyTorch**: Deep learning framework
- **NumPy/Pandas**: Data manipulation
- **FastAPI**: Async web framework
- **pydantic**: Data validation

**ML Tooling:**
- **transformers**: Hugging Face models
- **ONNX**: Model optimization
- **tensorrt**: NVIDIA GPU optimization

**Testing:**
- **pytest**: Test framework
- **hypothesis**: Property-based testing
- **pytest-benchmark**: Performance testing

**Dev Tools:**
- **ruff**: Fast linter/formatter (replaces black, flake8, isort)
- **mypy**: Static type checker
- **poetry/uv**: Dependency management

### Nushell Scripting

**Why Nushell?**
- Cross-platform (Windows, macOS, Linux)
- Structured data (JSON, CSV, tables)
- Type-safe pipelines
- Better error handling than Bash

**Common Patterns:**
```nushell
# Parse JSON API response
http get https://api.example.com/data
  | from json
  | where status == "active"
  | select name, count
  | sort-by count --reverse
  | to csv

# K8s pod monitoring
kubectl get pods --output json
  | from json
  | get items
  | where status.phase == "Running"
  | select metadata.name status.containerStatuses.restartCount
```

**Integration with Just:**
```just
# Justfile
deploy:
    nu scripts/deploy.nu --env production

logs pod:
    nu scripts/k8s-logs.nu --pod {{pod}} --tail 100
```

### Kubernetes (K8s) Patterns

**IaC Workflow:**
```bash
# Development (mop or hack-k8s)
cd k8s/
tk show environments/staging     # Preview changes (Tanka + Jsonnet)
tk apply environments/staging    # Apply to cluster
```

**Common Manifests:**
```yaml
# GPU workload (dgx-pixels)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dgx-pixels
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: inference
        image: raibid/dgx-pixels:v1.2.0
        resources:
          limits:
            nvidia.com/gpu: 1  # Request 1 GPU
            memory: 16Gi
          requests:
            nvidia.com/gpu: 1
            memory: 8Gi
        env:
        - name: CUDA_VISIBLE_DEVICES
          value: "0"
```

**Service Mesh (if used):**
- Istio or Linkerd for traffic management
- Distributed tracing (Jaeger)
- Service-to-service auth (mTLS)

---

## MCP (Model Context Protocol) Integration Strategy

### What is MCP?

MCP (Model Context Protocol) enables AI models (like Claude) to interact with external tools and data sources through standardized servers.

**Raibid Labs MCP Strategy:**
```
Claude Code
    ↓ (MCP protocol)
ardour-mcp server → Ardour DAW
    ↓
raibid-labs-mcp server → (TBD integrations)
    ↓
{future}-mcp servers → Other tools
```

### MCP Server Architecture

**Standard MCP Server Structure:**
```
{integration}-mcp/
├── src/
│   ├── __init__.py
│   ├── server.py        # MCP server implementation
│   ├── tools.py         # Tool definitions
│   └── handlers.py      # Tool execution logic
├── tests/
├── examples/
└── README.md
```

**Example: ardour-mcp**
```python
# src/server.py
from mcp.server import Server

server = Server("ardour-mcp")

@server.tool()
def export_audio(session: str, format: str = "wav") -> str:
    """Export Ardour session to audio file."""
    # Integration with Ardour API
    return f"Exported {session}.{format}"

if __name__ == "__main__":
    server.run()
```

**Usage from Claude Code:**
```python
# Claude Code can now call:
result = call_tool("ardour-mcp", "export_audio", {
    "session": "my-project",
    "format": "flac"
})
```

### Future MCP Integrations

**Planned (based on empty repos):**
- **raibid-labs-mcp**: Organization-wide tools
  - Repository management
  - CI/CD pipeline control
  - Infrastructure provisioning
- **osai-mcp**: AI service integration
  - Model inference endpoints
  - Training job management
  - Dataset operations

---

## Performance & Benchmarking Culture

### Performance Expectations

**Service Latency Targets:**
| Service Type | P50 | P95 | P99 |
|--------------|-----|-----|-----|
| API Gateway | <50ms | <100ms | <200ms |
| ML Inference (GPU) | <100ms | <250ms | <500ms |
| ML Inference (CPU) | <500ms | <1s | <2s |
| Database Query | <10ms | <50ms | <100ms |

**DGX Workload Metrics:**
| Metric | Target | Measurement |
|--------|--------|-------------|
| GPU Utilization | >70% | `nvidia-smi` |
| Throughput (images/sec) | >500 (A100) | Custom benchmark |
| Memory Usage | <80% VRAM | `nvidia-smi` |
| Multi-GPU Scaling | >0.9x linear | Distributed benchmark |

### Benchmarking Workflow

**1. Define Baseline:**
```bash
# Rust
cargo bench --bench inference_pipeline > baseline.txt

# Python
pytest benchmarks/ --benchmark-save=baseline
```

**2. Make Changes**

**3. Compare Results:**
```bash
# Rust
cargo bench --bench inference_pipeline > optimized.txt
critcmp baseline.txt optimized.txt

# Python
pytest benchmarks/ --benchmark-compare=baseline
```

**4. Document in PR:**
```markdown
## Performance Impact

**Benchmark:** `inference_pipeline` (DGX A100, batch_size=32)

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Throughput | 450 img/s | 1,035 img/s | +130% |
| Latency (P95) | 180ms | 75ms | -58% |
| GPU Util | 62% | 89% | +27pp |

**Profiling:** [flamegraph link]
```

---

## Security & Secrets Management

### Secrets Storage

**Development:**
```bash
# .env (gitignored)
DATABASE_URL=postgresql://localhost/dev
API_KEY=dev_key_12345
```

**Production:**
```yaml
# K8s ExternalSecrets (mop repo)
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: dgx-pixels-secrets
spec:
  secretStoreRef:
    name: aws-secrets-manager
  target:
    name: dgx-pixels-env
  data:
  - secretKey: API_KEY
    remoteRef:
      key: prod/dgx-pixels/api-key
```

**Never:**
- ❌ Commit `.env` files
- ❌ Hardcode secrets in code
- ❌ Log secrets (even in debug logs)
- ❌ Include secrets in error messages

### Security Scanning

**CI/CD Pipeline:**
```yaml
# .github/workflows/security.yml
- name: Dependency Audit
  run: |
    cargo audit          # Rust
    pip-audit            # Python
    npm audit            # Node.js

- name: SAST Scan
  run: |
    cargo clippy -- -D warnings
    bandit -r src/       # Python

- name: Container Scan
  run: trivy image raibid/{repo}:latest
```

---

## Documentation Standards

### Required Documentation

**Every Repository:**
1. **README.md**: Quick start, architecture overview (1-2 pages)
2. **CONTRIBUTING.md**: Development guide, testing, PR process
3. **CHANGELOG.md**: User-facing changes (keep-a-changelog format)

**Complex Projects:**
4. **ARCHITECTURE.md**: System design, key decisions (ADRs embedded or separate)
5. **API.md**: API documentation (or auto-generated via Swagger/rustdoc)
6. **DEPLOYMENT.md**: Production deployment guide

### Documentation Site (docs repo)

**Structure:**
```
docs/
├── docs/
│   ├── getting-started/
│   ├── architecture/
│   ├── api-reference/
│   ├── tutorials/
│   └── adr/               # Architecture Decision Records
├── blog/                  # Engineering blog posts
└── docusaurus.config.js   # Site config
```

**ADR Format (RFC 0005 style):**
```markdown
# ADR-001: Use Jsonnet for K8s Configuration

**Status:** Accepted (2025-01-15)
**Deciders:** Infrastructure Team
**Context:** Need DRY K8s manifests, reduce YAML duplication

## Decision
Use Jsonnet + Tanka for K8s IaC (over Helm, Kustomize, CUE)

## Consequences
✅ DRY templates, strong typing
✅ Tanka workflow well-documented
❌ Learning curve for Jsonnet
❌ Smaller ecosystem than Helm

## Alternatives Considered
- Helm: Too verbose, weak typing
- Kustomize: Limited templating
- CUE: Promising but immature
```

---

## Onboarding New Projects

### Checklist for New Repositories

**Setup Phase:**
- [ ] Choose appropriate name (dgx-*, hack-*, raibid-*, *-mcp)
- [ ] Initialize from template (if available)
- [ ] Add to organization documentation
- [ ] Configure branch protection (require PR, CI pass)

**Configuration:**
- [ ] Add Justfile with standard tasks
- [ ] Configure CI/CD (GitHub Actions)
- [ ] Add pre-commit hooks
- [ ] Create .claude/ configuration

**Documentation:**
- [ ] Write README with quick start
- [ ] Document architecture (if non-trivial)
- [ ] Add CONTRIBUTING guide
- [ ] Initialize CHANGELOG

**Integration:**
- [ ] Add to raibid-ci pipelines
- [ ] Create K8s manifests (if service)
- [ ] Link in docs site
- [ ] Announce in team channel

---

## Migration Path for Empty Repositories

**Current State (8 empty repos):**

**High Priority (Define & Implement):**
1. **raibid-labs-mcp**
   - Architecture: Python MCP server
   - Purpose: Organization tool integrations
   - Template: Python MCP template (create)
   - Timeline: 2 weeks

2. **raibid-cli**
   - Architecture: Rust CLI tool
   - Purpose: Organization management CLI
   - Template: Rust CLI template (use grimware patterns)
   - Timeline: 3 weeks

3. **agents**
   - Architecture: Python + Rust (if perf-critical)
   - Purpose: AI agent framework
   - Template: Python ML template
   - Timeline: 4 weeks

4. **osai**
   - Architecture: Python service + K8s
   - Purpose: AI service endpoints
   - Template: Python service template + mop IaC
   - Timeline: 4 weeks

**Medium Priority (Define Purpose First):**
5. **sparky** - Define scope, then architect
6. **hack-browser** - Define browser integration scope
7. **workspace** - Potentially monorepo or meta-repo

**Low Priority (Keep as Sandbox):**
8. **skunkworks** - No formal structure needed

---

## Cross-Repository Best Practices

### Shared Conventions

**Commit Message Format:**
```
type(scope): subject line (50 chars)

Body explaining why (72 chars per line)
- Performance impact
- Breaking changes

Refs: #123
Co-authored-by: Name <email>
```

**Branch Naming:**
```
feat/{issue-number}-{short-description}
fix/{issue-number}-{short-description}
refactor/{description}
chore/{description}
```

**Version Numbering:**
- Semantic Versioning (semver) for libraries
- Date-based for services (YYYY.MM.DD.patch)

**Release Process:**
```bash
# Tag release
git tag -a v1.2.0 -m "Release 1.2.0"
git push origin v1.2.0

# Automated by raibid-ci:
# - Build artifacts
# - Create GitHub release
# - Publish to registries (crates.io, PyPI, npm)
# - Deploy to staging
```

---

## Contact & Support

**Internal Resources:**
- **Documentation:** docs.raibid.io (docs repo)
- **Issue Tracker:** GitHub Issues (per repo)
- **Discussions:** GitHub Discussions (organization-wide)
- **CI/CD Dashboard:** raibid-ci.raibid.io

**External Resources:**
- **GitHub Organization:** https://github.com/raibid-labs
- **Public Repositories:** 12 (54.5% of total)

**Getting Help:**
1. Check docs site (docs repo)
2. Search GitHub Issues (existing solutions)
3. Ask in Discussions (technical questions)
4. File issue (bugs, feature requests)

---

## Continuous Improvement

**This document evolves.** Suggest improvements:
- PRs to `.claude/prompts/context.md`
- Issues tagged `documentation`
- Quarterly review in team retrospectives

**Last Updated:** 2025-11-13
**Next Review:** Quarterly or after major architectural changes

---

## Quick Reference Card

**Getting Started:**
```bash
gh repo clone raibid-labs/{repo}
cd {repo}
just setup
just dev
```

**Common Tasks:**
```bash
just test          # Run tests
just lint          # Run linters
just build         # Build artifacts
just deploy        # Deploy to staging
```

**Getting Help:**
```bash
just --list        # List available tasks
just help {task}   # Get task-specific help
```

**CI/CD Status:**
- Check GitHub Actions tab
- View raibid-ci dashboard
- Monitor K8s deployments: `kubectl get pods`

**Key Repositories:**
- **docs**: Organization documentation
- **raibid-ci**: CI/CD platform
- **mop**: K8s infrastructure
- **dgx-pixels**: ML service example
- **grimware**: Rust library example
