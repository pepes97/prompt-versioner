"""Prompt Versioner - Intelligent versioning for LLM prompts."""

# Import relativi corretti per quando è installato come package
from .core import PromptVersioner, TestContext, VersionBump, PreReleaseLabel
from .storage import PromptStorage
from .diff import DiffEngine, PromptDiff, ChangeType
from .tracker import GitTracker, AutoTracker, PromptHasher
from .metrics import MetricsTracker, MetricType, MetricAggregator, ModelMetrics, MetricsCalculator
from .testing import PromptTestRunner, TestCase, TestResult, TestDataset, ABTest, ABTestResult
from .monitoring import PerformanceMonitor, Alert, AlertType

__version__ = "0.1.0"

__all__ = [
    "PromptVersioner",
    "TestContext",
    "VersionBump",
    "PreReleaseLabel",
    "PromptStorage",
    "DiffEngine",
    "PromptDiff",
    "ChangeType",
    "GitTracker",
    "AutoTracker",
    "PromptHasher",
    "MetricsTracker",
    "MetricType",
    "MetricAggregator",
    "ModelMetrics",
    "MetricsCalculator",
    "PromptTestRunner",
    "TestCase",
    "TestResult",
    "TestDataset",
    "ABTest",
    "ABTestResult",
    "PerformanceMonitor",
    "Alert",
    "AlertType",
]