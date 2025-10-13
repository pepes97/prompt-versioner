# Database Schema

Database schema definitions and table structures for the Prompt Versioner SQLite database.

## Overview

The database schema defines the structure for storing prompts, versions, metrics, annotations, and related data. The schema uses SQLite with foreign key constraints and optimized indexes for performance.

## Schema Module

### Schema Definitions

```python
from prompt_versioner.storage.schema import SCHEMA_DEFINITIONS, INDEXES, SCHEMA_VERSION
```

The schema module provides:
- **Table Definitions**: DDL statements for all database tables
- **Index Definitions**: Performance-optimized indexes
- **Schema Versioning**: Migration support through version tracking

## Database Tables

### prompt_versions

Main table storing prompt versions and their content.

```sql
CREATE TABLE IF NOT EXISTS prompt_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    version TEXT NOT NULL,
    system_prompt TEXT NOT NULL,
    user_prompt TEXT NOT NULL,
    metadata TEXT,
    git_commit TEXT,
    timestamp TEXT NOT NULL,
    created_by TEXT,
    tags TEXT,
    UNIQUE(name, version)
)
```

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique prompt version ID |
| `name` | TEXT | NOT NULL | Prompt name identifier |
| `version` | TEXT | NOT NULL | Semantic version (e.g., "1.2.0") |
| `system_prompt` | TEXT | NOT NULL | System prompt content |
| `user_prompt` | TEXT | NOT NULL | User prompt template |
| `metadata` | TEXT | - | JSON metadata (optional) |
| `git_commit` | TEXT | - | Git commit hash (optional) |
| `timestamp` | TEXT | NOT NULL | ISO timestamp of creation |
| `created_by` | TEXT | - | Author identifier (optional) |
| `tags` | TEXT | - | Comma-separated tags (deprecated, use version_tags) |

**Constraints:**
- `UNIQUE(name, version)`: Prevents duplicate versions for same prompt

**Example Data:**
```sql
INSERT INTO prompt_versions (
    name, version, system_prompt, user_prompt, metadata, timestamp
) VALUES (
    'code_reviewer',
    '1.2.0',
    'You are an expert code reviewer.',
    'Review this code: {code}',
    '{"author": "john.doe", "purpose": "code review"}',
    '2025-01-15T10:30:00Z'
);
```

### prompt_metrics

Performance metrics and usage data for prompt versions.

```sql
CREATE TABLE IF NOT EXISTS prompt_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version_id INTEGER NOT NULL,
    model_name TEXT,
    input_tokens INTEGER,
    output_tokens INTEGER,
    total_tokens INTEGER,
    cost_eur REAL,
    latency_ms REAL,
    quality_score REAL,
    accuracy REAL,
    temperature REAL,
    top_p REAL,
    max_tokens INTEGER,
    success BOOLEAN,
    error_message TEXT,
    timestamp TEXT NOT NULL,
    metadata TEXT,
    FOREIGN KEY (version_id) REFERENCES prompt_versions(id) ON DELETE CASCADE
)
```

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique metric record ID |
| `version_id` | INTEGER | NOT NULL, FK | Reference to prompt_versions.id |
| `model_name` | TEXT | - | AI model used (e.g., "gpt-4o") |
| `input_tokens` | INTEGER | - | Number of input tokens |
| `output_tokens` | INTEGER | - | Number of output tokens |
| `total_tokens` | INTEGER | - | Total tokens (calculated) |
| `cost_eur` | REAL | - | Cost in euros |
| `latency_ms` | REAL | - | Response latency in milliseconds |
| `quality_score` | REAL | - | Quality assessment (0-1) |
| `accuracy` | REAL | - | Accuracy measurement (0-1) |
| `temperature` | REAL | - | Model temperature parameter |
| `top_p` | REAL | - | Model top_p parameter |
| `max_tokens` | INTEGER | - | Model max_tokens parameter |
| `success` | BOOLEAN | - | Whether request succeeded |
| `error_message` | TEXT | - | Error details if failed |
| `timestamp` | TEXT | NOT NULL | ISO timestamp of metric collection |
| `metadata` | TEXT | - | Additional JSON metadata |

**Relationships:**
- `FOREIGN KEY (version_id) REFERENCES prompt_versions(id) ON DELETE CASCADE`

**Example Data:**
```sql
INSERT INTO prompt_metrics (
    version_id, model_name, input_tokens, output_tokens,
    cost_eur, latency_ms, quality_score, success, timestamp
) VALUES (
    1, 'gpt-4o-mini', 150, 200, 0.004, 1250.5, 0.87, 1, '2025-01-15T10:35:00Z'
);
```

### annotations

Team annotations and comments on prompt versions.

```sql
CREATE TABLE IF NOT EXISTS annotations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version_id INTEGER NOT NULL,
    author TEXT NOT NULL,
    text TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    annotation_type TEXT DEFAULT 'comment',
    resolved BOOLEAN DEFAULT 0,
    FOREIGN KEY (version_id) REFERENCES prompt_versions(id) ON DELETE CASCADE
)
```

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique annotation ID |
| `version_id` | INTEGER | NOT NULL, FK | Reference to prompt_versions.id |
| `author` | TEXT | NOT NULL | Annotation author |
| `text` | TEXT | NOT NULL | Annotation content |
| `timestamp` | TEXT | NOT NULL | ISO timestamp of creation |
| `annotation_type` | TEXT | DEFAULT 'comment' | Type: comment, review, approval |
| `resolved` | BOOLEAN | DEFAULT 0 | Whether annotation is resolved |

**Annotation Types:**
- `comment`: General comment or note
- `review`: Code/prompt review feedback
- `approval`: Approval for production deployment
- `issue`: Issue or problem identification

**Example Data:**
```sql
INSERT INTO annotations (
    version_id, author, text, annotation_type, timestamp
) VALUES (
    1, 'team_lead', 'Approved for production deployment', 'approval', '2025-01-15T11:00:00Z'
);
```

### version_tags

Tag system for organizing and categorizing prompt versions.

```sql
CREATE TABLE IF NOT EXISTS version_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    version_id INTEGER NOT NULL,
    tag TEXT NOT NULL,
    FOREIGN KEY (version_id) REFERENCES prompt_versions(id) ON DELETE CASCADE,
    UNIQUE(version_id, tag)
)
```

**Columns:**

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique tag association ID |
| `version_id` | INTEGER | NOT NULL, FK | Reference to prompt_versions.id |
| `tag` | TEXT | NOT NULL | Tag name |

**Constraints:**
- `UNIQUE(version_id, tag)`: Prevents duplicate tags on same version

**Common Tags:**
- `production`: Production-ready versions
- `experimental`: Experimental versions
- `deprecated`: Deprecated versions
- `stable`: Stable releases
- `hotfix`: Emergency fixes

**Example Data:**
```sql
INSERT INTO version_tags (version_id, tag) VALUES
    (1, 'production'),
    (1, 'stable'),
    (2, 'experimental');
```

## Database Indexes

Performance-optimized indexes for common query patterns:

```python
INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_name_version ON prompt_versions(name, version)",
    "CREATE INDEX IF NOT EXISTS idx_timestamp ON prompt_versions(timestamp DESC)",
    "CREATE INDEX IF NOT EXISTS idx_name ON prompt_versions(name)",
    "CREATE INDEX IF NOT EXISTS idx_metrics_version ON prompt_metrics(version_id)",
    "CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON prompt_metrics(timestamp DESC)",
    "CREATE INDEX IF NOT EXISTS idx_annotations_version ON annotations(version_id)",
    "CREATE INDEX IF NOT EXISTS idx_tags_version ON version_tags(version_id)",
    "CREATE INDEX IF NOT EXISTS idx_tags_tag ON version_tags(tag)",
]
```

### Index Purpose

| Index | Purpose | Query Optimization |
|-------|---------|-------------------|
| `idx_name_version` | Composite index | Fast lookup by name + version |
| `idx_timestamp` | Temporal ordering | Recent versions first |
| `idx_name` | Name-based queries | List versions by prompt name |
| `idx_metrics_version` | Metrics lookup | Get metrics for specific version |
| `idx_metrics_timestamp` | Temporal metrics | Recent metrics analysis |
| `idx_annotations_version` | Annotation lookup | Get annotations for version |
| `idx_tags_version` | Tag queries | Find tags for version |
| `idx_tags_tag` | Tag filtering | Find versions with specific tag |

### Query Performance Examples

```sql
-- ✅ Optimized: Uses idx_name_version
SELECT * FROM prompt_versions WHERE name = 'code_reviewer' AND version = '1.2.0';

-- ✅ Optimized: Uses idx_timestamp
SELECT * FROM prompt_versions ORDER BY timestamp DESC LIMIT 10;

-- ✅ Optimized: Uses idx_metrics_version
SELECT AVG(quality_score) FROM prompt_metrics WHERE version_id = 1;

-- ✅ Optimized: Uses idx_tags_tag
SELECT pv.* FROM prompt_versions pv
JOIN version_tags vt ON pv.id = vt.version_id
WHERE vt.tag = 'production';
```

## Schema Versioning

### Current Schema Version

```python
SCHEMA_VERSION = 1
```

The schema version enables database migrations and compatibility checking:

```python
def check_schema_version(db):
    """Check if database schema matches current version."""
    current_version = get_user_version(db)
    if current_version != SCHEMA_VERSION:
        raise SchemaVersionMismatch(
            f"Database schema v{current_version} != required v{SCHEMA_VERSION}"
        )
```

### Migration Support

Future schema changes will increment `SCHEMA_VERSION` and provide migration scripts:

```python
# Future migration example
MIGRATIONS = {
    1: [
        "ALTER TABLE prompt_versions ADD COLUMN new_field TEXT",
        "CREATE INDEX idx_new_field ON prompt_versions(new_field)"
    ],
    2: [
        "CREATE TABLE new_table (...)",
        "INSERT INTO new_table SELECT ... FROM old_table"
    ]
}
```

## Relationships and Constraints

### Entity Relationship Diagram

```
prompt_versions (1) ──── (N) prompt_metrics
       │
       │ (1)
       │
       └── (N) annotations
       │
       │ (1)
       │
       └── (N) version_tags
```

### Foreign Key Behavior

All foreign keys use `ON DELETE CASCADE` for automatic cleanup:

```sql
-- When a prompt version is deleted:
DELETE FROM prompt_versions WHERE id = 1;

-- Automatically deletes:
-- - All metrics for that version
-- - All annotations for that version
-- - All tags for that version
```

### Data Integrity Rules

1. **Unique Versions**: Each prompt can have only one version with a given number
2. **Required Fields**: Core fields (name, version, prompts, timestamp) are mandatory
3. **Referential Integrity**: Metrics, annotations, and tags must reference valid versions
4. **Cascade Deletion**: Related data is automatically cleaned up

## Usage Examples

### Creating Tables

```python
from prompt_versioner.storage.database import DatabaseManager
from prompt_versioner.storage.schema import SCHEMA_DEFINITIONS, INDEXES

db = DatabaseManager()

# Tables are created automatically during initialization
# But you can create manually if needed:
with db.get_connection() as conn:
    for table_name, table_sql in SCHEMA_DEFINITIONS.items():
        conn.execute(table_sql)

    for index_sql in INDEXES:
        conn.execute(index_sql)
```

### Querying Related Data

```python
# Get version with all related data
def get_version_with_details(db, version_id):
    with db.get_connection() as conn:
        # Main version data
        version = conn.execute(
            "SELECT * FROM prompt_versions WHERE id = ?",
            (version_id,)
        ).fetchone()

        # Metrics summary
        metrics = conn.execute("""
            SELECT COUNT(*) as count, AVG(quality_score) as avg_quality,
                   AVG(latency_ms) as avg_latency, AVG(cost_eur) as avg_cost
            FROM prompt_metrics WHERE version_id = ?
        """, (version_id,)).fetchone()

        # Annotations
        annotations = conn.execute(
            "SELECT * FROM annotations WHERE version_id = ? ORDER BY timestamp",
            (version_id,)
        ).fetchall()

        # Tags
        tags = conn.execute(
            "SELECT tag FROM version_tags WHERE version_id = ?",
            (version_id,)
        ).fetchall()

        return {
            'version': dict(version),
            'metrics': dict(metrics),
            'annotations': [dict(a) for a in annotations],
            'tags': [t['tag'] for t in tags]
        }
```

### Complex Queries

```python
# Find best performing versions by tag
def get_top_versions_by_tag(db, tag, limit=10):
    query = """
        SELECT pv.name, pv.version, AVG(pm.quality_score) as avg_quality
        FROM prompt_versions pv
        JOIN version_tags vt ON pv.id = vt.version_id
        JOIN prompt_metrics pm ON pv.id = pm.version_id
        WHERE vt.tag = ? AND pm.quality_score IS NOT NULL
        GROUP BY pv.id
        ORDER BY avg_quality DESC
        LIMIT ?
    """
    return db.execute(query, (tag, limit), fetch="all")
```

## See Also

- [`DatabaseManager`](database.md) - Database connection and operations
- [`Queries`](queries.md) - Pre-built query functions
- [SQLite Foreign Keys](https://www.sqlite.org/foreignkeys.html) - Foreign key documentation
- [SQLite Indexes](https://www.sqlite.org/optoverview.html) - Index optimization guide
