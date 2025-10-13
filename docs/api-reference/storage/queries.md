
# Queries

The `prompt_versioner.storage.queries` module provides utilities for safe SQL query construction and common predefined queries.

## QueryBuilder

A static class for safely building SQL queries with protection against SQL injection.

### Methods

#### validate_table_name()

```python
@staticmethod
    def _validate_table_name(table_name: str) -> None
```

Validates a table name to prevent SQL injection.

**Parameters:**
- `table` (str): Name of the table to validate

**Raises:**
- `ValueError`: If the table name contains invalid characters

**Example:**
```python
QueryBuilder._validate_table_name("prompt_versions")  # OK
QueryBuilder._validate_table_name("invalid; DROP TABLE") # Raises ValueError
```

#### _validate_column_names()

```python
@staticmethod
    def _validate_column_names(columns: list[str]) -> None
```

Validates a list of column names to prevent SQL injection.

**Parameters:**
- `columns` (List[str]): List of column names to validate

**Raises:**
- `ValueError`: If any column name contains invalid characters

**Example:**
```python
QueryBuilder._validate_column_names(["id", "name", "version"])  # OK
QueryBuilder._validate_column_names(["id; DROP TABLE"])  # Raises ValueError
```

#### build_where_clause()

```python
@staticmethod
    def build_where_clause(conditions: Dict[str, Any]) -> tuple[str, List[Any]]
```

Builds a safe WHERE clause from a dictionary of conditions.

**Parameters:**
- `conditions` (Dict[str, Any]): Dictionary of conditions {column: value}

**Returns:**
- `tuple[str, List[Any]]`: Tuple containing (WHERE clause, parameters)

**Example:**
```python
conditions = {"name": "my_prompt", "version": "1.0.0"}
where_clause, params = QueryBuilder.build_where_clause(conditions)
# where_clause: "WHERE name = ? AND version = ?"
# params: ["my_prompt", "1.0.0"]
```

#### build_select()

```python
@staticmethod
def build_select(
        table: str,
        columns: list[str] | None = None,
        where: Dict[str, Any] | None = None,
        order_by: str | None = None,
        limit: int | None = None,
    ) -> tuple[str, List[Any]]
```

Builds a complete and safe SELECT query.

**Parameters:**
- `table` (str): Table name
- `columns` (List[str] | None): List of columns to select (None for *)
- `where` (Dict[str, Any] | None): WHERE conditions
- `order_by` (str | None): ORDER BY clause
- `limit` (int | None): Maximum number of results

**Returns:**
- `tuple[str, List[Any]]`: Tuple containing (SQL query, parameters)

**Example:**
```python
query, params = QueryBuilder.build_select(
    table="prompt_versions",
    columns=["id", "name", "version"],
    where={"name": "my_prompt"},
    order_by="timestamp DESC",
    limit=10
)
# query: "SELECT id, name, version FROM prompt_versions WHERE name = ? ORDER BY timestamp DESC LIMIT 10"
# params: ["my_prompt"]
```

## CommonQueries

A collection of predefined queries for common operations.

### Methods

#### get_version_stats()

```python
@staticmethod
    def get_version_stats(db_manager: DatabaseManager) -> Dict[str, Any]
```

Gets general statistics about versions.

**Parameters:**
- `db_manager` (DatabaseManager): Instance of DatabaseManager

**Returns:**
- `Dict[str, Any]`: Dictionary with statistics:
  - `total_versions`: Total number of versions
  - `total_prompts`: Total number of unique prompts
  - `total_metrics`: Total number of metrics
  - `total_annotations`: Total number of annotations

**Example:**
```python
from prompt_versioner.storage.database import DatabaseManager
from prompt_versioner.storage.queries import CommonQueries

db_manager = DatabaseManager("path/to/database.db")
stats = CommonQueries.get_version_stats(db_manager)
print(f"Total versions: {stats['total_versions']}")
print(f"Total prompts: {stats['total_prompts']}")
```

#### get_most_used_models()

```python
@staticmethod
    def get_most_used_models(db_manager: DatabaseManager, limit: int = 10) -> List[Dict[str, Any]]
```

Gets the most used models with usage statistics.

**Parameters:**
- `db_manager` (DatabaseManager): Instance of DatabaseManager
- `limit` (int): Maximum number of results (default: 10)

**Returns:**
- `List[Dict[str, Any]]`: List of dictionaries with statistics per model:
  - `model_name`: Model name
  - `usage_count`: Number of uses
  - `avg_cost`: Average cost in EUR
  - `avg_latency`: Average latency in ms

**Example:**
```python
models = CommonQueries.get_most_used_models(db_manager, limit=5)
for model in models:
    print(f"{model['model_name']}: {model['usage_count']} uses, "
          f"avg cost: €{model['avg_cost']:.4f}")
```

#### get_recent_activity()

```python
@staticmethod
    def get_recent_activity(db_manager: DatabaseManager, days: int = 7) -> List[Dict[str, Any]]
```

Gets recent version activity.

**Parameters:**
- `db_manager` (DatabaseManager): Instance of DatabaseManager
- `days` (int): Number of days to consider (default: 7)

**Returns:**
- `List[Dict[str, Any]]`: List of recent versions ordered by descending timestamp

**Example:**
```python
recent_versions = CommonQueries.get_recent_activity(db_manager, days=3)
for version in recent_versions:
    print(f"{version['name']} v{version['version']} - {version['timestamp']}")
```

## Usage with DatabaseManager

Queries built with `QueryBuilder` are designed to be used with `DatabaseManager`:

```python
from prompt_versioner.storage.database import DatabaseManager
from prompt_versioner.storage.queries import QueryBuilder, CommonQueries

# Initialize database manager
db_manager = DatabaseManager("path/to/database.db")

# Build custom query
query, params = QueryBuilder.build_select(
    table="prompt_versions",
    where={"name": "my_prompt"},
    order_by="timestamp DESC"
)

# Execute query
results = db_manager.execute(query, params, fetch="all")

# Or use predefined queries
stats = CommonQueries.get_version_stats(db_manager)
```

## See Also

- [`DatabaseManager`](database.md) - Database connection and operations
- [`Queries`](queries.md) - Pre-built query functions
- [SQLite Foreign Keys](https://www.sqlite.org/foreignkeys.html) - Foreign key documentation
- [SQLite Indexes](https://www.sqlite.org/optoverview.html) - Index optimization guide
