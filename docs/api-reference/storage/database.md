# Database Manager

The `DatabaseManager` class handles SQLite database connections and operations for the Prompt Versioner storage layer.

## Overview

The Database Manager provides:
- SQLite database connection management with context managers
- Automatic schema initialization and migration
- Connection pooling and transaction management
- Database utility operations (backup, vacuum, statistics)
- SQL injection protection through input validation

## Class Reference

### DatabaseManager

```python
from prompt_versioner.storage.database import DatabaseManager
```

The main database management class that handles all low-level database operations.

**Constructor:**
```python
def __init__(self, db_path: Optional[Path] = None)
```

**Parameters:**
- `db_path` (Optional[Path]): Path to SQLite database file. Defaults to `.prompt_versions/db.sqlite`

**Example:**
```python
from pathlib import Path
from prompt_versioner.storage.database import DatabaseManager

# Default location
db = DatabaseManager()  # Creates .prompt_versions/db.sqlite

# Custom location
db = DatabaseManager(Path("/opt/prompts/database.db"))

# In-memory database (for testing)
db = DatabaseManager(Path(":memory:"))
```

## Connection Management

### get_connection()

```python
@contextmanager
def get_connection(self) -> Generator[sqlite3.Connection, None, None]
```

Context manager for database connections with automatic transaction handling.

**Returns:**
- `Generator[sqlite3.Connection, None, None]`: Database connection context manager

**Features:**
- Automatic transaction commit on success
- Automatic rollback on exceptions
- Proper connection cleanup
- Row factory set to `sqlite3.Row` for dict-like access

**Example:**
```python
# Safe database operations with automatic cleanup
with db.get_connection() as conn:
    cursor = conn.execute("SELECT * FROM prompts WHERE name = ?", ("my_prompt",))
    result = cursor.fetchone()

    # Automatic commit on successful completion
    # Automatic rollback if exception occurs
```

**Transaction Behavior:**
```python
try:
    with db.get_connection() as conn:
        # Multiple operations in single transaction
        conn.execute("INSERT INTO prompts (name, system_prompt) VALUES (?, ?)",
                    ("prompt1", "System prompt 1"))
        conn.execute("INSERT INTO prompts (name, system_prompt) VALUES (?, ?)",
                    ("prompt2", "System prompt 2"))
        # Both inserts committed together
except Exception as e:
    # Both inserts rolled back on any error
    print(f"Transaction failed: {e}")
```

## Query Execution

### execute()

```python
def execute(
    self,
    query: str,
    params: tuple = (),
    fetch: str | None = None
) -> Any
```

Execute a single SQL query with optional result fetching.

**Parameters:**
- `query` (str): SQL query string
- `params` (tuple): Query parameters for safe parameter binding
- `fetch` (str | None): Result fetch mode - 'one', 'all', or None

**Returns:**
- `Any`: Query results based on fetch parameter
  - `'one'`: Returns single row or None
  - `'all'`: Returns list of all rows
  - `None`: Returns cursor for manual fetching

**Example:**
```python
# Insert with no result
db.execute(
    "INSERT INTO prompts (name, system_prompt) VALUES (?, ?)",
    ("my_prompt", "You are a helpful assistant.")
)

# Fetch single result
prompt = db.execute(
    "SELECT * FROM prompts WHERE name = ?",
    ("my_prompt",),
    fetch="one"
)

# Fetch all results
all_prompts = db.execute(
    "SELECT name, version FROM prompts ORDER BY created_at DESC",
    fetch="all"
)

# Manual cursor handling
cursor = db.execute("SELECT COUNT(*) FROM prompts")
count = cursor.fetchone()[0]
```

### execute_many()

```python
def execute_many(self, query: str, params_list: List[tuple]) -> None
```

Execute a query multiple times with different parameter sets (bulk operations).

**Parameters:**
- `query` (str): SQL query string
- `params_list` (List[tuple]): List of parameter tuples

**Example:**
```python
# Bulk insert multiple prompts
prompts_data = [
    ("prompt1", "System prompt 1", "User prompt 1"),
    ("prompt2", "System prompt 2", "User prompt 2"),
    ("prompt3", "System prompt 3", "User prompt 3"),
]

db.execute_many(
    "INSERT INTO prompts (name, system_prompt, user_prompt) VALUES (?, ?, ?)",
    prompts_data
)

# Bulk metrics insertion
metrics_data = [
    ("prompt1", "1.0.0", 0.85, 1200),
    ("prompt1", "1.0.0", 0.87, 1150),
    ("prompt1", "1.0.0", 0.86, 1300),
]

db.execute_many(
    "INSERT INTO metrics (prompt_name, version, quality_score, latency_ms) VALUES (?, ?, ?, ?)",
    metrics_data
)
```

## Database Introspection

### get_table_info()

```python
def get_table_info(self, table_name: str) -> List[Dict[str, Any]]
```

Get detailed information about a database table's schema.

**Parameters:**
- `table_name` (str): Name of the table to inspect

**Returns:**
- `List[Dict[str, Any]]`: List of column information dictionaries

**Column Information:**
- `cid`: Column ID
- `name`: Column name
- `type`: SQL data type
- `notnull`: Whether column is NOT NULL (1 or 0)
- `dflt_value`: Default value
- `pk`: Whether column is primary key (1 or 0)

**Example:**
```python
# Get table schema information
table_info = db.get_table_info("prompts")

for column in table_info:
    print(f"Column: {column['name']}")
    print(f"  Type: {column['type']}")
    print(f"  Not Null: {bool(column['notnull'])}")
    print(f"  Primary Key: {bool(column['pk'])}")
    print(f"  Default: {column['dflt_value']}")
```

**Output:**
```
Column: id
  Type: INTEGER
  Not Null: True
  Primary Key: True
  Default: None

Column: name
  Type: TEXT
  Not Null: True
  Primary Key: False
  Default: None

Column: system_prompt
  Type: TEXT
  Not Null: True
  Primary Key: False
  Default: None
```

### get_tables()

```python
def get_tables(self) -> List[str]
```

Get list of all tables in the database.

**Returns:**
- `List[str]`: List of table names sorted alphabetically

**Example:**
```python
tables = db.get_tables()
print("Database tables:", tables)
# Output: ['annotations', 'metrics', 'prompts', 'versions']

# Check if specific table exists
if "prompts" in db.get_tables():
    print("Prompts table exists")
```

## Database Maintenance

### vacuum()

```python
def vacuum(self) -> None
```

Vacuum the database to reclaim space and optimize performance.

**Side Effects:**
- Rebuilds database file to remove unused space
- Updates internal statistics for query optimization
- May take time for large databases

**Example:**
```python
# Regular maintenance
db.vacuum()
print("Database vacuumed and optimized")

# Check size before and after
size_before = db.get_db_size()
db.vacuum()
size_after = db.get_db_size()
print(f"Reclaimed {size_before - size_after} bytes")
```

### get_db_size()

```python
def get_db_size(self) -> int
```

Get the current database file size in bytes.

**Returns:**
- `int`: Size in bytes, or 0 if database file doesn't exist

**Example:**
```python
size_bytes = db.get_db_size()
size_mb = size_bytes / (1024 * 1024)
print(f"Database size: {size_mb:.2f} MB")

# Monitor growth
def monitor_db_growth():
    sizes = []
    for i in range(10):
        # ... perform operations ...
        sizes.append(db.get_db_size())

    growth = sizes[-1] - sizes[0]
    print(f"Database grew by {growth} bytes")
```

### backup()

```python
def backup(self, backup_path: Path) -> None
```

Create a backup of the database to another file.

**Parameters:**
- `backup_path` (Path): Path for the backup file

**Features:**
- Creates parent directories if they don't exist
- Uses SQLite's built-in backup API for consistent backups
- Can backup while database is in use

**Example:**
```python
from pathlib import Path
from datetime import datetime

# Daily backup
backup_dir = Path("/backups/prompts")
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = backup_dir / f"prompts_backup_{timestamp}.db"

db.backup(backup_file)
print(f"Backup created: {backup_file}")

# Automated backup function
def create_backup():
    backup_path = Path(f"backups/prompts_{datetime.now().isoformat()}.db")
    db.backup(backup_path)
    return backup_path
```

## Database Statistics

### get_stats()

```python
def get_stats(self) -> Dict[str, Any]
```

Get comprehensive database statistics and information.

**Returns:**
- `Dict[str, Any]`: Dictionary containing database statistics

**Statistics Included:**
- `db_path`: Database file path
- `db_size_bytes`: Database file size in bytes
- `tables`: Dictionary mapping table names to row counts

**Example:**
```python
stats = db.get_stats()

print(f"Database: {stats['db_path']}")
print(f"Size: {stats['db_size_bytes']} bytes")
print("\nTable Row Counts:")
for table, count in stats['tables'].items():
    print(f"  {table}: {count:,} rows")
```

**Output:**
```
Database: /path/to/prompts.db
Size: 2,048,576 bytes

Table Row Counts:
  annotations: 15 rows
  metrics: 1,247 rows
  prompts: 8 rows
  versions: 23 rows
```

## Security Features

### SQL Injection Protection

The DatabaseManager includes automatic protection against SQL injection:

```python
def _validate_table_name(self, table_name: str) -> None:
    """Validate table name to prevent SQL injection."""
    if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", table_name):
        raise ValueError(f"Invalid table name: {table_name}")
```

**Safe Practices:**
```python
# ✅ Safe - uses parameterized queries
db.execute("SELECT * FROM prompts WHERE name = ?", ("user_input",))

# ✅ Safe - table name validated
table_info = db.get_table_info("prompts")  # Validates table name

# ❌ Unsafe - don't do this
# db.execute(f"SELECT * FROM prompts WHERE name = '{user_input}'")
```

## Integration PromptStorage

```python
from prompt_versioner.storage import PromptStorage

# Storage layer uses DatabaseManager internally
storage = PromptStorage()  # Creates DatabaseManager automatically

# Access underlying database if needed
db_stats = storage.db.get_stats()
print(f"Total prompts: {db_stats['tables']['prompts']}")
```

## See Also

- [`Schema`](schema.md) - Database schema definitions and indexes
- [`Queries`](queries.md) - Pre-built query functions
- [`SQLite Documentation`](https://www.sqlite.org/docs.html) - SQLite reference
