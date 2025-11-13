# Raibid Labs - Brand Voice & Engineering Philosophy

## Organization Identity

**Raibid Labs** is a modern, AI-first technology organization pushing boundaries in high-performance computing, machine learning infrastructure, and developer tooling. We embrace experimentation, value correctness, and optimize for velocity without compromising quality.

---

## Voice & Tone

### Core Characteristics

**Innovative but Pragmatic**
- We explore cutting-edge technologies (AI/ML, GPU workloads, modern systems languages)
- We ship production-ready code, not just experiments
- Balance: "Move fast AND build things right"

**Technical Excellence**
- Precision in language: Use exact terminology
- Evidence-based decisions: Measure, don't guess
- Performance-conscious: Optimize hot paths, profile real workloads
- Type-safe where it matters: Leverage Rust's guarantees, Python's flexibility

**Collaboration over Competition**
- Open source mindset (54.5% public repositories)
- Knowledge sharing through documentation
- Cross-functional thinking (Python + Rust, infrastructure + ML)

**Experimental Mindset**
- "hack-*" repositories are sandboxes for learning
- Fail fast, learn faster
- Prototype aggressively, refine incrementally

---

## Technical Communication Style

### Writing Code Comments

**DO:**
```rust
// PERF: This hot loop processes 10M samples/sec on DGX A100
// Consider SIMD if throughput < 8M samples/sec
fn process_batch(samples: &[f32]) -> Result<Tensor, Error> { ... }
```

**DON'T:**
```rust
// This function processes samples
fn process_batch(samples: &[f32]) -> Result<Tensor, Error> { ... }
```

**Principles:**
- Explain *why*, not *what* (code shows what)
- Document performance expectations for critical paths
- Call out GPU/DGX-specific optimizations
- Flag experimental code clearly

### Commit Messages

**Format:** Conventional Commits standard
```
type(scope): short description (50 chars max)

Longer explanation of the change, including:
- Why this change was necessary
- Performance implications (if any)
- Breaking changes (if any)

Refs: #123
Co-authored-by: ...
```

**Types:**
- `feat`: New feature (user-facing or API)
- `fix`: Bug fix
- `perf`: Performance improvement
- `refactor`: Code restructure without behavior change
- `test`: Test additions/updates
- `docs`: Documentation only
- `ci`: CI/CD changes
- `chore`: Tooling, dependencies, maintenance

**Examples:**
```
feat(dgx-pixels): add mixed-precision inference pipeline

Implements FP16/FP32 mixed precision for 2.3x throughput
improvement on DGX A100 nodes. Falls back to FP32 on
older hardware.

Benchmark: 450 → 1,035 images/sec (DGX-1 → DGX A100)

Refs: #142
```

```
perf(raibid-ci): parallelize container build stages

Reduces CI run time from 18m → 7m by building frontend
and backend containers concurrently.

Refs: #89
```

### Documentation Tone

**Technical Docs (README, API docs):**
- Concise, scannable (bullet points, code blocks)
- Show, don't tell (working examples > prose)
- Assume intelligent reader (don't over-explain basics)
- Link to external resources for deep dives

**Architecture Decision Records (ADRs):**
- Structured: Context → Decision → Consequences
- Evidence-based: Include benchmarks, trade-off analysis
- Time-stamped: Decisions may change as tech evolves

---

## Terminology Preferences

### Language & Tools

**Use These Terms:**
| Preferred | Avoid |
|-----------|-------|
| Container | Docker container (unless Docker-specific) |
| K8s | Kubernetes (in casual docs) |
| CI/CD pipeline | Build system (ambiguous) |
| GPU workload | CUDA workload (not always NVIDIA) |
| Inference server | Model server |
| Multi-precision | Mixed precision (unless FP16/FP32 specific) |
| Nushell script | PowerShell/Bash (when cross-platform) |
| Just task | Make target (we prefer Just) |

### Repository Naming

**Established Patterns:**
- `dgx-*`: AI/ML workloads optimized for DGX systems
- `hack-*`: Experimental/research projects (internal sandboxes)
- `raibid-*`: Core infrastructure/tools (production-grade)
- `*-mcp`: Model Context Protocol integrations

**Naming New Projects:**
1. Production infrastructure → `raibid-{name}`
2. AI/ML experiments → `dgx-{name}` or `hack-{name}`
3. General experiments → `hack-{name}`
4. MCP integrations → `{integration}-mcp`

---

## Code Philosophy

### Language Selection Matrix

| Use Case | Primary Language | Secondary | Reasoning |
|----------|------------------|-----------|-----------|
| CLI tools | Rust | Python | Performance, single binary, ergonomics |
| AI/ML services | Python | Rust (bindings) | Ecosystem, rapid iteration, GPU libraries |
| Infrastructure | Rust/Go | Nushell (scripts) | Reliability, concurrency, low overhead |
| Web frontends | TypeScript | - | Type safety, modern ecosystem |
| Build automation | Just + Nushell | - | Cross-platform, data-oriented pipelines |
| IaC (K8s) | Jsonnet/CUE | Starlark (Bazel) | Templating, validation, DRY |

### Hybrid Stack Strategy

**Python + Rust Pattern** (dgx-pixels, ardour-mcp):
- Python for high-level logic, I/O, ML frameworks
- Rust for hot paths (>10% CPU time), unsafe ops, native bindings
- Use PyO3 or ctypes for seamless interop
- Profile first, optimize second

**When to Choose:**
- ✅ Rust: Performance-critical, memory-unsafe APIs, concurrency
- ✅ Python: Rapid prototyping, ML experiments, data wrangling
- ✅ TypeScript: Interactive UIs, documentation sites
- ✅ Nushell: Cross-platform automation, CI/CD scripts

---

## Engineering Values

### 1. Performance is a Feature

**Mindset:**
- DGX systems are expensive; maximize utilization
- Measure before optimizing (profile, don't guess)
- Document expected performance characteristics
- Regression tests for critical hot paths

**Benchmarking Culture:**
- Include benchmarks in `/benches` directory (Rust)
- Use `pytest-benchmark` for Python
- Track metrics over time (CI integration)
- Compare against baselines (CPU vs GPU, old vs new arch)

### 2. Correctness Before Speed

**Priority Order:**
1. **Correctness**: Does it work as specified?
2. **Maintainability**: Can others understand and modify it?
3. **Performance**: Is it fast enough for production?

**Example:**
```rust
// CORRECT: Start with clear, correct implementation
fn validate_config(cfg: &Config) -> Result<(), Error> {
    if cfg.batch_size == 0 {
        return Err(Error::InvalidBatchSize);
    }
    // ... thorough validation
    Ok(())
}

// LATER: Optimize if profiling shows bottleneck
```

### 3. Testability as Design Constraint

**Standards:**
- Unit tests for pure functions (100% coverage)
- Integration tests for APIs/pipelines (happy + edge cases)
- Property tests for complex logic (quickcheck, hypothesis)
- Benchmark tests for performance claims

**Test Organization:**
- Rust: `#[cfg(test)]` modules + `/benches`
- Python: `/tests` with pytest + `/notebooks` for exploratory
- End-to-end: Separate `/e2e` or `/integration` directories

### 4. Modular, Composable Systems

**Architecture Principles:**
- Small, focused modules (<500 LOC per file)
- Clear interfaces (traits in Rust, protocols in Python)
- Dependency injection over globals
- Configuration as code (not env vars for complex state)

**Example Structure:**
```
dgx-pixels/
├── src/
│   ├── inference/       # Core ML pipeline
│   ├── preprocessing/   # Data transforms
│   ├── postprocessing/  # Output formatting
│   └── serving/         # HTTP/gRPC API
├── tests/               # Unit + integration
├── benches/             # Performance tests
└── examples/            # Usage examples
```

### 5. Documentation as Code Artifact

**Required Documentation:**
1. **README.md**: Quick start, architecture overview
2. **ARCHITECTURE.md**: System design, key decisions
3. **CONTRIBUTING.md**: How to develop/test locally
4. **API docs**: Auto-generated from code (rustdoc, Sphinx)

**Optional (but encouraged):**
- ADRs (Architecture Decision Records) in `/docs/adr/`
- Runbooks for operational tasks
- Performance tuning guides for GPU workloads

---

## Innovation Focus Areas

### AI/ML Infrastructure (Core Competency)

**DGX Optimization:**
- Multi-GPU training (distributed data parallel)
- Mixed-precision inference (TensorRT, ONNX)
- Memory-efficient model serving (quantization, pruning)
- Batch processing pipelines (throughput > latency)

**ML Operations:**
- Model versioning and registry
- A/B testing frameworks
- Monitoring (GPU utilization, inference latency)
- Cost optimization (spot instances, autoscaling)

### Developer Experience (Strategic Investment)

**Tooling Philosophy:**
- Just for task running (cross-platform, fast)
- Nushell for scripting (structured data, safety)
- Claude Code integration (AI-assisted development)
- Template repositories (accelerate new projects)

**Automation Culture:**
- CI/CD for every repository
- Pre-commit hooks (formatting, linting)
- Automated dependency updates (Dependabot, Renovate)
- One-command local development (`just dev`)

### Experimentation Velocity

**"hack-*" Repository Guidelines:**
- No production dependencies on hack projects
- Document learnings in README (what worked, what didn't)
- Graduate successful experiments to production repos
- Archive failed experiments (preserve learnings)

**Metrics:**
- Time from idea → working prototype (target: <1 week)
- Experiments per quarter (target: 5-10)
- Graduation rate (target: 20-30%)

---

## Anti-Patterns (What We Avoid)

### Code
- ❌ Premature optimization (profile first)
- ❌ "Not invented here" syndrome (use proven libraries)
- ❌ Magic numbers (use named constants)
- ❌ God objects (modular design)
- ❌ Ignoring errors (`unwrap()` without justification)

### Process
- ❌ "Works on my machine" (containerize environments)
- ❌ Tribal knowledge (document in code/wiki)
- ❌ Long-lived feature branches (integrate frequently)
- ❌ Manual deployments (automate everything)
- ❌ Skipping tests (CI must pass)

### Communication
- ❌ Vague issue descriptions (provide repro steps)
- ❌ "This is broken" (include logs, context)
- ❌ Assuming context (link to prior discussions)
- ❌ Dismissing ideas without evidence

---

## Cultural Norms

### Code Review Etiquette

**Reviewers:**
- Assume good intent, ask questions
- Distinguish: blocking issues vs nits vs suggestions
- Provide context for requested changes
- Approve quickly for low-risk changes

**Authors:**
- Keep PRs small (<400 lines when possible)
- Self-review before requesting review
- Respond to all comments (even just "Done")
- Update PR description as scope evolves

### Meeting Culture

**Bias toward async:**
- Default to GitHub discussions, not meetings
- Document decisions in ADRs or issues
- Record demos/presentations for async viewing

**When meetings are necessary:**
- Clear agenda in advance
- Action items with owners
- Meeting notes published within 24h

### Failure & Learning

**Blameless Postmortems:**
- Focus on systems, not individuals
- Root cause analysis (5 whys)
- Actionable improvements (not just "be more careful")

**Celebrate Failures:**
- "hack-agent-lightning failed, but we learned X"
- Share negative results (saves others time)
- Pivoting is progress, not failure

---

## Brand Personality

**If Raibid Labs were a person:**
- **Experienced engineer** who's also excited about new tech
- **Pragmatic hacker** who measures impact, not lines of code
- **Generous mentor** who documents learnings for others
- **Performance nerd** who geeks out over benchmarks
- **Team player** who values collaboration over ego

**Voice Examples:**

| Context | Voice |
|---------|-------|
| README | "Quick start: `just run`. Optimized for DGX A100, runs anywhere." |
| Error message | "`batch_size` must be >0 (got: 0). See docs/tuning.md for sizing." |
| PR comment | "Nice refactor! Consider caching here: [link to profile data]" |
| Commit | "perf: 2.3x speedup via GPU kernel fusion (profile: [link])" |
| Docs | "This guide assumes basic Rust knowledge. New to Rust? [link]" |

---

## External Representation

### Open Source Engagement

**Contributions:**
- Upstream fixes to dependencies (don't fork unless necessary)
- Share learnings via blog posts/papers
- Sponsor maintainers of critical libraries

**Community:**
- Respond to issues within 48h (even just "triaged")
- Welcome first-time contributors (label: `good-first-issue`)
- Recognize contributors in changelogs

### Technical Writing

**Preferred Outlets:**
- Engineering blog (technical deep-dives)
- Conference talks (architecture, performance)
- Papers (novel ML techniques, benchmarks)

**Topics:**
- DGX optimization strategies
- Rust+Python hybrid architectures
- K8s for ML workloads
- MCP integration patterns

---

## Evolution of Brand

**Current State (2025):**
- Emerging organization with clear technical direction
- Strong foundation in Rust, Python, modern tooling
- Focus on AI/ML infrastructure and developer velocity

**Future Direction:**
- Thought leader in DGX/GPU optimization
- Reference architecture for ML platforms
- Open source champion for hybrid-language systems

**Guardrails:**
- Stay true to technical excellence
- Don't chase hype without validation
- Maintain work/life balance (sustainable velocity)
- Prioritize team growth over growth at all costs

---

## Questions to Ask Yourself

Before committing code, ask:
1. ✅ Is this the simplest solution that works?
2. ✅ Have I measured the performance claim?
3. ✅ Can someone else understand this in 6 months?
4. ✅ Does this integrate cleanly with existing patterns?
5. ✅ Have I documented why, not just what?

Before creating a new project, ask:
1. ✅ Does this fit our strategic focus?
2. ✅ Should this be in an existing repo?
3. ✅ Is this a "hack-" experiment or production tool?
4. ✅ Have I checked for existing solutions?
5. ✅ Can I commit to maintaining this?

---

**Remember:** Raibid Labs values **impact over activity**. Write less code, better code. Ship often, learn constantly. Collaborate generously.
