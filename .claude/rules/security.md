# Security Guidelines - Raibid Labs

## Overview
This document defines security standards and best practices for all Raibid Labs projects. Security is not optional—all projects MUST follow these guidelines.

---

## Secret Management

### ❌ NEVER Commit Secrets

**Forbidden Practices**:
```
# ❌ NEVER do this
DATABASE_URL = "postgres://user:password@host/db"
API_KEY = "sk-1234567890abcdef"
AWS_SECRET_KEY = "abcdefghijklmnop"

# config.py
SECRET_KEY = "hardcoded-secret-key"
```

**Consequences**:
- Secrets committed to Git are **permanently** in history
- Public repositories expose secrets to the world
- Even private repos can be accessed by unauthorized users
- Rotating compromised secrets is costly and disruptive

### ✅ Proper Secret Management

**1. Environment Variables** (Development):
```bash
# .env (add to .gitignore!)
DATABASE_URL=postgres://user:password@localhost/db
API_KEY=sk-development-key

# .env.example (commit this)
DATABASE_URL=postgres://user:password@host/db
API_KEY=your-api-key-here
```

```python
# Python - use python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]
API_KEY = os.environ["API_KEY"]
```

```rust
// Rust - use dotenvy or dotenv
use std::env;

fn main() {
    dotenvy::dotenv().ok();
    let database_url = env::var("DATABASE_URL")
        .expect("DATABASE_URL must be set");
    let api_key = env::var("API_KEY")
        .expect("API_KEY must be set");
}
```

**2. Kubernetes Secrets** (Production):
```yaml
# k8s/secrets.yaml (DO NOT COMMIT - use sealed-secrets or external-secrets)
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: production
type: Opaque
stringData:
  database-url: postgres://user:password@db/prod
  api-key: sk-production-key
```

**Use in Deployment**:
```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: app
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: database-url
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: api-key
```

**3. External Secret Stores** (Recommended for Production):

**AWS Secrets Manager / HashiCorp Vault**:
```rust
// Rust - fetch from AWS Secrets Manager
use aws_sdk_secretsmanager::Client;

async fn get_secret(client: &Client, name: &str) -> Result<String> {
    let response = client
        .get_secret_value()
        .secret_id(name)
        .send()
        .await?;

    Ok(response.secret_string().unwrap().to_string())
}
```

**Kubernetes External Secrets Operator**:
```yaml
# k8s/external-secret.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
  namespace: production
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: app-secrets
    creationPolicy: Owner
  data:
  - secretKey: database-url
    remoteRef:
      key: production/database-url
  - secretKey: api-key
    remoteRef:
      key: production/api-key
```

### Secret Scanning

**Pre-commit Hook** (detect secrets before commit):
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: detect-private-key
      - id: detect-aws-credentials

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

**GitHub Action** (scan repository):
```yaml
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]

jobs:
  secret-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for scanning

      - name: TruffleHog Scan
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD
```

---

## Dependency Security

### Dependency Scanning (Required)

**Rust**:
```bash
# Install cargo-audit
cargo install cargo-audit

# Scan for vulnerabilities
cargo audit

# Add to CI/CD
just audit:
  cargo audit --deny warnings
```

**Python**:
```bash
# Install safety
pip install safety

# Scan for vulnerabilities
safety check --json

# Or use pip-audit (more comprehensive)
pip install pip-audit
pip-audit

# Add to CI/CD
just audit:
  pip-audit --require-hashes --strict
```

**TypeScript/Node.js**:
```bash
# Use npm audit or yarn audit
npm audit

# Fix automatically when possible
npm audit fix

# Add to CI/CD
just audit:
  npm audit --audit-level=moderate
```

### Dependabot Configuration

**All repositories MUST enable Dependabot**:
```yaml
# .github/dependabot.yml
version: 2
updates:
  # Rust dependencies
  - package-ecosystem: "cargo"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "security-team"
    labels:
      - "dependencies"
      - "security"

  # Python dependencies
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10

  # NPM dependencies
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10

  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Dependency Pinning

**Lock files are MANDATORY**:
- Rust: `Cargo.lock` (commit to Git)
- Python: `requirements.lock` or `poetry.lock` (commit to Git)
- Node.js: `package-lock.json` or `yarn.lock` (commit to Git)

**Why**:
- Reproducible builds
- Protection against supply chain attacks
- Explicit dependency upgrades

---

## Container Security

### Dockerfile Security Best Practices

**✅ Secure Dockerfile**:
```dockerfile
# Use specific version tags, not 'latest'
FROM rust:1.75-slim as builder

# Run as non-root user
RUN useradd -m -u 1000 builder
USER builder
WORKDIR /build

# Copy only necessary files
COPY --chown=builder:builder Cargo.toml Cargo.lock ./
COPY --chown=builder:builder src/ ./src/

RUN cargo build --release

# Minimal runtime image
FROM debian:bookworm-slim

# Install only required runtime dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    libssl3 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Non-root user
RUN useradd -m -u 1000 appuser
USER appuser
WORKDIR /app

# Copy only the binary
COPY --from=builder --chown=appuser:appuser /build/target/release/app /app/

# Drop capabilities (when running with --cap-drop=ALL)
# No SUID/SGID bits
RUN chmod -R go-w /app

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
  CMD ["/app/app", "--health-check"]

EXPOSE 8080
CMD ["/app/app"]
```

**❌ Insecure Dockerfile**:
```dockerfile
# ❌ Using 'latest' tag (unpredictable)
FROM rust:latest

# ❌ Running as root
WORKDIR /app
COPY . .
RUN cargo build --release

# ❌ No specific version
FROM debian

# ❌ Still running as root
COPY --from=0 /app/target/release/app /app/
CMD ["/app/app"]  # Runs as root!
```

### Container Scanning

**Trivy** (recommended scanner):
```bash
# Install trivy
brew install trivy  # macOS
# or download from https://github.com/aquasecurity/trivy

# Scan Docker image
trivy image --severity HIGH,CRITICAL myimage:latest

# Scan filesystem
trivy fs --severity HIGH,CRITICAL .
```

**GitHub Action**:
```yaml
# .github/workflows/container-scan.yml
name: Container Security Scan
on:
  push:
    branches: [main]
  pull_request:

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build image
        run: docker build -t ${{ github.repository }}:${{ github.sha }} .

      - name: Run Trivy scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ github.repository }}:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'HIGH,CRITICAL'

      - name: Upload results to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'
```

### Kubernetes Pod Security

**Pod Security Standards** (enforce in all namespaces):
```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

**Secure Pod Spec**:
```yaml
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      # Security Context for all containers
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        runAsGroup: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault

      containers:
      - name: app
        image: myimage:v1.0.0

        # Container-specific security
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
              - ALL

        # Resource limits (prevent resource exhaustion)
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi

        # Read-only volumes
        volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/cache

      volumes:
      - name: tmp
        emptyDir: {}
      - name: cache
        emptyDir: {}
```

---

## API Security

### Authentication & Authorization

**JWT Authentication Pattern**:
```rust
// Rust - JWT middleware
use jsonwebtoken::{decode, Validation, DecodingKey};
use axum::{
    extract::Request,
    http::StatusCode,
    middleware::Next,
    response::Response,
};

#[derive(Deserialize)]
struct Claims {
    sub: String,  // Subject (user ID)
    exp: usize,   // Expiration
    roles: Vec<String>,
}

async fn auth_middleware(
    req: Request,
    next: Next,
) -> Result<Response, StatusCode> {
    let token = req
        .headers()
        .get("Authorization")
        .and_then(|h| h.to_str().ok())
        .and_then(|h| h.strip_prefix("Bearer "))
        .ok_or(StatusCode::UNAUTHORIZED)?;

    let key = env::var("JWT_SECRET").expect("JWT_SECRET must be set");
    let decoding_key = DecodingKey::from_secret(key.as_bytes());

    decode::<Claims>(token, &decoding_key, &Validation::default())
        .map_err(|_| StatusCode::UNAUTHORIZED)?;

    Ok(next.run(req).await)
}
```

**Role-Based Access Control (RBAC)**:
```rust
fn check_permission(user: &User, resource: &str, action: &str) -> bool {
    user.roles.iter().any(|role| {
        match (role.as_str(), resource, action) {
            ("admin", _, _) => true,
            ("user", "users", "read") => true,
            ("user", "projects", _) => true,
            _ => false,
        }
    })
}
```

### Input Validation

**Always validate user input**:
```rust
// Rust - use validator crate
use validator::{Validate, ValidationError};

#[derive(Deserialize, Validate)]
struct CreateUserRequest {
    #[validate(length(min = 3, max = 50))]
    username: String,

    #[validate(email)]
    email: String,

    #[validate(length(min = 8))]
    #[validate(custom = "validate_password")]
    password: String,
}

fn validate_password(password: &str) -> Result<(), ValidationError> {
    let has_uppercase = password.chars().any(|c| c.is_uppercase());
    let has_lowercase = password.chars().any(|c| c.is_lowercase());
    let has_digit = password.chars().any(|c| c.is_numeric());

    if has_uppercase && has_lowercase && has_digit {
        Ok(())
    } else {
        Err(ValidationError::new("password_strength"))
    }
}

async fn create_user(
    Json(payload): Json<CreateUserRequest>,
) -> Result<Json<User>, StatusCode> {
    payload.validate()
        .map_err(|_| StatusCode::BAD_REQUEST)?;

    // Process validated input
    Ok(Json(user))
}
```

```python
# Python - use pydantic
from pydantic import BaseModel, EmailStr, Field, validator

class CreateUserRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain lowercase')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v

@app.post("/users")
async def create_user(request: CreateUserRequest):
    # Input is already validated by pydantic
    pass
```

### SQL Injection Prevention

**✅ Use Parameterized Queries**:
```rust
// Rust - sqlx
let user = sqlx::query_as!(
    User,
    "SELECT * FROM users WHERE email = $1",
    email  // Parameter is safely escaped
)
.fetch_one(&pool)
.await?;
```

```python
# Python - asyncpg
user = await conn.fetchrow(
    "SELECT * FROM users WHERE email = $1",
    email  # Parameter is safely escaped
)
```

**❌ NEVER Concatenate User Input**:
```rust
// ❌ VULNERABLE TO SQL INJECTION
let query = format!("SELECT * FROM users WHERE email = '{}'", email);
sqlx::raw_sql(&query).fetch_one(&pool).await?;
```

---

## GPU/ML Workload Security

### DGX-Specific Considerations

**Resource Isolation**:
```yaml
# Kubernetes - GPU resource limits
apiVersion: v1
kind: Pod
metadata:
  name: ml-training
spec:
  containers:
  - name: trainer
    resources:
      limits:
        nvidia.com/gpu: 1  # Request 1 GPU
        memory: 16Gi
        cpu: 4
```

**Model Poisoning Prevention**:
- Verify model checksums before loading
- Use signed/trusted model sources only
- Scan models for embedded malware

```python
import hashlib

def verify_model_checksum(model_path: Path, expected_sha256: str) -> bool:
    """Verify model file integrity."""
    sha256 = hashlib.sha256()
    with model_path.open('rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)

    computed = sha256.hexdigest()
    if computed != expected_sha256:
        raise ValueError(
            f"Model checksum mismatch: {computed} != {expected_sha256}"
        )
    return True

# Load model only after verification
verify_model_checksum(model_path, known_good_checksum)
model = torch.load(model_path)
```

**Data Privacy**:
- Sanitize training data (no PII in logs)
- Encrypt datasets at rest
- Use differential privacy techniques

---

## OWASP Top 10 Awareness

### Critical Vulnerabilities to Prevent

1. **A01:2021 – Broken Access Control**
   - Always check permissions before operations
   - Deny by default, allow explicitly
   - Test authorization logic thoroughly

2. **A02:2021 – Cryptographic Failures**
   - Use TLS 1.3 for all network traffic
   - Never roll your own crypto
   - Use bcrypt/argon2 for password hashing

3. **A03:2021 – Injection**
   - Parameterized queries (SQL)
   - Input validation and sanitization
   - Escape outputs in HTML/JS context

4. **A04:2021 – Insecure Design**
   - Threat modeling during design phase
   - Security requirements in stories
   - Defense in depth

5. **A05:2021 – Security Misconfiguration**
   - Disable debug mode in production
   - Remove default accounts/passwords
   - Keep software up to date

6. **A06:2021 – Vulnerable Components**
   - Automated dependency scanning
   - Regular updates
   - Remove unused dependencies

7. **A07:2021 – Identification and Authentication Failures**
   - Multi-factor authentication
   - Strong password policies
   - Secure session management

8. **A08:2021 – Software and Data Integrity Failures**
   - Verify signatures on updates
   - Integrity checks for dependencies
   - Code signing for releases

9. **A09:2021 – Security Logging and Monitoring Failures**
   - Log all security events
   - Real-time alerting
   - Retain logs for forensics

10. **A10:2021 – Server-Side Request Forgery (SSRF)**
    - Validate/sanitize URLs
    - Allowlist of permitted destinations
    - Network segmentation

---

## Security Checklist

Before deployment, verify:

- [ ] No secrets in Git history
- [ ] All dependencies scanned and up to date
- [ ] Container images scanned (no HIGH/CRITICAL vulns)
- [ ] Kubernetes Pod Security Standards enforced
- [ ] Authentication/authorization implemented
- [ ] Input validation on all user inputs
- [ ] Parameterized SQL queries
- [ ] TLS enabled for all external traffic
- [ ] Non-root containers
- [ ] Resource limits configured
- [ ] Logging/monitoring enabled
- [ ] Backup/recovery procedures documented
- [ ] Security team review completed

---

## Incident Response

**If a security incident occurs**:

1. **Contain**: Isolate affected systems immediately
2. **Assess**: Determine scope and impact
3. **Notify**: Security team and relevant stakeholders
4. **Remediate**: Fix vulnerability, rotate credentials
5. **Document**: Post-mortem and lessons learned
6. **Prevent**: Update procedures to prevent recurrence

**Emergency Contacts**:
- Security team: security@raibid-labs.io
- On-call engineer: [PagerDuty/Slack]

---

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
