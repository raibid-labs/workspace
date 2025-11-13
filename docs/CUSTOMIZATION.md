# Customizing Organization Configuration

**Complete guide for overriding and extending raibid-labs org settings for specific repository needs**

## Table of Contents

1. [Overview](#overview)
2. [Customization Principles](#customization-principles)
3. [Override Patterns](#override-patterns)
4. [Adding Custom MCP Servers](#adding-custom-mcp-servers)
5. [Modifying Templates](#modifying-templates)
6. [Rule Customization](#rule-customization)
7. [Advanced Customization](#advanced-customization)
8. [Examples by Use Case](#examples-by-use-case)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

---

## Overview

While the raibid-labs organization configuration provides consistent defaults, individual repositories often need specific customizations. This guide explains how to properly override, extend, and customize the org configuration without breaking inheritance.

### Customization Hierarchy

```
┌─────────────────────────────┐
│  Organization Config         │  ← Base layer (lowest priority)
│  (claude-org-config)         │
└──────────┬───────────────────┘
           │
┌──────────▼───────────────────┐
│  Template Config             │  ← Template layer
│  (rust-service.json, etc.)   │
└──────────┬───────────────────┘
           │
┌──────────▼───────────────────┐
│  Repository Config           │  ← Repo layer (highest priority)
│  (.claude/project.json)      │
└──────────────────────────────┘
```

### When to Customize

Customize when your repository:
- Uses unique frameworks or tools not covered by org standards
- Has specific security or compliance requirements
- Requires specialized MCP servers or tools
- Follows domain-specific conventions (e.g., scientific computing, ML)
- Needs to override org defaults for valid reasons

---

## Customization Principles

### 1. Extend, Don't Replace

**Preferred:** Extend org configuration
```json
{
  "extends": "github:raibid-labs/claude-org-config/templates/repo-types/rust-service.json",
  "rules": {
    "org_rules": "inherit",
    "additional": ["./docs/SPECIAL_RULES.md"]
  }
}
```

**Avoid:** Complete replacement
```json
{
  // No extends - loses all org benefits
  "name": "my-repo",
  "rules": ["./my-rules.md"]
}
```

### 2. Document Your Overrides

Always document why you're overriding:
```json
{
  "overrides": {
    "comment": "Using Deno instead of Node.js for better security",
    "runtime": "deno",
    "package_manager": null
  }
}
```

### 3. Maintain Compatibility

Ensure customizations don't break team workflows:
```json
{
  "compatibility": {
    "min_claude_version": "1.0.0",
    "requires_mcp_servers": ["custom-server"],
    "conflicts_with": ["node-specific-tools"]
  }
}
```

---

## Override Patterns

### Pattern 1: Additive Customization

Add to org settings without removing anything:

```json
{
  "extends": "github:raibid-labs/claude-org-config/templates/repo-types/python-service.json",
  "rules": {
    "org_rules": "inherit",
    "additional": [
      "./docs/ML_GUIDELINES.md",
      "./docs/DATA_PROCESSING.md"
    ]
  },
  "context": {
    "inherit_org": true,
    "additional": {
      "notebooks": "./notebooks/",
      "models": "./models/",
      "datasets": "./data/"
    }
  }
}
```

### Pattern 2: Selective Override

Override specific settings while keeping others:

```json
{
  "extends": "github:raibid-labs/claude-org-config/templates/repo-types/rust-service.json",
  "overrides": {
    "testing": {
      "framework": "criterion",  // Override default test framework
      "coverage_threshold": 95,   // Higher than org standard
      "keep_org_defaults": ["test_structure", "naming_conventions"]
    },
    "async_runtime": "async-std"  // Override tokio default
  }
}
```

### Pattern 3: Complete Section Override

Replace entire configuration sections:

```json
{
  "extends": "github:raibid-labs/claude-org-config/templates/repo-types/base-template.json",
  "rules": {
    "replace": true,  // Don't inherit org rules
    "custom": [
      "./QUANTUM_COMPUTING_RULES.md",
      "./CRYPTOGRAPHY_STANDARDS.md"
    ]
  },
  "justification": "Quantum computing repo with unique requirements"
}
```

### Pattern 4: Conditional Override

Override based on environment or context:

```json
{
  "extends": "github:raibid-labs/claude-org-config/templates/repo-types/typescript-service.json",
  "conditional_overrides": [
    {
      "condition": "environment === 'production'",
      "overrides": {
        "logging_level": "error",
        "optimizations": "aggressive"
      }
    },
    {
      "condition": "branch === 'experimental'",
      "overrides": {
        "allow_unsafe": true,
        "experimental_features": true
      }
    }
  ]
}
```

---

## Adding Custom MCP Servers

### Basic MCP Server Addition

Add repository-specific MCP servers:

```json
{
  "extends": "github:raibid-labs/claude-org-config/templates/repo-types/python-ml.json",
  "mcp_servers": {
    "inherit_org": true,  // Keep org servers
    "custom": {
      "jupyter-context": {
        "command": "python",
        "args": ["-m", "jupyter_mcp_server"],
        "env": {
          "NOTEBOOK_DIR": "./notebooks"
        }
      },
      "mlflow-tracker": {
        "command": "mlflow",
        "args": ["mcp-serve"],
        "env": {
          "MLFLOW_TRACKING_URI": "./mlruns"
        }
      }
    }
  }
}
```

### Override Org MCP Servers

Replace or modify org-level MCP servers:

```json
{
  "mcp_servers": {
    "org_overrides": {
      "repo-standards": {
        "disabled": true,  // Disable this org server
        "reason": "Using custom validation"
      },
      "org-context": {
        "env_override": {
          "CUSTOM_FLAG": "true",
          "REPO_SPECIFIC": "value"
        }
      }
    },
    "replacements": {
      "repo-standards": {
        "command": "npx",
        "args": ["-y", "@myrepo/custom-validator"],
        "replaces": "org-server"
      }
    }
  }
}
```

### Environment-Specific MCP Servers

Configure MCP servers per environment:

```json
{
  "mcp_servers": {
    "base": {
      "inherit_org": true
    },
    "development": {
      "debug-server": {
        "command": "npx",
        "args": ["-y", "claude-debug-server"],
        "env": {
          "DEBUG": "true"
        }
      }
    },
    "production": {
      "monitoring-server": {
        "command": "npx",
        "args": ["-y", "prod-monitor-mcp"],
        "env": {
          "METRICS_ENDPOINT": "${METRICS_URL}"
        }
      }
    }
  }
}
```

---

## Modifying Templates

### Creating Custom Templates

For repos that don't fit standard templates:

```json
{
  "name": "custom-repo-template",
  "description": "Template for quantum computing services",
  "base": "github:raibid-labs/claude-org-config/templates/repo-types/base-template.json",
  "customizations": {
    "languages": ["python", "qiskit", "cirq"],
    "rules": [
      "./templates/quantum-rules.md",
      "./templates/quantum-patterns.md"
    ],
    "context": {
      "quantum_circuits": "./circuits/",
      "algorithms": "./quantum_algorithms/",
      "simulations": "./simulations/"
    },
    "specific_requirements": {
      "min_qubit_count": 5,
      "supported_backends": ["qiskit_aer", "cirq_simulator"],
      "noise_models": true
    }
  }
}
```

### Extending Existing Templates

Build on top of org templates:

```json
{
  "extends": "github:raibid-labs/claude-org-config/templates/repo-types/rust-service.json",
  "template_extensions": {
    "add_rules": [
      "./embedded-systems-rules.md"
    ],
    "modify_context": {
      "remove": ["./examples/"],  // Not applicable
      "add": {
        "hal": "./src/hal/",
        "drivers": "./src/drivers/",
        "board_configs": "./boards/"
      }
    },
    "toolchain": {
      "target": "thumbv7em-none-eabihf",
      "features": ["no_std", "embedded", "hal"]
    }
  }
}
```

### Template Composition

Combine multiple templates:

```json
{
  "name": "hybrid-service",
  "compose_from": [
    "github:raibid-labs/claude-org-config/templates/repo-types/rust-service.json",
    "github:raibid-labs/claude-org-config/templates/repo-types/python-ml.json"
  ],
  "composition_strategy": {
    "rules": "merge",  // Combine all rules
    "context": "merge",  // Combine contexts
    "mcp_servers": "merge",  // Include all servers
    "conflicts": {
      "testing_framework": "pytest",  // Resolve conflict
      "build_system": "maturin"  // For Rust+Python
    }
  }
}
```

---

## Rule Customization

### Adding Domain-Specific Rules

Create rules for specialized domains:

```json
{
  "extends": "github:raibid-labs/claude-org-config/templates/repo-types/python-service.json",
  "domain_rules": {
    "healthcare": [
      "./rules/HIPAA_COMPLIANCE.md",
      "./rules/PHI_HANDLING.md",
      "./rules/AUDIT_LOGGING.md"
    ],
    "override_org_rules": {
      "data_retention": "7_years",  // HIPAA requirement
      "encryption": "AES-256",  // Minimum standard
      "audit_trail": "required"
    }
  }
}
```

### Rule Priority and Conflicts

Define how rules interact:

```json
{
  "rule_priority": {
    "order": [
      "security_rules",     // Highest priority
      "compliance_rules",
      "org_rules",
      "team_rules",
      "repo_rules"         // Lowest priority
    ],
    "conflict_resolution": "highest_priority_wins",
    "exceptions": {
      "testing_rules": "always_override",  // Testing rules always win
      "performance_rules": "merge"  // Combine performance rules
    }
  },
  "rules": {
    "security_rules": ["./security/STRICT_RULES.md"],
    "compliance_rules": ["./compliance/SOC2.md"],
    "org_rules": "inherit",
    "team_rules": ["./team/CONVENTIONS.md"],
    "repo_rules": ["./REPO_SPECIFIC.md"]
  }
}
```

### Conditional Rules

Apply rules based on conditions:

```json
{
  "conditional_rules": [
    {
      "condition": "file_path.includes('src/crypto')",
      "apply_rules": ["./rules/CRYPTOGRAPHY.md"],
      "override": {
        "allow_console_log": false,
        "require_security_review": true
      }
    },
    {
      "condition": "file_path.includes('test')",
      "apply_rules": ["./rules/TESTING.md"],
      "override": {
        "allow_any": ["console.log", "debugger"],
        "coverage_required": false
      }
    }
  ]
}
```

---

## Advanced Customization

### Dynamic Configuration

Load configuration based on runtime conditions:

```json
{
  "dynamic_config": {
    "loader": "./scripts/load-config.js",
    "cache_duration": 3600,
    "variables": {
      "team": "${TEAM_NAME}",
      "environment": "${ENV}",
      "feature_flags": "${FEATURE_FLAGS}"
    }
  }
}
```

```javascript
// scripts/load-config.js
module.exports = async function loadConfig(variables) {
  const { team, environment, feature_flags } = variables;

  // Dynamic rule selection
  const rules = ['./base-rules.md'];
  if (team === 'security') {
    rules.push('./security-team-rules.md');
  }
  if (environment === 'production') {
    rules.push('./production-rules.md');
  }

  // Feature flag based configuration
  const features = JSON.parse(feature_flags || '{}');
  const config = {
    rules,
    experimental_features: features.experimental || false,
    strict_mode: features.strict_mode || false
  };

  return config;
};
```

### Plugin System

Extend Claude's capabilities with plugins:

```json
{
  "plugins": [
    {
      "name": "custom-linter",
      "path": "./plugins/linter.js",
      "config": {
        "rules": ["no-var", "prefer-const"],
        "auto_fix": true
      }
    },
    {
      "name": "api-generator",
      "path": "./plugins/api-gen.js",
      "triggers": ["on_save", "on_build"],
      "config": {
        "spec": "./api/openapi.yaml",
        "output": "./generated/"
      }
    }
  ]
}
```

### Custom Knowledge Sources

Define specialized knowledge sources:

```json
{
  "knowledge_sources": {
    "inherit_org": true,
    "custom": [
      {
        "type": "api",
        "name": "Internal API Docs",
        "endpoint": "https://api-docs.raibid-labs.internal",
        "auth": {
          "type": "bearer",
          "token": "${INTERNAL_API_TOKEN}"
        }
      },
      {
        "type": "database",
        "name": "Schema Documentation",
        "connection": {
          "type": "postgres",
          "host": "localhost",
          "database": "development",
          "schema_only": true
        }
      },
      {
        "type": "dynamic",
        "name": "Runtime Metrics",
        "loader": "./scripts/load-metrics.js",
        "refresh_interval": 300
      }
    ]
  }
}
```

### Integration Hooks

Define hooks for various Claude operations:

```json
{
  "hooks": {
    "pre_commit": {
      "script": "./hooks/pre-commit.sh",
      "blocking": true,
      "timeout": 30
    },
    "post_generation": {
      "script": "./hooks/format-code.sh",
      "applies_to": ["*.rs", "*.ts", "*.py"]
    },
    "pre_context_load": {
      "script": "./hooks/prepare-context.js",
      "modifies_context": true
    },
    "validation": {
      "script": "./hooks/validate-claude-output.js",
      "on_failure": "warn"  // or "block"
    }
  }
}
```

---

## Examples by Use Case

### Example 1: Microservice with Custom Protocol

```json
{
  "name": "grpc-service",
  "extends": "github:raibid-labs/claude-org-config/templates/repo-types/rust-service.json",
  "protocol_customization": {
    "type": "grpc",
    "rules": [
      "./docs/GRPC_CONVENTIONS.md",
      "./proto/README.md"
    ],
    "context": {
      "proto_files": "./proto/",
      "generated_code": "./src/generated/",
      "client_examples": "./examples/clients/"
    },
    "tools": {
      "protoc": {
        "version": "3.20.0",
        "plugins": ["tonic", "prost"]
      }
    }
  },
  "overrides": {
    "serialization": "protobuf",
    "transport": "grpc",
    "http_server": null  // Not using HTTP
  }
}
```

### Example 2: Machine Learning Pipeline

```json
{
  "name": "ml-pipeline",
  "extends": "github:raibid-labs/claude-org-config/templates/repo-types/python-ml.json",
  "ml_customization": {
    "pipeline_stages": [
      "data_ingestion",
      "preprocessing",
      "feature_engineering",
      "training",
      "evaluation",
      "deployment"
    ],
    "frameworks": {
      "ml": "scikit-learn",
      "deep_learning": "pytorch",
      "data_processing": "polars",
      "orchestration": "airflow"
    },
    "rules": [
      "./docs/ML_PIPELINE_RULES.md",
      "./docs/EXPERIMENT_TRACKING.md"
    ],
    "context": {
      "dags": "./airflow/dags/",
      "transforms": "./src/transforms/",
      "models": "./models/",
      "configs": "./configs/experiments/"
    },
    "mcp_servers": {
      "mlflow": {
        "command": "mlflow",
        "args": ["server", "--mcp"],
        "env": {
          "MLFLOW_TRACKING_URI": "./mlruns"
        }
      }
    }
  }
}
```

### Example 3: Multi-Cloud Infrastructure

```json
{
  "name": "multi-cloud-infra",
  "extends": "github:raibid-labs/claude-org-config/templates/repo-types/infrastructure-terraform.json",
  "cloud_customization": {
    "providers": ["aws", "gcp", "azure"],
    "environments": {
      "dev": {
        "primary": "aws",
        "regions": ["us-west-2"]
      },
      "staging": {
        "primary": "gcp",
        "regions": ["us-central1", "europe-west1"]
      },
      "production": {
        "primary": "aws",
        "secondary": "azure",
        "regions": ["us-east-1", "eu-west-1", "ap-southeast-1"]
      }
    },
    "rules": [
      "./docs/MULTI_CLOUD_STRATEGY.md",
      "./docs/CLOUD_SPECIFIC_PATTERNS.md"
    ],
    "context": {
      "modules": "./terraform/modules/",
      "environments": "./terraform/environments/",
      "policies": "./policies/"
    },
    "compliance": {
      "standards": ["SOC2", "ISO27001", "HIPAA"],
      "scanning": "checkov",
      "policy_as_code": "sentinel"
    }
  }
}
```

### Example 4: Blockchain/Web3 Service

```json
{
  "name": "web3-service",
  "extends": "github:raibid-labs/claude-org-config/templates/repo-types/typescript-service.json",
  "blockchain_customization": {
    "chain": "ethereum",
    "layer": "L2",
    "network": "arbitrum",
    "rules": [
      "./docs/SMART_CONTRACT_SECURITY.md",
      "./docs/WEB3_BEST_PRACTICES.md",
      "./docs/GAS_OPTIMIZATION.md"
    ],
    "context": {
      "contracts": "./contracts/",
      "deployments": "./deployments/",
      "tests": "./test/contracts/",
      "scripts": "./scripts/blockchain/"
    },
    "tools": {
      "framework": "hardhat",
      "testing": "foundry",
      "security": "slither"
    },
    "overrides": {
      "numeric_precision": "use_bignumber",
      "async_patterns": "web3_specific",
      "error_handling": "revert_patterns"
    }
  }
}
```

### Example 5: High-Performance Computing

```json
{
  "name": "hpc-simulation",
  "extends": "github:raibid-labs/claude-org-config/templates/repo-types/base-template.json",
  "hpc_customization": {
    "languages": ["c++", "cuda", "fortran"],
    "parallelization": {
      "mpi": true,
      "openmp": true,
      "cuda": true,
      "target_architecture": "A100"
    },
    "rules": [
      "./docs/HPC_OPTIMIZATION.md",
      "./docs/MEMORY_MANAGEMENT.md",
      "./docs/PARALLEL_PATTERNS.md"
    ],
    "context": {
      "kernels": "./src/kernels/",
      "benchmarks": "./benchmarks/",
      "configs": "./job_configs/",
      "results": "./results/"
    },
    "performance": {
      "profiling_tools": ["nvprof", "vtune", "perf"],
      "optimization_level": "O3",
      "vectorization": "AVX512"
    },
    "overrides": {
      "memory_management": "manual",
      "bounds_checking": "disabled_in_production",
      "floating_point": "fast_math"
    }
  }
}
```

---

## Best Practices

### 1. Document Everything

Always document your customizations:

```json
{
  "customization_docs": {
    "why": "This repo requires custom configuration because...",
    "what": "The following settings are overridden...",
    "impact": "This affects the following workflows...",
    "team_agreement": "Approved by @teamlead on 2024-01-15",
    "review_date": "2024-06-15"
  }
}
```

### 2. Version Your Customizations

Track configuration changes:

```json
{
  "config_version": "2.1.0",
  "changelog": [
    {
      "version": "2.1.0",
      "date": "2024-01-20",
      "changes": ["Added ML pipeline configuration"],
      "breaking": false
    },
    {
      "version": "2.0.0",
      "date": "2024-01-01",
      "changes": ["Migrated to new template system"],
      "breaking": true,
      "migration_guide": "./docs/MIGRATION_2.0.md"
    }
  ]
}
```

### 3. Test Your Customizations

Validate customizations work correctly:

```bash
#!/bin/bash
# test-customization.sh

echo "Testing Claude configuration customizations..."

# Test 1: Valid JSON
jq . .claude/project.json > /dev/null || exit 1

# Test 2: Inheritance works
EXTENDS=$(jq -r '.extends' .claude/project.json)
if [[ -z "$EXTENDS" ]]; then
  echo "Warning: No extends field found"
fi

# Test 3: Custom rules exist
jq -r '.rules.additional[]?, .rules.custom[]?' .claude/project.json | while read rule; do
  if [ ! -f "$rule" ]; then
    echo "Error: Rule file missing: $rule"
    exit 1
  fi
done

# Test 4: MCP servers are valid
jq -r '.mcp_servers.custom | keys[]' .claude/project.json | while read server; do
  echo "Validating MCP server: $server"
  # Add actual validation logic
done

echo "✅ All customization tests passed"
```

### 4. Maintain Backward Compatibility

Ensure changes don't break existing workflows:

```json
{
  "compatibility_layer": {
    "deprecated": {
      "old_setting": {
        "maps_to": "new_setting",
        "warning": "old_setting is deprecated, use new_setting",
        "remove_in": "3.0.0"
      }
    },
    "aliases": {
      "test": "test_command",
      "build": "build_command"
    }
  }
}
```

### 5. Use Feature Flags

Enable gradual rollout of customizations:

```json
{
  "feature_flags": {
    "new_ml_pipeline": {
      "enabled": false,
      "rollout_percentage": 25,
      "enabled_for_teams": ["ml-team"],
      "config_when_enabled": {
        "rules": ["./ml/NEW_PIPELINE.md"]
      }
    }
  }
}
```

---

## Troubleshooting

### Common Customization Issues

#### Issue: "Customization not taking effect"

**Diagnosis:**
```bash
# Check inheritance chain
claude-code --show-config-inheritance

# Verify override syntax
jq '.overrides' .claude/project.json
```

**Solution:**
```json
{
  "overrides": {
    "force": true,  // Force override
    "setting_name": "value"
  }
}
```

#### Issue: "Conflict between org and custom rules"

**Diagnosis:**
```bash
# List all active rules
claude-code --list-active-rules

# Check for conflicts
claude-code --check-rule-conflicts
```

**Solution:**
```json
{
  "conflict_resolution": {
    "strategy": "repo_wins",  // or "org_wins", "merge"
    "explicit_overrides": {
      "rule_name": "use_repo_version"
    }
  }
}
```

#### Issue: "MCP server not loading"

**Diagnosis:**
```bash
# Test MCP server directly
npx your-mcp-server test

# Check Claude logs
claude-code --debug --log-level=verbose
```

**Solution:**
```json
{
  "mcp_servers": {
    "problematic_server": {
      "command": "npx",
      "args": ["-y", "server-name", "--verbose"],
      "debug": true,
      "timeout": 30000,
      "retry_on_failure": true
    }
  }
}
```

#### Issue: "Template composition conflicts"

**Diagnosis:**
```bash
# Show composed configuration
claude-code --show-composed-config

# Identify conflicts
claude-code --analyze-template-conflicts
```

**Solution:**
```json
{
  "composition_strategy": {
    "conflict_resolution": {
      "field_name": "prefer_template_1",
      "another_field": "merge_both",
      "third_field": "custom_value"
    }
  }
}
```

### Debug Mode for Customizations

Enable detailed debugging:

```json
{
  "debug": {
    "customization": true,
    "show_inheritance": true,
    "show_overrides": true,
    "show_conflicts": true,
    "log_file": "./.claude-debug.log"
  }
}
```

### Getting Help with Customizations

1. **Check documentation:**
   ```bash
   # View customization examples
   open https://github.com/raibid-labs/claude-org-config/tree/main/examples
   ```

2. **Validate configuration:**
   ```bash
   # Run validation with detailed output
   curl -fsSL https://raw.githubusercontent.com/raibid-labs/claude-org-config/main/scripts/validate-customization.sh | bash
   ```

3. **Get support:**
   ```bash
   # Open an issue with configuration details
   gh issue create \
     --repo raibid-labs/claude-org-config \
     --label "customization-help" \
     --title "Help with [specific customization]"
   ```

---

## Summary

Customization allows you to:
- Adapt org configuration to specific repo needs
- Add specialized tools and servers
- Override defaults when necessary
- Maintain consistency while allowing flexibility

Remember:
1. Document all customizations
2. Test thoroughly before deployment
3. Maintain backward compatibility
4. Use version control for configuration
5. Share successful patterns with the team

For more information:
- [SETUP.md](./SETUP.md) - Initial setup guide
- [MIGRATION.md](./MIGRATION.md) - Migration guide
- [Organization Config Repository](https://github.com/raibid-labs/claude-org-config)
- [Template Library](https://github.com/raibid-labs/claude-org-config/tree/main/templates)