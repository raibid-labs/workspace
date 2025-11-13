# Raibid Labs - Code Review Checklist

## Purpose

This checklist ensures consistency, quality, and knowledge sharing across all Raibid Labs repositories. Use this for all pull requests, adjusting depth based on change size and risk.

---

## Review Process Overview

### PR Size Guidelines

| Size | Lines Changed | Expected Review Time | Recommendation |
|------|---------------|---------------------|----------------|
| **XS** | <50 | 5-10 min | Ideal size, fast turnaround |
| **S** | 50-200 | 15-30 min | Good size, manageable scope |
| **M** | 200-400 | 30-60 min | Consider splitting if possible |
| **L** | 400-800 | 1-2 hours | Should be split into smaller PRs |
| **XL** | >800 | >2 hours | ❌ Split into multiple PRs |

**Note:** Large PRs often indicate architectural changes or refactors. Consider RFC/design doc before implementation.

---

## 1. Functional Correctness

### Core Functionality
- [ ] **Does the code solve the stated problem?** (check issue/description)
- [ ] **Are edge cases handled?** (nulls, empty collections, boundary values)
- [ ] **Are error conditions handled gracefully?** (no panics/unwraps in prod code)
- [ ] **Does it match the acceptance criteria?** (from issue/spec)

### Rust-Specific (if applicable)
- [ ] **No `unwrap()` or `expect()` in non-test code** (unless infallible)
  - Use `?` operator or explicit error handling
  - Exception: Initialization code with clear failure modes
- [ ] **Proper error types** (use `thiserror` or custom enums, not `String`)
- [ ] **No unnecessary `clone()`** (check for Arc/Rc or borrowing opportunities)
- [ ] **Lifetime annotations correct** (compiler helps, but verify intent)

### Python-Specific (if applicable)
- [ ] **Type hints present** (functions, class attributes)
- [ ] **No bare `except:`** (catch specific exceptions)
- [ ] **Resource cleanup** (use context managers for files, connections)
- [ ] **No global mutable state** (unless explicitly managed)

### TypeScript-Specific (if applicable)
- [ ] **No `any` types** (use `unknown` or proper types)
- [ ] **Null checks** (use optional chaining, nullish coalescing)
- [ ] **Async/await consistency** (don't mix callbacks and promises)

---

## 2. Code Quality

### Readability
- [ ] **Variable/function names are descriptive** (no `tmp`, `data`, `util`)
- [ ] **Functions are focused** (<50 lines, single responsibility)
- [ ] **Complex logic is commented** (explain *why*, not *what*)
- [ ] **No commented-out code** (use git history instead)
- [ ] **Consistent formatting** (rustfmt, black, prettier applied)

### Structure
- [ ] **Appropriate abstraction level** (not too generic, not too specific)
- [ ] **DRY principle followed** (no copy-pasted logic)
- [ ] **Separation of concerns** (UI/logic/data access clearly separated)
- [ ] **No god objects/functions** (refactor if >200 LOC or >10 params)

### Performance
- [ ] **No obvious performance issues** (n² algorithms, unnecessary allocations)
- [ ] **Hot paths optimized** (profiling data included if performance claim)
- [ ] **Database queries efficient** (proper indexes, no N+1 queries)
- [ ] **GPU memory usage considered** (for DGX workloads, check batch sizes)

### Performance Checklist (GPU/DGX Workloads)
- [ ] **Batch size documented** (with GPU memory requirements)
- [ ] **Mixed-precision used** (FP16/FP32 where applicable)
- [ ] **Memory transfers minimized** (CPU↔GPU bandwidth is expensive)
- [ ] **Kernel fusion considered** (for ML pipelines)
- [ ] **Fallback for non-DGX hardware** (graceful degradation)

---

## 3. Testing Requirements

### Test Coverage (Required)
- [ ] **Unit tests present** (for pure functions, business logic)
- [ ] **Integration tests** (for APIs, database interactions)
- [ ] **Edge cases tested** (null, empty, max values, error conditions)
- [ ] **Tests are deterministic** (no flaky tests due to timing/randomness)

### Test Quality
- [ ] **Test names describe behavior** (`test_parse_invalid_json_returns_error`)
- [ ] **No test interdependencies** (can run in any order)
- [ ] **Assertions are specific** (`assert_eq!` not `assert!`)
- [ ] **Test data is minimal** (only what's needed to verify behavior)

### Coverage Thresholds
| Repository Type | Minimum Coverage | Target |
|-----------------|------------------|--------|
| Core libraries | 85% | 95%+ |
| Services/APIs | 75% | 85% |
| Tools/CLI | 70% | 80% |
| Experiments (hack-*) | 50% | N/A |

**Measuring Coverage:**
- Rust: `cargo tarpaulin` or `cargo llvm-cov`
- Python: `pytest --cov`
- TypeScript: `jest --coverage`

### Test Examples

**❌ Bad Test:**
```rust
#[test]
fn test_function() {
    let result = my_function();
    assert!(result.is_ok());  // Too vague
}
```

**✅ Good Test:**
```rust
#[test]
fn parse_valid_config_returns_expected_values() {
    let input = r#"{"batch_size": 32, "learning_rate": 0.001}"#;
    let config = parse_config(input).expect("valid config");

    assert_eq!(config.batch_size, 32);
    assert_eq!(config.learning_rate, 0.001);
}
```

---

## 4. Documentation

### Code Documentation
- [ ] **Public APIs documented** (rustdoc, docstrings, JSDoc)
- [ ] **Complex algorithms explained** (why this approach, trade-offs)
- [ ] **Performance characteristics noted** (O(n), memory usage)
- [ ] **Unsafe code justified** (Rust: why unsafe, invariants maintained)

### Repository Documentation
- [ ] **README updated** (if public API or usage changes)
- [ ] **CHANGELOG updated** (user-facing changes, breaking changes)
- [ ] **Examples updated** (if API signature changes)
- [ ] **Architecture docs updated** (if structure changes)

### API Documentation Standards

**Rust (rustdoc):**
```rust
/// Processes a batch of samples using mixed-precision inference.
///
/// # Arguments
/// * `samples` - Input tensor (shape: [batch_size, channels, height, width])
/// * `precision` - Inference precision mode (FP16/FP32)
///
/// # Returns
/// Processed tensor or error if GPU memory insufficient.
///
/// # Performance
/// ~1000 samples/sec on DGX A100 (FP16), ~450 samples/sec (FP32)
///
/// # Examples
/// ```
/// let samples = Tensor::zeros([32, 3, 224, 224]);
/// let output = process_batch(&samples, Precision::FP16)?;
/// ```
pub fn process_batch(samples: &Tensor, precision: Precision) -> Result<Tensor> { ... }
```

**Python (docstrings):**
```python
def process_batch(samples: torch.Tensor, precision: str = "fp16") -> torch.Tensor:
    """Process a batch using mixed-precision inference.

    Args:
        samples: Input tensor (batch_size, channels, height, width)
        precision: Inference mode ("fp16" or "fp32")

    Returns:
        Processed tensor

    Raises:
        ValueError: If precision not supported
        RuntimeError: If GPU memory insufficient

    Performance:
        ~1000 samples/sec on DGX A100 (fp16)

    Example:
        >>> samples = torch.zeros(32, 3, 224, 224)
        >>> output = process_batch(samples, precision="fp16")
    """
```

---

## 5. Security Considerations

### Secrets Management
- [ ] **No hardcoded secrets** (API keys, passwords, tokens)
- [ ] **Secrets from environment variables** (or secret management service)
- [ ] **No secrets in logs** (redact sensitive data)
- [ ] **`.env` files in `.gitignore`**

### Input Validation
- [ ] **All external inputs validated** (API params, file uploads, CLI args)
- [ ] **SQL injection prevention** (parameterized queries)
- [ ] **Path traversal prevention** (sanitize file paths)
- [ ] **Rate limiting considered** (for public APIs)

### Dependencies
- [ ] **No known vulnerabilities** (run `cargo audit`, `pip-audit`, `npm audit`)
- [ ] **Dependencies justified** (not adding large deps for trivial features)
- [ ] **Versions pinned** (Cargo.lock, requirements.txt, package-lock.json committed)

### Common Vulnerabilities Checklist
- [ ] **Command injection** (no `os.system()` with user input)
- [ ] **Deserialization attacks** (validate before deserializing)
- [ ] **Resource exhaustion** (limits on upload size, request count)
- [ ] **Timing attacks** (constant-time comparison for secrets)

---

## 6. Performance Considerations

### Profiling Requirements (if performance claim made)
- [ ] **Benchmark data included** (before/after, environment specs)
- [ ] **Profiling tool used** (flamegraph, perf, py-spy)
- [ ] **Regression tests added** (benchmark in CI)

### GPU/DGX-Specific Performance
- [ ] **GPU utilization >70%** (for compute-bound workloads)
- [ ] **Memory transfers minimized** (batch operations)
- [ ] **Multi-GPU scaling verified** (if applicable)
- [ ] **Fallback to CPU tested** (for non-GPU environments)

### Optimization Anti-Patterns to Avoid
- [ ] **No premature optimization** (profile first)
- [ ] **No micro-optimizations** (readability > minor perf gains)
- [ ] **No trading correctness for speed** (unless explicitly unsafe)

---

## 7. Integration Checks

### API Compatibility
- [ ] **Backward compatible** (no breaking changes without major version bump)
- [ ] **Deprecation warnings** (for removed features, with migration path)
- [ ] **API versioning** (for HTTP APIs)

### Configuration
- [ ] **Config changes documented** (in README or migration guide)
- [ ] **Defaults are sensible** (safe for most users)
- [ ] **Config validation** (fail fast on invalid config)

### Database Changes (if applicable)
- [ ] **Migration script included** (SQL, Alembic, Diesel)
- [ ] **Reversible migrations** (down script)
- [ ] **Tested on production-like data** (size, indexes)
- [ ] **No data loss** (verified)

### Container/Deployment
- [ ] **Dockerfile optimized** (multi-stage builds, layer caching)
- [ ] **Health checks defined** (for K8s deployments)
- [ ] **Resource limits set** (CPU/memory requests/limits)
- [ ] **Environment-agnostic** (no hardcoded prod URLs)

---

## 8. CI/CD Pipeline

### Automated Checks (must pass)
- [ ] **All tests pass** (`just test` or `cargo test`, `pytest`, `npm test`)
- [ ] **Linting passes** (`cargo clippy`, `ruff`, `eslint`)
- [ ] **Formatting applied** (`cargo fmt`, `black`, `prettier`)
- [ ] **Type checking passes** (Rust, `mypy`, `tsc --noEmit`)
- [ ] **Security scan** (`cargo audit`, `pip-audit`, `npm audit`)

### Build Verification
- [ ] **Clean build succeeds** (no cached artifacts)
- [ ] **Cross-platform build** (if applicable: Linux, macOS, Windows)
- [ ] **Container build succeeds** (if Dockerfile present)

### Performance Benchmarks (if applicable)
- [ ] **Benchmark CI job passes** (no regressions >5%)
- [ ] **Results compared to baseline** (automated or manual review)

---

## 9. Git Hygiene

### Commit Quality
- [ ] **Conventional commit format** (`type(scope): description`)
- [ ] **Commits are atomic** (one logical change per commit)
- [ ] **Commit messages are descriptive** (why, not just what)
- [ ] **No "fix typo" commits** (squash before merge)

### Branch Management
- [ ] **Branch name follows convention** (`feat/`, `fix/`, `refactor/`)
- [ ] **Up to date with main/master** (rebase or merge before review)
- [ ] **No merge conflicts**

### Squash Strategy
| Change Type | Squash? | Reasoning |
|-------------|---------|-----------|
| Feature (multi-step) | No | Preserve logical steps |
| Bug fix | Yes | Single atomic fix |
| Refactor | Context | Preserve if multi-phase, squash if cleanup |
| Docs | Yes | Single commit fine |

---

## 10. Repository-Specific Checks

### Rust Projects (grimware, raibid-ci, hack-*)
- [ ] **Cargo.toml dependencies justified** (check `cargo tree`)
- [ ] **Feature flags documented** (in README)
- [ ] **No `unsafe` without justification** (comment explains why)
- [ ] **Clippy lints addressed** (no `#[allow(clippy::*)]` without reason)
- [ ] **Cross-compilation tested** (if targeting multiple platforms)

### Python Projects (dgx-*, ardour-mcp)
- [ ] **Dependencies in `pyproject.toml` or `requirements.txt`**
- [ ] **Virtual environment reproducible** (`poetry`, `uv`, or `venv`)
- [ ] **Type stubs for external libs** (if using `mypy --strict`)
- [ ] **No blocking I/O in async code** (use `asyncio` properly)
- [ ] **Notebook outputs cleared** (for `.ipynb` files in git)

### Infrastructure/IaC (mop, hack-k8s, raibid-ci)
- [ ] **YAML/JSON validated** (syntax check)
- [ ] **Secrets management** (use Sealed Secrets, ExternalSecrets)
- [ ] **Resource limits defined** (K8s manifests)
- [ ] **Rollback plan documented** (for infrastructure changes)
- [ ] **Terraform/Pulumi plans reviewed** (if using)

### Documentation Sites (docs)
- [ ] **Links are valid** (no 404s)
- [ ] **Images optimized** (WebP, compressed)
- [ ] **Code examples tested** (runnable snippets)
- [ ] **Search index updated** (if static site)

---

## 11. Non-Functional Requirements

### Accessibility (for UIs)
- [ ] **Keyboard navigation** (all interactive elements)
- [ ] **Screen reader friendly** (semantic HTML, ARIA labels)
- [ ] **Color contrast** (WCAG AA minimum)

### Localization (if applicable)
- [ ] **No hardcoded strings** (use i18n framework)
- [ ] **Date/time formatting** (locale-aware)
- [ ] **Number formatting** (locale-aware)

### Logging & Observability
- [ ] **Appropriate log levels** (ERROR, WARN, INFO, DEBUG, TRACE)
- [ ] **Structured logging** (JSON for services)
- [ ] **No sensitive data in logs** (PII, secrets)
- [ ] **Correlation IDs** (for distributed tracing)

### Error Handling Best Practices
**Rust:**
```rust
// ❌ Bad: Swallows error
let data = fetch_data().unwrap_or_default();

// ✅ Good: Propagates error context
let data = fetch_data()
    .context("Failed to fetch user data from API")?;
```

**Python:**
```python
# ❌ Bad: Generic exception
try:
    process_data(input)
except Exception as e:
    print(f"Error: {e}")

# ✅ Good: Specific exception, proper logging
try:
    process_data(input)
except ValidationError as e:
    logger.error(f"Invalid input: {e}", extra={"input": input})
    raise
except ProcessingError as e:
    logger.error(f"Processing failed: {e}", exc_info=True)
    raise
```

---

## 12. Final Review Checklist

Before approving:
- [ ] **I understand what this PR does** (asked clarifying questions if needed)
- [ ] **I've tested locally** (for complex changes)
- [ ] **I've reviewed the diff carefully** (line-by-line)
- [ ] **I've checked for unintended changes** (formatting, whitespace)
- [ ] **Breaking changes are justified and documented**
- [ ] **I would be comfortable maintaining this code**

---

## Review Feedback Guidelines

### Classifying Comments

Use these prefixes to indicate severity:

| Prefix | Meaning | Action Required |
|--------|---------|-----------------|
| **BLOCKING** | Must be fixed before merge | Yes |
| **IMPORTANT** | Should be addressed, but not blocking | Discuss |
| **NIT** | Minor suggestion, author's discretion | No |
| **QUESTION** | Clarification needed | Respond |
| **PRAISE** | Positive feedback | N/A |

**Examples:**
- ✅ **BLOCKING:** This will panic if `batch_size` is 0. Add validation.
- ✅ **IMPORTANT:** Consider caching this result. Profile shows 15% CPU time here.
- ✅ **NIT:** Could rename `data` to `pixel_data` for clarity.
- ✅ **QUESTION:** Why FP16 instead of FP32 here? Performance reason?
- ✅ **PRAISE:** Excellent test coverage! Clear test names.

### Providing Feedback

**DO:**
- 👍 Ask questions ("Why this approach?" not "This is wrong")
- 👍 Suggest alternatives with reasoning
- 👍 Link to documentation or examples
- 👍 Praise good work (motivation matters)
- 👍 Focus on code, not person

**DON'T:**
- ❌ "This is bad" (be specific)
- ❌ Nitpick formatting (automate with rustfmt/black)
- ❌ Request changes outside PR scope (file separate issues)
- ❌ Bikeshed variable names (unless truly confusing)
- ❌ Block for personal style preferences

---

## Post-Merge Actions

### After PR Merge
- [ ] **Delete feature branch** (keep repo clean)
- [ ] **Close linked issues** (if PR fully resolves them)
- [ ] **Monitor CI/CD** (ensure deployment succeeds)
- [ ] **Update project board** (move issue to "Done")

### If Issues Found Post-Merge
- [ ] **File issue immediately** (don't wait)
- [ ] **Revert if critical** (broken main is not acceptable)
- [ ] **Post-mortem for outages** (blameless, focus on process)

---

## Reviewer Rotation

To distribute knowledge and avoid bottlenecks:

1. **Auto-assign reviewers** (GitHub CODEOWNERS)
2. **Round-robin for fairness**
3. **Domain experts for critical changes** (security, performance)
4. **Two reviewers for large changes** (>400 LOC)

**Response Time Expectations:**
- **Small PRs (XS/S):** 24 hours
- **Medium PRs (M):** 48 hours
- **Large PRs (L):** 3-5 days (should be split anyway)

---

## Special Case Reviews

### Security-Critical Changes
- [ ] **Two reviewers required** (security-focused)
- [ ] **Threat model discussed** (attack vectors)
- [ ] **Penetration testing considered** (for auth/authz changes)

### Performance-Critical Changes
- [ ] **Benchmarks included** (before/after)
- [ ] **Profiling data reviewed** (flamegraphs, traces)
- [ ] **Regression tests added** (CI benchmarks)

### Breaking Changes
- [ ] **Migration guide written** (in PR description or docs)
- [ ] **Deprecation period observed** (warn before breaking)
- [ ] **Version bump planned** (semver: major version)

### Experimental Features (hack-* repos)
- [ ] **Lower review bar** (encourage iteration)
- [ ] **Focus on learnings** (what worked, what didn't)
- [ ] **Document results in README** (even if project abandoned)

---

## Tools to Assist Reviews

### Automated Tools
- **Rust:** `cargo clippy`, `cargo audit`, `cargo tarpaulin`
- **Python:** `ruff`, `mypy`, `bandit`, `pytest --cov`
- **TypeScript:** `eslint`, `tsc --noEmit`, `jest --coverage`
- **General:** `pre-commit` hooks, GitHub Actions

### Manual Review Aids
- **GitHub features:** Code suggestions, comment threads
- **Local testing:** `just test`, `just lint`, `just build`
- **Profiling:** `cargo flamegraph`, `py-spy`, Chrome DevTools

---

## Review Culture

### Raibid Labs Review Philosophy

**We review to:**
1. Ensure correctness and quality
2. Share knowledge across the team
3. Catch issues before production
4. Learn from each other's approaches

**We do NOT review to:**
1. Gatekeep or slow progress
2. Enforce personal style preferences
3. Show off knowledge
4. Nitpick trivial details

### Handling Disagreements

1. **Start with questions** ("Have you considered...?")
2. **Provide evidence** (docs, benchmarks, prior art)
3. **Escalate if needed** (tech lead, RFC process)
4. **Default to author** (if both approaches valid)
5. **Document decision** (ADR if architectural)

---

## Continuous Improvement

This checklist evolves. Suggest improvements via:
- PRs to `.claude/prompts/review-checklist.md`
- Issues tagged `process-improvement`
- Retrospectives after major projects

**Last Updated:** 2025-11-13
**Next Review:** Quarterly (or after major incidents)
