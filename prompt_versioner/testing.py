"""Testing framework for prompt versions."""

from typing import Callable, Dict, List, Any, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import statistics
from prompt_versioner.metrics import MetricAggregator


@dataclass
class TestCase:
    """A single test case for a prompt."""
    name: str
    inputs: Dict[str, Any]
    expected_output: Optional[Any] = None
    validation_fn: Optional[Callable[[Any], bool]] = None


@dataclass
class TestResult:
    """Result of running a test case."""
    test_case: TestCase
    success: bool
    output: Any
    metrics: Dict[str, float]
    error: Optional[str] = None
    duration_ms: float = 0.0

@dataclass
class ABTestResult:
    """Result of an A/B test."""
    version_a: str
    version_b: str
    metric_name: str
    a_values: List[float]
    b_values: List[float]
    a_mean: float
    b_mean: float
    winner: str
    improvement: float
    confidence: float


class PromptTestRunner:
    """Test runner for prompt versions."""

    def __init__(self, max_workers: int = 4):
        """Initialize test runner.
        
        Args:
            max_workers: Maximum number of parallel test workers
        """
        self.max_workers = max_workers
        self.aggregator = MetricAggregator()

    def run_test(
        self,
        test_case: TestCase,
        prompt_fn: Callable[[Dict[str, Any]], Any],
        metric_fn: Optional[Callable[[Any], Dict[str, float]]] = None,
    ) -> TestResult:
        """Run a single test case.
        
        Args:
            test_case: TestCase to run
            prompt_fn: Function that takes inputs and returns LLM output
            metric_fn: Optional function to compute metrics from output
            
        Returns:
            TestResult object
        """
        start_time = time.time()
        
        try:
            # Run the prompt function
            output = prompt_fn(test_case.inputs)
            
            # Validate output
            success = True
            if test_case.validation_fn:
                success = test_case.validation_fn(output)
            elif test_case.expected_output is not None:
                success = output == test_case.expected_output
            
            # Compute metrics
            metrics = {}
            if metric_fn:
                metrics = metric_fn(output)
            
            duration_ms = (time.time() - start_time) * 1000
            metrics["duration_ms"] = duration_ms
            
            # Aggregate metrics
            self.aggregator.add_batch(metrics)
            
            return TestResult(
                test_case=test_case,
                success=success,
                output=output,
                metrics=metrics,
                duration_ms=duration_ms,
            )
        
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            return TestResult(
                test_case=test_case,
                success=False,
                output=None,
                metrics={"duration_ms": duration_ms},
                error=str(e),
                duration_ms=duration_ms,
            )

    def run_tests(
        self,
        test_cases: List[TestCase],
        prompt_fn: Callable[[Dict[str, Any]], Any],
        metric_fn: Optional[Callable[[Any], Dict[str, float]]] = None,
        parallel: bool = True,
    ) -> List[TestResult]:
        """Run multiple test cases.
        
        Args:
            test_cases: List of TestCase objects
            prompt_fn: Function that takes inputs and returns LLM output
            metric_fn: Optional function to compute metrics from output
            parallel: Whether to run tests in parallel
            
        Returns:
            List of TestResult objects
        """
        self.aggregator.clear()
        
        if parallel and len(test_cases) > 1:
            return self._run_parallel(test_cases, prompt_fn, metric_fn)
        else:
            return self._run_sequential(test_cases, prompt_fn, metric_fn)

    def _run_sequential(
        self,
        test_cases: List[TestCase],
        prompt_fn: Callable[[Dict[str, Any]], Any],
        metric_fn: Optional[Callable[[Any], Dict[str, float]]],
    ) -> List[TestResult]:
        """Run tests sequentially."""
        results = []
        for test_case in test_cases:
            result = self.run_test(test_case, prompt_fn, metric_fn)
            results.append(result)
        return results

    def _run_parallel(
        self,
        test_cases: List[TestCase],
        prompt_fn: Callable[[Dict[str, Any]], Any],
        metric_fn: Optional[Callable[[Any], Dict[str, float]]],
    ) -> List[TestResult]:
        """Run tests in parallel."""
        results = []
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self.run_test, tc, prompt_fn, metric_fn): tc
                for tc in test_cases
            }
            
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
        
        return results

    def get_summary(self, results: List[TestResult]) -> Dict[str, Any]:
        """Generate summary of test results.
        
        Args:
            results: List of TestResult objects
            
        Returns:
            Summary dict with statistics
        """
        total = len(results)
        passed = sum(1 for r in results if r.success)
        failed = total - passed
        
        # Get aggregated metrics
        stats = self.aggregator.get_stats()
        
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "pass_rate": passed / total if total > 0 else 0.0,
            "metrics": {s.name: {
                "mean": s.mean,
                "median": s.median,
                "std_dev": s.std_dev,
                "min": s.min_val,
                "max": s.max_val,
            } for s in stats},
        }

    def format_summary(self, summary: Dict[str, Any]) -> str:
        """Format test summary as human-readable text.
        
        Args:
            summary: Summary dict from get_summary
            
        Returns:
            Formatted string
        """
        lines = ["=" * 80, "TEST SUMMARY", "=" * 80]
        
        lines.append(f"\nTests Run: {summary['total']}")
        lines.append(f"Passed:    {summary['passed']} ({summary['pass_rate']:.1%})")
        lines.append(f"Failed:    {summary['failed']}")
        
        if summary['metrics']:
            lines.append("\nMETRICS:")
            for name, stats in summary['metrics'].items():
                lines.append(f"\n  {name}:")
                lines.append(f"    Mean:   {stats['mean']:.4f}")
                lines.append(f"    Median: {stats['median']:.4f}")
                lines.append(f"    Std:    {stats['std_dev']:.4f}")
                lines.append(f"    Range:  [{stats['min']:.4f}, {stats['max']:.4f}]")
        
        return "\n".join(lines)


class TestDataset:
    """Collection of test cases."""

    def __init__(self, name: str):
        """Initialize test dataset.
        
        Args:
            name: Dataset name
        """
        self.name = name
        self.test_cases: List[TestCase] = []

    def add_test(
        self,
        name: str,
        inputs: Dict[str, Any],
        expected_output: Optional[Any] = None,
        validation_fn: Optional[Callable[[Any], bool]] = None,
    ) -> None:
        """Add a test case to the dataset.
        
        Args:
            name: Test case name
            inputs: Input dict for the prompt
            expected_output: Optional expected output
            validation_fn: Optional validation function
        """
        self.test_cases.append(
            TestCase(
                name=name,
                inputs=inputs,
                expected_output=expected_output,
                validation_fn=validation_fn,
            )
        )

    def add_tests_from_list(
        self,
        tests: List[Dict[str, Any]],
        validation_fn: Optional[Callable[[Any], bool]] = None,
    ) -> None:
        """Add multiple test cases from a list.
        
        Args:
            tests: List of dicts with 'name', 'inputs', 'expected_output' keys
            validation_fn: Optional validation function for all tests
        """
        for test in tests:
            self.add_test(
                name=test["name"],
                inputs=test["inputs"],
                expected_output=test.get("expected_output"),
                validation_fn=validation_fn,
            )

    def get_tests(self) -> List[TestCase]:
        """Get all test cases.
        
        Returns:
            List of TestCase objects
        """
        return self.test_cases

    def __len__(self) -> int:
        """Get number of test cases."""
        return len(self.test_cases)
    


class ABTest:
    """A/B test framework for comparing prompt versions."""
    
    def __init__(
        self,
        versioner: Any,
        prompt_name: str,
        version_a: str,
        version_b: str,
        metric_name: str = "quality_score"
    ):
        """Initialize A/B test.
        
        Args:
            versioner: PromptVersioner instance
            prompt_name: Name of prompt to test
            version_a: First version (baseline)
            version_b: Second version (challenger)
            metric_name: Metric to compare
        """
        self.versioner = versioner
        self.prompt_name = prompt_name
        self.version_a = version_a
        self.version_b = version_b
        self.metric_name = metric_name
        
        self.results_a: List[float] = []
        self.results_b: List[float] = []
    
    def log_result(self, version: str, metric_value: float) -> None:
        """Log a test result.
        
        Args:
            version: Which version (a or b)
            metric_value: Metric value
        """
        if version == "a":
            self.results_a.append(metric_value)
        elif version == "b":
            self.results_b.append(metric_value)
        else:
            raise ValueError(f"Invalid version: {version}")
    
    def get_result(self) -> ABTestResult:
        """Get A/B test result.
        
        Returns:
            ABTestResult with winner and statistics
        """
        if not self.results_a or not self.results_b:
            raise ValueError("Not enough data for A/B test")
        
        mean_a = statistics.mean(self.results_a)
        mean_b = statistics.mean(self.results_b)
        
        # Simple winner determination (could use t-test for real confidence)
        winner = "b" if mean_b > mean_a else "a"
        improvement = abs(mean_b - mean_a) / mean_a * 100
        
        # Simplified confidence (would need proper statistical test)
        confidence = min(len(self.results_a), len(self.results_b)) / 30.0
        confidence = min(confidence, 1.0)
        
        return ABTestResult(
            version_a=self.version_a,
            version_b=self.version_b,
            metric_name=self.metric_name,
            a_values=self.results_a,
            b_values=self.results_b,
            a_mean=mean_a,
            b_mean=mean_b,
            winner=self.version_b if winner == "b" else self.version_a,
            improvement=improvement,
            confidence=confidence
        )
    
    def print_result(self) -> None:
        """Print formatted A/B test result."""
        result = self.get_result()
        
        print("=" * 60)
        print(f"A/B Test Results: {self.prompt_name}")
        print("=" * 60)
        print(f"Metric: {self.metric_name}")
        print(f"\nVersion A ({result.version_a}):")
        print(f"  Mean: {result.a_mean:.4f}")
        print(f"  Samples: {len(result.a_values)}")
        print(f"\nVersion B ({result.version_b}):")
        print(f"  Mean: {result.b_mean:.4f}")
        print(f"  Samples: {len(result.b_values)}")
        print(f"\n🏆 Winner: {result.winner}")
        print(f"📈 Improvement: {result.improvement:.2f}%")
        print(f"🎯 Confidence: {result.confidence:.1%}")
        print("=" * 60)