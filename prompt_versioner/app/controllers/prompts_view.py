"""Controller for prompt-related routes."""

from flask import Blueprint, jsonify, current_app
from typing import Any


prompts_bp = Blueprint("prompts", __name__, url_prefix="/api/prompts")


@prompts_bp.route("", methods=["GET"])
def get_prompts() -> Any:
    """Get all prompts with metadata."""
    try:
        metrics_service = current_app.metrics_service  # type: ignore[attr-defined]
        stats = metrics_service.get_global_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@prompts_bp.route("/<name>/stats", methods=["GET"])
def get_prompt_stats(name: str) -> Any:
    """Get aggregated stats for a specific prompt."""
    try:
        metrics_service = current_app.metrics_service  # type: ignore[attr-defined]
        stats = metrics_service.get_prompt_stats(name)
        return jsonify(stats)
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@prompts_bp.route("/<name>/ab-tests", methods=["GET"])
def get_ab_tests(name: str) -> Any:
    """Get available versions for A/B testing."""
    try:
        versioner = current_app.versioner  # type: ignore[attr-defined]
        config = current_app.config

        versions = versioner.list_versions(name)

        testable_versions = []
        for v in versions:
            summary = versioner.storage.get_metrics_summary(v["id"])
            if summary and summary.get("call_count", 0) >= config["MIN_CALLS_FOR_AB_TEST"]:
                testable_versions.append(
                    {
                        "version": v["version"],
                        "timestamp": v["timestamp"],
                        "call_count": summary["call_count"],
                        "avg_quality": summary.get("avg_quality", 0),
                        "avg_cost": summary.get("avg_cost", 0),
                        "avg_latency": summary.get("avg_latency", 0),
                    }
                )

        return jsonify(testable_versions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
