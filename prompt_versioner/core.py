"""Core PromptVersioner class - main interface for the library."""

from pathlib import Path
import re
import yaml
import json
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast, Literal
from functools import wraps
from prompt_versioner.storage import PromptStorage
from prompt_versioner.diff import DiffEngine, PromptDiff
from prompt_versioner.tracker import GitTracker, AutoTracker
from prompt_versioner.metrics import MetricsTracker

F = TypeVar("F", bound=Callable[..., Any])

from enum import Enum


class VersionBump(Enum):
    """Type of version bump following SemVer 2.0.0."""

    MAJOR = "major"  # Breaking changes (non retrocompatibile)
    MINOR = "minor"  # New features (retrocompatibile)
    PATCH = "patch"  # Bug fixes (retrocompatibile)


class PreReleaseLabel(Enum):
    """Pre-release labels for versioning."""

    SNAPSHOT = "SNAPSHOT"  # Development version
    MILESTONE = "M"  # Milestone version
    RC = "RC"  # Release Candidate
    STABLE = None  # Stable release (no label)


class PromptVersioner:
    """Main interface for prompt versioning system."""

    def __init__(
        self,
        project_name: str,
        db_path: Optional[Path] = None,
        enable_git: bool = True,
        auto_track: bool = False,
    ):
        """Initialize PromptVersioner.

        Args:
            project_name: Name of your project
            db_path: Optional custom database path
            enable_git: Enable Git integration
            auto_track: Enable automatic tracking on prompt changes
        """
        self.project_name = project_name
        self.storage = PromptStorage(db_path)

        # Git integration
        self.git_tracker: Optional[GitTracker] = None
        if enable_git:
            try:
                self.git_tracker = GitTracker()
            except RuntimeError:
                # Not in a Git repo, continue without Git features
                pass

        # Auto tracking
        self.auto_tracker = AutoTracker(self.storage, self.git_tracker)
        self.auto_track_enabled = auto_track

        # Metrics
        self.metrics_tracker = MetricsTracker()

    def track(
        self,
        name: str,
        auto_commit: bool = False,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Callable[[F], F]:
        """Decorator to track prompt functions.

        Args:
            name: Name/identifier for the prompt
            auto_commit: Automatically version on each call
            metadata: Additional metadata to store

        Returns:
            Decorated function

        Example:
            @pv.track(name="code_reviewer", auto_commit=True)
            def get_prompts(code: str):
                return {
                    "system": "You are a code reviewer...",
                    "user": f"Review: {code}"
                }
        """

        def decorator(func: F) -> F:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                result = func(*args, **kwargs)

                # Extract prompts from result
                if isinstance(result, dict):
                    system_prompt = result.get("system", "")
                    user_prompt = result.get("user", "")
                elif isinstance(result, tuple) and len(result) == 2:
                    system_prompt, user_prompt = result
                else:
                    raise ValueError(
                        "Tracked function must return dict with 'system' and 'user' keys, "
                        "or tuple of (system, user)"
                    )

                # Auto-version if enabled
                if auto_commit or self.auto_track_enabled:
                    self.auto_tracker.auto_version(
                        name=name,
                        system_prompt=system_prompt,
                        user_prompt=user_prompt,
                        metadata=metadata,
                    )

                return result

            return cast(F, wrapper)

        return decorator

    def save_version(
        self,
        name: str,
        system_prompt: str,
        user_prompt: str,
        version: Optional[str] = None,
        bump_type: Optional[VersionBump | str] = None,
        pre_label: Optional[PreReleaseLabel | str] = None,
        pre_number: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
        overwrite: bool = False,  
    ) -> int:
        """Manually save a prompt version following SemVer 2.0.0.

        Args:
            name: Name/identifier for the prompt
            system_prompt: System prompt content
            user_prompt: User prompt content
            version: Optional explicit version string (overrides bump_type)
            bump_type: Type of version bump (MAJOR/MINOR/PATCH or "major"/"minor"/"patch")
            pre_label: Pre-release label (SNAPSHOT/M/RC/STABLE or "snapshot"/"m"/"rc"/"stable")
            pre_number: Pre-release number (for M.X or RC.X)
            metadata: Additional metadata

        Returns:
            Version ID

        Examples:
            # Con enum (come prima)
            pv.save_version(
                name="my_prompt",
                system_prompt="...",
                user_prompt="...",
                bump_type=VersionBump.PATCH,
                pre_label=PreReleaseLabel.SNAPSHOT
            )

            # Con stringhe (nuovo)
            pv.save_version(
                name="my_prompt",
                system_prompt="...",
                user_prompt="...",
                bump_type="patch",
                pre_label="snapshot"
            )

            # Case insensitive
            pv.save_version(
                name="my_prompt",
                system_prompt="...",
                user_prompt="...",
                bump_type="MAJOR",
                pre_label="RC"
            )
        """
        parsed_bump = self._parse_bump_type(bump_type)
        parsed_label = self._parse_pre_label(pre_label)

        # Auto-generate version if not provided
        if version is None:
            if parsed_bump is not None:
                # Semantic versioning
                latest = self.get_latest(name)
                current_version = latest["version"] if latest else None
                version = self._calculate_next_version(
                    current_version, parsed_bump, parsed_label, pre_number
                )
                git_commit = self.git_tracker.get_current_commit() if self.git_tracker else None
            elif self.git_tracker:
                # Git-based versioning (fallback)
                version = self.git_tracker.get_version_string()
                git_commit = self.git_tracker.get_current_commit()
            else:
                # Hash-based versioning (fallback)
                from .tracker import PromptHasher

                version = PromptHasher.compute_hash(system_prompt, user_prompt)
                git_commit = None
        else:
            git_commit = self.git_tracker.get_current_commit() if self.git_tracker else None

        existing = self.get_version(name, version)
        if existing:
            if overwrite:
                # Delete existing version
                self.storage.delete_version(name, version)
                print(f"Overwriting existing version {version} for {name}")
            else:
                raise ValueError(
                    f"Version {version} already exists for prompt '{name}'. "
                    f"Use overwrite=True to replace it or use a different bump_type."
                )

        return self.storage.save_version(
            name=name,
            version=version,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            metadata=metadata,
            git_commit=git_commit,
        )

    def get_version(self, name: str, version: str) -> Optional[Dict[str, Any]]:
        """Get a specific prompt version.

        Args:
            name: Prompt name
            version: Version string

        Returns:
            Version data or None
        """
        return self.storage.get_version(name, version)

    def get_latest(self, name: str) -> Optional[Dict[str, Any]]:
        """Get the latest version of a prompt.

        Args:
            name: Prompt name

        Returns:
            Latest version data or None
        """
        return self.storage.get_latest_version(name)

    def list_versions(self, name: str) -> List[Dict[str, Any]]:
        """List all versions of a prompt.

        Args:
            name: Prompt name

        Returns:
            List of versions (newest first)
        """
        return self.storage.list_versions(name)

    def list_prompts(self) -> List[str]:
        """List all tracked prompt names.

        Returns:
            List of prompt names
        """
        return self.storage.list_all_prompts()

    def diff(
        self,
        name: str,
        version1: str,
        version2: str,
        format_output: bool = False,
    ) -> PromptDiff:
        """Compare two versions of a prompt.

        Args:
            name: Prompt name
            version1: First version
            version2: Second version
            format_output: If True, print formatted diff

        Returns:
            PromptDiff object
        """
        v1 = self.storage.get_version(name, version1)
        v2 = self.storage.get_version(name, version2)

        if not v1:
            raise ValueError(f"Version {version1} not found for prompt {name}")
        if not v2:
            raise ValueError(f"Version {version2} not found for prompt {name}")

        diff = DiffEngine.compute_diff(
            old_system=v1["system_prompt"],
            old_user=v1["user_prompt"],
            new_system=v2["system_prompt"],
            new_user=v2["user_prompt"],
        )

        if format_output:
            print(DiffEngine.format_diff_text(diff))

        return diff

    def rollback(self, name: str, to_version: str) -> int:
        """Rollback to a previous version (creates new version with old content).

        Args:
            name: Prompt name
            to_version: Version to rollback to

        Returns:
            New version ID
        """
        old_version = self.storage.get_version(name, to_version)

        if not old_version:
            raise ValueError(f"Version {to_version} not found for prompt {name}")

        # Create new version with old content
        return self.save_version(
            name=name,
            system_prompt=old_version["system_prompt"],
            user_prompt=old_version["user_prompt"],
            metadata={"rollback_from": to_version},
        )

    def compare_versions(
        self,
        name: str,
        versions: List[str],
    ) -> Dict[str, Any]:
        """Compare multiple versions with metrics.

        Args:
            name: Prompt name
            versions: List of version strings to compare

        Returns:
            Comparison data with metrics
        """
        comparison = {
            "versions": [],
            "metrics": {},
        }

        for version in versions:
            v = self.storage.get_version(name, version)
            if v:
                metrics = self.storage.get_metrics(v["id"])
                comparison["versions"].append(
                    {
                        "version": version,
                        "timestamp": v["timestamp"],
                        "git_commit": v.get("git_commit"),
                        "metrics": metrics,
                    }
                )

        return comparison

    def log_metrics(
        self,
        name: str,
        version: str,
        model_name: Optional[str] = None,
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None,
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
        """Log metrics for a specific version.

        Args:
            name: Prompt name
            version: Version string
            model_name: Name of the LLM model
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            cost_eur: Cost in USD (auto-calculated if not provided)
            latency_ms: Response latency in ms
            quality_score: Quality score (0-1)
            accuracy: Accuracy score (0-1)
            temperature: Model temperature
            top_p: Model top_p parameter
            max_tokens: Max tokens parameter
            success: Whether call succeeded
            error_message: Error message if failed
            metadata: Additional metadata
        """
        v = self.storage.get_version(name, version)
        if not v:
            raise ValueError(f"Version {version} not found for prompt {name}")

        # Auto-calculate cost if not provided
        if cost_eur is None and model_name and input_tokens and output_tokens:
            from prompt_versioner.metrics import MetricsCalculator

            cost_eur = MetricsCalculator.calculate_cost(model_name, input_tokens, output_tokens)

        # Calculate total tokens
        total_tokens = None
        if input_tokens is not None and output_tokens is not None:
            total_tokens = input_tokens + output_tokens

        self.storage.save_metrics(
            version_id=v["id"],
            model_name=model_name,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            cost_eur=cost_eur,
            latency_ms=latency_ms,
            quality_score=quality_score,
            accuracy=accuracy,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            success=success,
            error_message=error_message,
            metadata=metadata,
        )

    def test_version(
        self,
        name: str,
        version: str,
    ) -> "TestContext":
        """Context manager for testing a prompt version.

        Args:
            name: Prompt name
            version: Version string

        Returns:
            TestContext for logging metrics

        Example:
            with pv.test_version("my_prompt", "v1.0.0"):
                result = call_llm(prompt)
                pv.log_metrics(tokens=150, cost=0.002)
        """
        return TestContext(self, name, version)

    def install_git_hooks(self) -> None:
        """Install Git hooks for automatic versioning."""
        if not self.git_tracker:
            raise RuntimeError("Git integration not enabled")

        self.git_tracker.install_hooks()

    def uninstall_git_hooks(self) -> None:
        """Remove Git hooks."""
        if not self.git_tracker:
            raise RuntimeError("Git integration not enabled")

        self.git_tracker.uninstall_hooks()

    def _parse_bump_type(self, bump_type: VersionBump | str | None) -> Optional[VersionBump]:
        """Parse bump type from string or enum.

        Args:
            bump_type: VersionBump enum or string ("major", "minor", "patch")

        Returns:
            VersionBump enum or None

        Examples:
            >>> _parse_bump_type("patch")
            VersionBump.PATCH
            >>> _parse_bump_type("MAJOR")
            VersionBump.MAJOR
            >>> _parse_bump_type(VersionBump.MINOR)
            VersionBump.MINOR
        """
        if bump_type is None:
            return None

        if isinstance(bump_type, VersionBump):
            return bump_type

        if isinstance(bump_type, str):
            # Case insensitive mapping
            bump_map = {
                "major": VersionBump.MAJOR,
                "minor": VersionBump.MINOR,
                "patch": VersionBump.PATCH,
            }
            return bump_map.get(bump_type.lower())

        return None

    def _parse_pre_label(
        self, pre_label: PreReleaseLabel | str | None
    ) -> Optional[PreReleaseLabel]:
        """Parse pre-release label from string or enum.

        Args:
            pre_label: PreReleaseLabel enum or string

        Returns:
            PreReleaseLabel enum or None

        Examples:
            >>> _parse_pre_label("snapshot")
            PreReleaseLabel.SNAPSHOT
            >>> _parse_pre_label("RC")
            PreReleaseLabel.RC
            >>> _parse_pre_label("m")
            PreReleaseLabel.MILESTONE
        Returns:
            PreReleaseLabel enum or None

        Examples:
            >>> _parse_pre_label("snapshot")
            PreReleaseLabel.SNAPSHOT
            >>> _parse_pre_label("RC")
            PreReleaseLabel.RC
            >>> _parse_pre_label("m")
            PreReleaseLabel.MILESTONE
            >>> _parse_pre_label("stable")
            PreReleaseLabel.STABLE
        """
        if pre_label is None:
            return None

        if isinstance(pre_label, PreReleaseLabel):
            return pre_label

        if isinstance(pre_label, str):
            # Case insensitive mapping
            label_map = {
                "snapshot": PreReleaseLabel.SNAPSHOT,
                "milestone": PreReleaseLabel.MILESTONE,
                "m": PreReleaseLabel.MILESTONE,
                "rc": PreReleaseLabel.RC,
                "release_candidate": PreReleaseLabel.RC,
                "stable": PreReleaseLabel.STABLE,
                "": PreReleaseLabel.STABLE,  # Empty string = stable
            }
            return label_map.get(pre_label.lower())

        return None

    def _parse_version(self, version_string: str) -> dict:
        """Parse a semantic version string.

        Args:
            version_string: Version string (e.g., "1.2.3-RC.1")

        Returns:
            Dict with parsed components
        """
        # Pattern: MAJOR.MINOR.PATCH[-PRERELEASE]
        pattern = r"^(\d+)\.(\d+)\.(\d+)(?:-([A-Za-z]+)(?:\.(\d+))?)?$"
        match = re.match(pattern, version_string)

        if not match:
            return None

        major, minor, patch, pre_label, pre_number = match.groups()

        return {
            "major": int(major),
            "minor": int(minor),
            "patch": int(patch),
            "pre_label": pre_label,
            "pre_number": int(pre_number) if pre_number else None,
        }

    def _format_version(
        self,
        major: int,
        minor: int,
        patch: int,
        pre_label: Optional[PreReleaseLabel] = None,
        pre_number: Optional[int] = None,
    ) -> str:
        """Format version components into string.

        Args:
            major: Major version
            minor: Minor version
            patch: Patch version
            pre_label: Pre-release label (optional)
            pre_number: Pre-release number (optional)

        Returns:
            Formatted version string
        """
        base = f"{major}.{minor}.{patch}"

        if pre_label and pre_label != PreReleaseLabel.STABLE:
            if pre_number is not None:
                return f"{base}-{pre_label.value}.{pre_number}"
            else:
                return f"{base}-{pre_label.value}"

        return base

    def _calculate_next_version(
        self,
        current_version: Optional[str],
        bump_type: VersionBump,
        pre_label: Optional[PreReleaseLabel] = None,
        pre_number: Optional[int] = None,
    ) -> str:
        """Calculate next semantic version following SemVer 2.0.0.

        Args:
            current_version: Current version string (e.g., "1.2.3-RC.1") or None
            bump_type: Type of version bump (MAJOR, MINOR, PATCH)
            pre_label: Pre-release label (SNAPSHOT, M, RC, or STABLE)
            pre_number: Pre-release number (for M.X or RC.X)

        Returns:
            Next version string

        Examples:
            >>> _calculate_next_version(None, VersionBump.PATCH)
            "1.0.0"

            >>> _calculate_next_version("1.0.0", VersionBump.PATCH, PreReleaseLabel.SNAPSHOT)
            "1.0.1-SNAPSHOT"

            >>> _calculate_next_version("1.0.0", VersionBump.MINOR, PreReleaseLabel.MILESTONE, 1)
            "1.1.0-M.1"

            >>> _calculate_next_version("1.0.0-RC.1", VersionBump.PATCH, PreReleaseLabel.RC, 2)
            "1.0.0-RC.2"

            >>> _calculate_next_version("1.0.0-RC.2", VersionBump.PATCH, PreReleaseLabel.STABLE)
            "1.0.0"
        """
        # First version
        if current_version is None:
            major, minor, patch = 1, 0, 0
        else:
            # Parse current version
            parsed = self._parse_version(current_version)
            if not parsed:
                # Invalid format, start fresh
                major, minor, patch = 1, 0, 0
            else:
                major = parsed["major"]
                minor = parsed["minor"]
                patch = parsed["patch"]

                # If current is pre-release and new is stable with same version, keep numbers
                if (
                    pre_label == PreReleaseLabel.STABLE
                    and parsed["pre_label"] is not None
                    and bump_type == VersionBump.PATCH
                ):
                    # Releasing stable from pre-release, keep version
                    pass
                # Otherwise bump version
                elif bump_type == VersionBump.MAJOR:
                    major += 1
                    minor = 0
                    patch = 0
                elif bump_type == VersionBump.MINOR:
                    minor += 1
                    patch = 0
                elif bump_type == VersionBump.PATCH:
                    patch += 1

        return self._format_version(major, minor, patch, pre_label, pre_number)

    def export_prompt(
        self,
        name: str,
        output_file: Path,
        format: Literal["json", "yaml"] = "json",
        include_metrics: bool = True,
    ) -> None:
        """Export all versions of a prompt to file.

        Args:
            name: Prompt name to export
            output_file: Output file path
            format: Export format (json or yaml)
            include_metrics: Whether to include metrics data
        """
        versions = self.list_versions(name)

        if not versions:
            raise ValueError(f"No versions found for prompt '{name}'")

        export_data = {
            "prompt_name": name,
            "export_date": datetime.now(timezone.utc).isoformat(),
            "versions": [],
        }

        for v in versions:
            version_data = {
                "version": v["version"],
                "system_prompt": v["system_prompt"],
                "user_prompt": v["user_prompt"],
                "metadata": v.get("metadata"),
                "git_commit": v.get("git_commit"),
                "timestamp": v["timestamp"],
            }

            if include_metrics:
                metrics_summary = self.storage.get_metrics_summary(v["id"])
                metrics_list = self.storage.get_metrics(v["id"])
                version_data["metrics_summary"] = metrics_summary
                version_data["metrics_count"] = len(metrics_list)

            export_data["versions"].append(version_data)

        output_file.parent.mkdir(parents=True, exist_ok=True)

        if format == "json":
            output_file.write_text(json.dumps(export_data, indent=2, ensure_ascii=False))
        elif format == "yaml":

            output_file.write_text(yaml.dump(export_data, allow_unicode=True))

        print(f"Exported {len(versions)} versions of '{name}' to {output_file}")

    def import_prompt(
        self, input_file: Path, overwrite: bool = False, bump_type: Optional[VersionBump] = None
    ) -> dict:
        """Import prompt versions from file.

        Args:
            input_file: Input file path
            overwrite: If True, overwrite existing versions
            bump_type: If specified, renumber versions with semantic versioning

        Returns:
            Dict with import statistics
        """
        if not input_file.exists():
            raise FileNotFoundError(f"File not found: {input_file}")

        content = input_file.read_text()

        if input_file.suffix == ".json":
            import_data = json.loads(content)
        elif input_file.suffix in [".yaml", ".yml"]:
            import_data = yaml.safe_load(content)
        else:
            raise ValueError(f"Unsupported format: {input_file.suffix}")

        prompt_name = import_data["prompt_name"]
        versions = import_data["versions"]

        imported = 0
        skipped = 0

        for v in versions:
            # Check if version already exists
            existing = self.get_version(prompt_name, v["version"])

            if existing and not overwrite:
                skipped += 1
                continue

            # Import version
            version_str = v["version"]
            if bump_type:
                # Renumber with semantic versioning
                latest = self.get_latest(prompt_name)
                current_version = latest["version"] if latest else None
                version_str = self._calculate_next_version(current_version, bump_type)

            self.save_version(
                name=prompt_name,
                system_prompt=v["system_prompt"],
                user_prompt=v["user_prompt"],
                version=version_str,
                metadata=v.get("metadata"),
                overwrite=overwrite,
            )
            imported += 1

        result = {
            "prompt_name": prompt_name,
            "imported": imported,
            "skipped": skipped,
            "total": len(versions),
        }

        print(f"Import completed: {imported} imported, {skipped} skipped")

        return result

    def export_all(self, output_dir: Path, format: Literal["json", "yaml"] = "json") -> None:
        """Export all prompts to directory.

        Args:
            output_dir: Output directory
            format: Export format
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        prompts = self.list_prompts()

        for prompt_name in prompts:
            safe_name = prompt_name.replace("/", "_").replace("\\", "_")
            output_file = output_dir / f"{safe_name}.{format}"
            self.export_prompt(prompt_name, output_file, format)

        print(f"Exported {len(prompts)} prompts to {output_dir}")

    def add_annotation(self, name: str, version: str, text: str, author: str = "unknown") -> None:
        """Add annotation to a prompt version.

        Args:
            name: Prompt name
            version: Version string
            text: Annotation text
            author: Author name/email
        """
        v = self.get_version(name, version)
        if not v:
            raise ValueError(f"Version {version} not found for prompt {name}")

        self.storage.add_annotation(v["id"], author, text)
        print(f"Added annotation to {name} v{version} by {author}")

    def get_annotations(self, name: str, version: str) -> List[Dict[str, Any]]:
        """Get annotations for a version.

        Args:
            name: Prompt name
            version: Version string

        Returns:
            List of annotations
        """
        v = self.get_version(name, version)
        if not v:
            return []

        return self.storage.get_annotations(v["id"])
    
    
class TestContext:
    """Context manager for testing prompt versions."""

    def __init__(self, versioner: PromptVersioner, name: str, version: str):
        """Initialize test context.

        Args:
            versioner: PromptVersioner instance
            name: Prompt name
            version: Version string
        """
        self.versioner = versioner
        self.name = name
        self.version = version
        self.metrics: Dict[str, float] = {}

    def __enter__(self) -> "TestContext":
        """Enter context."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context and save metrics."""
        if self.metrics:
            self.versioner.log_metrics(self.name, self.version, **self.metrics)

    def log(
        self,
        model_name: Optional[str] = None,
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None,
        cost_eur: Optional[float] = None,
        latency_ms: Optional[float] = None,
        quality_score: Optional[float] = None,
        accuracy: Optional[float] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        success: bool = True,
        error_message: Optional[str] = None,
        **extra: Any,
    ) -> None:
        """Log metrics during test.

        Args:
            model_name: Model name
            input_tokens: Input tokens
            output_tokens: Output tokens
            cost_eur: Cost in USD
            latency_ms: Latency in ms
            quality_score: Quality score
            accuracy: Accuracy
            temperature: Temperature
            max_tokens: Max tokens
            success: Success flag
            error_message: Error message
            **extra: Extra metadata
        """
        self.metrics.update(
            {
                "model_name": model_name,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost_eur": cost_eur,
                "latency_ms": latency_ms,
                "quality_score": quality_score,
                "accuracy": accuracy,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "success": success,
                "error_message": error_message,
                "metadata": extra if extra else None,
            }
        )
