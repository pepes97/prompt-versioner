"""Storage module for prompt versions using SQLite."""

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import json
import sqlite3
from contextlib import contextmanager


class PromptStorage:
    """Handles persistent storage of prompt versions."""

    def __init__(self, db_path: Optional[Path] = None):
        """Initialize storage with SQLite database.

        Args:
            db_path: Path to SQLite database file. Defaults to .prompt_versions/db.sqlite
        """
        if db_path is None:
            db_path = Path.cwd() / ".prompt_versions" / "db.sqlite"

        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    @contextmanager
    def _get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self) -> None:
        """Initialize database schema."""
        with self._get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS prompt_versions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    version TEXT NOT NULL,
                    system_prompt TEXT NOT NULL,
                    user_prompt TEXT NOT NULL,
                    metadata TEXT,
                    git_commit TEXT,
                    timestamp TEXT NOT NULL,
                    UNIQUE(name, version)
                )
            """
            )

            conn.execute(
                """
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
                    FOREIGN KEY (version_id) REFERENCES prompt_versions(id)
                )
            """
            )

            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_name_version 
                ON prompt_versions(name, version)
            """
            )

            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_timestamp 
                ON prompt_versions(timestamp DESC)
            """
            )

            # New annotations table
            conn.execute(
                """
            CREATE TABLE IF NOT EXISTS annotations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                version_id INTEGER NOT NULL,
                author TEXT NOT NULL,
                text TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (version_id) REFERENCES prompt_versions(id)
            )
            """
            )

            conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_annotations_version 
                ON annotations(version_id)
            """
            )

    def save_version(
        self,
        name: str,
        version: str,
        system_prompt: str,
        user_prompt: str,
        metadata: Optional[Dict[str, Any]] = None,
        git_commit: Optional[str] = None,
    ) -> int:
        """Save a new prompt version.

        Args:
            name: Name/identifier for the prompt
            version: Version string (e.g., "v1.0.0", "main-abc123")
            system_prompt: System prompt content
            user_prompt: User prompt content
            metadata: Additional metadata as dict
            git_commit: Git commit hash

        Returns:
            ID of the saved version
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        metadata_json = json.dumps(metadata) if metadata else None

        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO prompt_versions 
                (name, version, system_prompt, user_prompt, metadata, git_commit, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (name, version, system_prompt, user_prompt, metadata_json, git_commit, timestamp),
            )
            return cursor.lastrowid

    def get_version(self, name: str, version: str) -> Optional[Dict[str, Any]]:
        """Get a specific prompt version.

        Args:
            name: Prompt name
            version: Version string

        Returns:
            Dict with version data or None if not found
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT * FROM prompt_versions 
                WHERE name = ? AND version = ?
                """,
                (name, version),
            )
            row = cursor.fetchone()

            if row:
                return self._row_to_dict(row)
            return None

    def get_latest_version(self, name: str) -> Optional[Dict[str, Any]]:
        """Get the most recent version of a prompt.

        Args:
            name: Prompt name

        Returns:
            Dict with version data or None if not found
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT * FROM prompt_versions 
                WHERE name = ? 
                ORDER BY timestamp DESC 
                LIMIT 1
                """,
                (name,),
            )
            row = cursor.fetchone()

            if row:
                return self._row_to_dict(row)
            return None

    def list_versions(self, name: str) -> List[Dict[str, Any]]:
        """List all versions of a prompt.

        Args:
            name: Prompt name

        Returns:
            List of version dicts ordered by timestamp (newest first)
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT * FROM prompt_versions 
                WHERE name = ? 
                ORDER BY timestamp DESC
                """,
                (name,),
            )
            return [self._row_to_dict(row) for row in cursor.fetchall()]

    def list_all_prompts(self) -> List[str]:
        """List all unique prompt names.

        Returns:
            List of prompt names
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT DISTINCT name FROM prompt_versions 
                ORDER BY name
                """
            )
            return [row["name"] for row in cursor.fetchall()]

    def save_metrics(
        self,
        version_id: int,
        model_name: Optional[str] = None,
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None,
        total_tokens: Optional[int] = None,
        cost_eur: Optional[float] = None,
        latency_ms: Optional[float] = None,
        quality_score: Optional[float] = None,
        accuracy: Optional[float] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        success: bool = True,
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Save metrics for a prompt version.

        Args:
            version_id: ID of the prompt version
            model_name: Name of the LLM model used
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            total_tokens: Total tokens (input + output)
            cost_eur: Cost in USD
            latency_ms: Response latency in milliseconds
            quality_score: Quality score (0-1)
            accuracy: Accuracy score (0-1)
            temperature: Model temperature parameter
            top_p: Model top_p parameter
            max_tokens: Max tokens parameter
            success: Whether the call succeeded
            error_message: Error message if failed
            metadata: Additional metadata
        """
        timestamp = datetime.utcnow().isoformat()
        metadata_json = json.dumps(metadata) if metadata else None

        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO prompt_metrics 
                (version_id, model_name, input_tokens, output_tokens, total_tokens,
                 cost_eur, latency_ms, quality_score, accuracy, temperature, top_p,
                 max_tokens, success, error_message, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    version_id,
                    model_name,
                    input_tokens,
                    output_tokens,
                    total_tokens,
                    cost_eur,
                    latency_ms,
                    quality_score,
                    accuracy,
                    temperature,
                    top_p,
                    max_tokens,
                    success,
                    error_message,
                    timestamp,
                    metadata_json,
                ),
            )

    def get_metrics(self, version_id: int) -> List[Dict[str, Any]]:
        """Get all metrics for a version.

        Args:
            version_id: ID of the prompt version

        Returns:
            List of metric dicts
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT * FROM prompt_metrics 
                WHERE version_id = ?
                ORDER BY timestamp DESC
                """,
                (version_id,),
            )

            metrics = []
            for row in cursor.fetchall():
                metric = dict(row)
                if metric.get("metadata"):
                    metric["metadata"] = json.loads(metric["metadata"])
                metrics.append(metric)

            return metrics

    def get_metrics_summary(self, version_id: int) -> Dict[str, Any]:
        """Get summary statistics of metrics for a version.

        Args:
            version_id: ID of the prompt version

        Returns:
            Dict with summary statistics
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT 
                    COUNT(*) as call_count,
                    AVG(input_tokens) as avg_input_tokens,
                    AVG(output_tokens) as avg_output_tokens,
                    AVG(total_tokens) as avg_total_tokens,
                    SUM(total_tokens) as total_tokens_used,
                    AVG(cost_eur) as avg_cost,
                    SUM(cost_eur) as total_cost,
                    AVG(latency_ms) as avg_latency,
                    MIN(latency_ms) as min_latency,
                    MAX(latency_ms) as max_latency,
                    AVG(quality_score) as avg_quality,
                    AVG(accuracy) as avg_accuracy,
                    SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as success_count,
                    SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as error_count
                FROM prompt_metrics 
                WHERE version_id = ?
                """,
                (version_id,),
            )

            row = cursor.fetchone()
            if row:
                summary = dict(row)
                summary["success_rate"] = (
                    summary["success_count"] / summary["call_count"]
                    if summary["call_count"] > 0
                    else 0
                )
                return summary
            return {}

    def delete_version(self, name: str, version: str) -> bool:
        """Delete a specific version.

        Args:
            name: Prompt name
            version: Version string

        Returns:
            True if deleted, False if not found
        """
        with self._get_connection() as conn:
            # First get the version_id
            cursor = conn.execute(
                "SELECT id FROM prompt_versions WHERE name = ? AND version = ?",
                (name, version),
            )
            row = cursor.fetchone()

            if not row:
                return False

            version_id = row["id"]

            # Delete metrics
            conn.execute("DELETE FROM prompt_metrics WHERE version_id = ?", (version_id,))

            # Delete version
            conn.execute(
                "DELETE FROM prompt_versions WHERE id = ?",
                (version_id,),
            )

            return True

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
        """Convert SQLite row to dict.

        Args:
            row: SQLite row object

        Returns:
            Dict representation
        """
        data = dict(row)
        if data.get("metadata"):
            data["metadata"] = json.loads(data["metadata"])
        return data

    def add_annotation(self, version_id: int, author: str, text: str) -> int:
        """Add annotation to a version.

        Args:
            version_id: Version ID
            author: Author name/email
            text: Annotation text

        Returns:
            Annotation ID
        """
        timestamp = datetime.utcnow().isoformat()

        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO annotations (version_id, author, text, timestamp)
                VALUES (?, ?, ?, ?)
                """,
                (version_id, author, text, timestamp),
            )
            return cursor.lastrowid

    def get_annotations(self, version_id: int) -> List[Dict[str, Any]]:
        """Get all annotations for a version.

        Args:
            version_id: Version ID

        Returns:
            List of annotations
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT * FROM annotations
                WHERE version_id = ?
                ORDER BY timestamp DESC
                """,
                (version_id,),
            )
            return [dict(row) for row in cursor.fetchall()]
