# Architecture Guidelines - Raibid Labs

## Overview
This document defines architectural standards and patterns for Raibid Labs projects, based on proven patterns from raibid-ci, grimware, dgx-*, and mop.

---

## Service Architecture Patterns

### Microservices vs Monolith Decision Matrix

**Use Microservices when**:
- Multiple teams working independently
- Different services have different scaling needs
- Services use different tech stacks (e.g., dgx-pixels, dgx-music)
- Need independent deployment cycles
- Services have distinct business domains

**Use Monolith when**:
- Single small team
- Shared business logic across components
- Early stage/MVP development
- Simple deployment requirements
- Tight coupling between features

**Raibid Labs Pattern**: Start with modular monolith, extract to microservices when scaling demands

```
Phase 1: Modular Monolith
┌─────────────────────────────┐
│      Single Service         │
│  ┌─────┐ ┌─────┐ ┌─────┐  │
│  │ API │ │Core │ │Data │  │
│  └─────┘ └─────┘ └─────┘  │
└─────────────────────────────┘

Phase 2: Extract High-Load Services
┌────────┐  ┌──────────────┐  ┌────────┐
│  API   │→ │Core Monolith │← │Worker  │
└────────┘  └──────────────┘  └────────┘
                  ↓
            ┌──────────┐
            │ Database │
            └──────────┘
```

---

## API Design Standards

### REST API Guidelines

**URL Structure**:
```
/api/v1/{resource}/{id}/{sub-resource}

✅ Good Examples:
GET    /api/v1/users
GET    /api/v1/users/123
POST   /api/v1/users
PUT    /api/v1/users/123
DELETE /api/v1/users/123
GET    /api/v1/users/123/projects

❌ Bad Examples:
GET    /api/get-users          (verb in URL)
POST   /api/v1/user            (singular noun)
GET    /api/v1/users?delete=1  (action via query param)
```

**HTTP Status Codes** (standard usage):
```
2xx Success:
  200 OK              - Successful GET, PUT, PATCH
  201 Created         - Successful POST creating resource
  204 No Content      - Successful DELETE

4xx Client Errors:
  400 Bad Request     - Invalid request body/parameters
  401 Unauthorized    - Missing/invalid authentication
  403 Forbidden       - Authenticated but not authorized
  404 Not Found       - Resource doesn't exist
  409 Conflict        - Resource conflict (e.g., duplicate)
  422 Unprocessable   - Validation errors

5xx Server Errors:
  500 Internal Error  - Unexpected server error
  502 Bad Gateway     - Upstream service error
  503 Service Unavailable - Service overloaded/down
```

**Response Format** (JSON standard):
```json
// Success response
{
  "data": {
    "id": "123",
    "name": "Example",
    "created_at": "2024-01-15T10:30:00Z"
  },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}

// Error response
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format"
      }
    ]
  },
  "meta": {
    "request_id": "req_abc123",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}

// Paginated list response
{
  "data": [...],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "total_pages": 8
  },
  "links": {
    "self": "/api/v1/users?page=1",
    "next": "/api/v1/users?page=2",
    "last": "/api/v1/users?page=8"
  }
}
```

**API Versioning**:
- Use URL versioning: `/api/v1/`, `/api/v2/`
- Maintain backward compatibility within major version
- Deprecate old versions with 6-month notice
- Document breaking changes in changelog

---

## Container Patterns

### Dockerfile Best Practices

**Multi-stage builds** (optimize image size):
```dockerfile
# Stage 1: Build
FROM rust:1.75 as builder
WORKDIR /build

# Cache dependencies
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN cargo build --release
RUN rm -rf src

# Build actual application
COPY src ./src
RUN cargo build --release

# Stage 2: Runtime
FROM debian:bookworm-slim
WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    ca-certificates \
    libssl3 \
    && rm -rf /var/lib/apt/lists/*

# Copy binary from builder
COPY --from=builder /build/target/release/app /app/

# Non-root user
RUN useradd -m -u 1000 appuser
USER appuser

EXPOSE 8080
CMD ["/app/app"]
```

**Python ML workload** (DGX pattern):
```dockerfile
FROM nvidia/cuda:12.2.0-runtime-ubuntu22.04
WORKDIR /workspace

# Install Python and system deps
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY models/ ./models/

# Non-root user
RUN useradd -m -u 1000 mluser
USER mluser

CMD ["python3", "-m", "src.main"]
```

**Docker Compose** (development environment):
```yaml
# docker-compose.yml
version: '3.9'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "8080:8080"
    environment:
      DATABASE_URL: postgres://postgres:password@db:5432/appdb
      REDIS_URL: redis://redis:6379
    volumes:
      - ./src:/app/src:ro
    depends_on:
      - db
      - redis
    develop:
      watch:
        - path: ./src
          action: rebuild

  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_DB: appdb
    volumes:
      - pgdata:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  pgdata:
```

---

## Kubernetes Deployment Patterns

### Resource Definitions

**Deployment** (stateless services):
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
  namespace: production
  labels:
    app: api-service
    version: v1.2.3
spec:
  replicas: 3
  revisionHistoryLimit: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: api-service
  template:
    metadata:
      labels:
        app: api-service
        version: v1.2.3
    spec:
      serviceAccountName: api-service
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: api
        image: ghcr.io/raibid-labs/api-service:v1.2.3
        imagePullPolicy: IfNotPresent
        ports:
        - name: http
          containerPort: 8080
          protocol: TCP
        env:
        - name: LOG_LEVEL
          value: "info"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: database-url
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 512Mi
        livenessProbe:
          httpGet:
            path: /health/live
            port: http
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health/ready
            port: http
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
        startupProbe:
          httpGet:
            path: /health/startup
            port: http
          initialDelaySeconds: 0
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 30
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
          - weight: 100
            podAffinityTerm:
              labelSelector:
                matchLabels:
                  app: api-service
              topologyKey: kubernetes.io/hostname
```

**Service** (expose pods):
```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
  namespace: production
  labels:
    app: api-service
spec:
  type: ClusterIP
  selector:
    app: api-service
  ports:
  - name: http
    port: 80
    targetPort: http
    protocol: TCP
  sessionAffinity: None
```

**HorizontalPodAutoscaler**:
```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-service-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-service
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 50
        periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
      - type: Pods
        value: 2
        periodSeconds: 15
      selectPolicy: Max
```

---

## Infrastructure as Code Standards

### Jsonnet/Tanka Pattern (mop, raibid-ci)

**Project Structure**:
```
iac/
├── lib/                    # Shared libraries
│   ├── k8s.libsonnet      # Kubernetes helpers
│   └── utils.libsonnet    # Common utilities
├── environments/
│   ├── dev/
│   │   ├── main.jsonnet
│   │   └── spec.json
│   ├── staging/
│   │   ├── main.jsonnet
│   │   └── spec.json
│   └── production/
│       ├── main.jsonnet
│       └── spec.json
├── tanka.yaml
└── jsonnetfile.json
```

**Jsonnet Template**:
```jsonnet
// environments/production/main.jsonnet
local k = import 'k8s.libsonnet';
local utils = import 'utils.libsonnet';

{
  apiVersion: 'tanka.dev/v1alpha1',
  kind: 'Environment',
  metadata: {
    name: 'production',
  },
  spec: {
    apiServer: 'https://api.k8s.prod.raibid.io',
    namespace: 'production',
  },
  data: {
    // Deployment
    deployment: k.deployment.new(
      name='api-service',
      replicas=3,
      containers=[
        k.container.new(
          name='api',
          image='ghcr.io/raibid-labs/api-service:v1.2.3',
        )
        + k.container.withPorts([
          k.containerPort.new(name='http', containerPort=8080),
        ])
        + k.container.resources.withRequests({
          cpu: '100m',
          memory: '128Mi',
        })
        + k.container.resources.withLimits({
          cpu: '500m',
          memory: '512Mi',
        }),
      ],
    ),

    // Service
    service: k.service.new(
      name='api-service',
      selector={app: 'api-service'},
      ports=[
        k.servicePort.new(name='http', port=80, targetPort='http'),
      ],
    ),
  },
}
```

**Justfile Integration**:
```just
# Infrastructure management

# Show diff for environment
diff env="dev":
  cd iac && tk diff environments/{{env}}

# Apply changes to environment
apply env="dev":
  cd iac && tk apply environments/{{env}}

# Show rendered manifests
show env="dev":
  cd iac && tk show environments/{{env}}

# Validate all environments
validate:
  cd iac && tk validate environments/dev
  cd iac && tk validate environments/staging
  cd iac && tk validate environments/production
```

---

## Multi-Language Project Organization

### Monorepo Structure (grimware pattern)

```
project-root/
├── rust/                   # Rust core library
│   ├── Cargo.toml
│   ├── src/
│   │   ├── lib.rs
│   │   └── modules/
│   └── tests/
├── python/                 # Python bindings/services
│   ├── pyproject.toml
│   ├── src/
│   │   └── project_name/
│   └── tests/
├── kotlin/                 # Mobile/Android
│   ├── build.gradle.kts
│   └── app/
├── typescript/             # Web frontend
│   ├── package.json
│   ├── src/
│   └── tests/
├── shared/                 # Shared resources
│   ├── schemas/           # API schemas (OpenAPI, Protobuf)
│   └── docs/              # Shared documentation
├── scripts/               # Build/deployment scripts
│   ├── build.nu
│   ├── test.nu
│   └── deploy.nu
├── k8s/                   # Kubernetes manifests
├── docker/                # Dockerfiles
│   ├── Dockerfile.rust
│   ├── Dockerfile.python
│   └── Dockerfile.web
├── .github/
│   └── workflows/         # CI/CD workflows
├── Justfile              # Unified task runner
├── docker-compose.yml    # Local development
└── README.md
```

**Cross-Language Communication**:

1. **FFI (Foreign Function Interface)** - Rust ↔ Python:
```rust
// Rust (using PyO3)
use pyo3::prelude::*;

#[pyfunction]
fn process_data(input: Vec<f64>) -> PyResult<Vec<f64>> {
    Ok(input.iter().map(|x| x * 2.0).collect())
}

#[pymodule]
fn rust_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(process_data, m)?)?;
    Ok(())
}
```

```python
# Python
import rust_core

result = rust_core.process_data([1.0, 2.0, 3.0])
```

2. **gRPC** - Language-agnostic services:
```protobuf
// shared/schemas/service.proto
syntax = "proto3";
package raibid.service.v1;

service DataProcessor {
  rpc ProcessData(DataRequest) returns (DataResponse);
}

message DataRequest {
  repeated double values = 1;
}

message DataResponse {
  repeated double results = 1;
}
```

3. **REST API** - HTTP-based integration (see API standards above)

---

## Database Architecture

### Database Selection Guide

**PostgreSQL** - Default choice for:
- Relational data with complex queries
- ACID transactions required
- JSON/JSONB support needed
- Full-text search
- Example: User accounts, metadata, configurations

**Redis** - Use for:
- Caching
- Session storage
- Real-time messaging (Pub/Sub)
- Rate limiting
- Example: API response caching, user sessions

**TimescaleDB** - Use for:
- Time-series data
- Metrics and monitoring
- IoT sensor data
- Example: ML training metrics, system telemetry

**Object Storage (S3/MinIO)** - Use for:
- Large files (models, datasets, media)
- Backup/archive
- Static assets
- Example: ML model weights, training datasets

### Schema Design Patterns

**Versioned Schema** (migrations):
```sql
-- migrations/001_initial.sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);

-- migrations/002_add_projects.sql
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_projects_user_id ON projects(user_id);
```

**Use migration tools**:
- Rust: `sqlx` or `diesel`
- Python: `alembic` or `yoyo-migrations`
- TypeScript: `knex` or `prisma`

---

## Observability Architecture

### Logging Standard

**Structured Logging** (JSON format):
```rust
// Rust (using tracing)
use tracing::{info, error, instrument};

#[instrument(skip(db))]
async fn process_request(user_id: &str, db: &Database) -> Result<()> {
    info!(user_id = %user_id, "Processing request");

    match db.query(user_id).await {
        Ok(data) => {
            info!(
                user_id = %user_id,
                records = data.len(),
                "Request processed successfully"
            );
            Ok(())
        }
        Err(e) => {
            error!(
                user_id = %user_id,
                error = %e,
                "Request processing failed"
            );
            Err(e)
        }
    }
}
```

```python
# Python (using structlog)
import structlog

logger = structlog.get_logger()

async def process_request(user_id: str, db: Database):
    logger.info("processing_request", user_id=user_id)

    try:
        data = await db.query(user_id)
        logger.info(
            "request_processed",
            user_id=user_id,
            records=len(data)
        )
    except Exception as e:
        logger.error(
            "request_failed",
            user_id=user_id,
            error=str(e),
            exc_info=True
        )
        raise
```

**Log Levels**:
- `ERROR` - System errors requiring immediate attention
- `WARN` - Degraded functionality, potential issues
- `INFO` - Normal operations, state changes
- `DEBUG` - Detailed diagnostic information (dev/staging only)

### Metrics

**Use Prometheus format**:
```rust
// Rust (using prometheus crate)
use prometheus::{Counter, Histogram, register_counter, register_histogram};

lazy_static! {
    static ref HTTP_REQUESTS: Counter = register_counter!(
        "http_requests_total",
        "Total HTTP requests"
    ).unwrap();

    static ref HTTP_DURATION: Histogram = register_histogram!(
        "http_request_duration_seconds",
        "HTTP request duration"
    ).unwrap();
}

async fn handle_request() {
    HTTP_REQUESTS.inc();
    let timer = HTTP_DURATION.start_timer();

    // Process request

    timer.observe_duration();
}
```

**Standard Metrics** (expose in all services):
- Request count by endpoint, status code
- Request duration (histogram)
- Error rate
- Active connections
- Queue depth
- Custom business metrics

---

## Security Architecture

**See [security.md](security.md) for detailed security guidelines.**

Key architectural patterns:
- API Gateway for authentication/authorization
- Network policies in Kubernetes
- Secrets management via external secret stores
- TLS/mTLS for service-to-service communication
- Regular dependency scanning

---

## Performance Patterns

### Caching Strategy

**Cache Levels**:
1. **Application Cache** (in-memory): Hot data, <100MB
2. **Distributed Cache** (Redis): Shared data, minutes to hours TTL
3. **CDN**: Static assets, long TTL
4. **Database Query Cache**: PostgreSQL shared buffers

**Cache Invalidation**:
- TTL-based for read-heavy, eventually consistent data
- Event-based for write-sensitive data
- LRU eviction for memory-constrained caches

### Asynchronous Processing

**Queue-based workers** (for long-running tasks):
```
┌──────┐    ┌──────────┐    ┌────────┐
│ API  │───→│  Queue   │───→│ Worker │
└──────┘    │ (Redis)  │    └────────┘
            └──────────┘         │
                                 ↓
                            ┌─────────┐
                            │ Storage │
                            └─────────┘
```

**Use cases**:
- ML model training/inference
- Data processing pipelines
- Report generation
- Email/notification sending

---

## Disaster Recovery

### Backup Strategy

**Database Backups**:
- Automated daily backups (retain 30 days)
- Point-in-time recovery (WAL archiving)
- Test restoration monthly

**Application State**:
- Configuration stored in version control
- Infrastructure as Code for reproducibility
- Container images tagged and archived

**Disaster Recovery Plan**:
- RTO (Recovery Time Objective): 4 hours
- RPO (Recovery Point Objective): 1 hour
- Document and test recovery procedures quarterly

---

## References

- [API Design Guide](https://cloud.google.com/apis/design)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
- [12-Factor App](https://12factor.net/)
- [Jsonnet Documentation](https://jsonnet.org/learning/tutorial.html)
