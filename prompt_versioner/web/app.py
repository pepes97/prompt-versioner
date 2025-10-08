"""Web dashboard for prompt versioner - Flask application."""

from flask import Flask, render_template, jsonify, send_file, request
from typing import Any
from pathlib import Path
import tempfile
import zipfile


def create_inline_diff(old_text: str, new_text: str) -> list:
    """Create word-level inline diff for highlighting.
    
    Args:
        old_text: Previous text
        new_text: New text
        
    Returns:
        List of dicts with 'type' and 'text' for each segment
    """
    import difflib
    
    old_words = old_text.split()
    new_words = new_text.split()
    
    diff_result = []
    matcher = difflib.SequenceMatcher(None, old_words, new_words)
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            diff_result.append({
                'type': 'unchanged',
                'text': ' '.join(new_words[j1:j2])
            })
        elif tag == 'delete':
            diff_result.append({
                'type': 'removed',
                'text': ' '.join(old_words[i1:i2])
            })
        elif tag == 'insert':
            diff_result.append({
                'type': 'added',
                'text': ' '.join(new_words[j1:j2])
            })
        elif tag == 'replace':
            diff_result.append({
                'type': 'removed',
                'text': ' '.join(old_words[i1:i2])
            })
            diff_result.append({
                'type': 'added',
                'text': ' '.join(new_words[j1:j2])
            })
    
    return diff_result


def create_app(versioner: Any) -> Flask:
    """Create Flask app for dashboard.
    
    Args:
        versioner: PromptVersioner instance
        
    Returns:
        Flask app
    """
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    app.versioner = versioner

    @app.route('/')
    def index() -> str:
        """Render dashboard."""
        return render_template('dashboard.html')

    @app.route('/api/prompts')
    def get_prompts() -> Any:
        """Get all prompts with metadata."""
        try:
            prompts = app.versioner.list_prompts()
            
            prompt_data = []
            total_versions = 0
            total_cost = 0.0
            total_tokens = 0
            total_calls = 0
            
            for name in prompts:
                versions = app.versioner.list_versions(name)
                total_versions += len(versions)
                
                for v in versions:
                    summary = app.versioner.storage.get_metrics_summary(v['id'])
                    if summary:
                        total_cost += summary.get('total_cost', 0) or 0
                        total_tokens += summary.get('total_tokens_used', 0) or 0
                        total_calls += summary.get('call_count', 0) or 0
                
                latest = versions[0] if versions else None
                prompt_data.append({
                    'name': name,
                    'version_count': len(versions),
                    'latest_version': latest['version'] if latest else 'N/A',
                    'latest_timestamp': latest['timestamp'] if latest else None,
                })
            
            return jsonify({
                'prompts': prompt_data,
                'total_versions': total_versions,
                'total_cost': round(total_cost, 4),
                'total_tokens': total_tokens,
                'total_calls': total_calls,
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/prompts/<name>/versions')
    def get_versions(name: str) -> Any:
        """Get all versions of a prompt with metrics."""
        try:
            versions = app.versioner.list_versions(name)
            
            for v in versions:
                v['metrics_summary'] = app.versioner.storage.get_metrics_summary(v['id'])
            
            return jsonify(versions)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/prompts/<name>/versions/with-diffs')
    def get_versions_with_diffs(name: str) -> Any:
        """Get all versions with diffs from previous version."""
        try:
            from prompt_versioner.diff import DiffEngine
            
            versions = app.versioner.list_versions(name)
            
            if not versions:
                return jsonify([])
            
            for i, v in enumerate(versions):
                v['metrics_summary'] = app.versioner.storage.get_metrics_summary(v['id'])
                
                metrics_list = app.versioner.storage.get_metrics(v['id'])
                model_name = None
                if metrics_list:
                    model_names = [m.get('model_name') for m in metrics_list if m.get('model_name')]
                    if model_names:
                        model_name = model_names[0]
                v['model_name'] = model_name

                annotations = app.versioner.storage.get_annotations(v['id'])
                v['annotations'] = annotations
                
                if i < len(versions) - 1:
                    prev_version = versions[i + 1]
                    
                    diff = DiffEngine.compute_diff(
                        old_system=prev_version['system_prompt'],
                        old_user=prev_version['user_prompt'],
                        new_system=v['system_prompt'],
                        new_user=v['user_prompt'],
                    )
                    
                    v['has_changes'] = diff.total_similarity < 1.0
                    v['diff_summary'] = diff.summary
                    v['system_similarity'] = diff.system_similarity
                    v['user_similarity'] = diff.user_similarity
                    
                    v['system_diff'] = create_inline_diff(
                        prev_version['system_prompt'],
                        v['system_prompt']
                    )
                    v['user_diff'] = create_inline_diff(
                        prev_version['user_prompt'],
                        v['user_prompt']
                    )
                else:
                    v['has_changes'] = False
                    v['diff_summary'] = "Initial version"
                    v['system_diff'] = [{'type': 'unchanged', 'text': v['system_prompt']}]
                    v['user_diff'] = [{'type': 'unchanged', 'text': v['user_prompt']}]
            
            return jsonify(versions)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/prompts/<name>/versions/<version>')
    def get_version_detail(name: str, version: str) -> Any:
        """Get a specific version with metrics summary."""
        try:
            v = app.versioner.get_version(name, version)
            if v:
                metrics_summary = app.versioner.storage.get_metrics_summary(v['id'])
                metrics_list = app.versioner.storage.get_metrics(v['id'])
                
                v['metrics_summary'] = metrics_summary
                v['metrics_history'] = metrics_list
                return jsonify(v)
            return jsonify({'error': 'Version not found'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/prompts/<name>/stats')
    def get_prompt_stats(name: str) -> Any:
        """Get aggregated stats across all versions of a prompt."""
        try:
            versions = app.versioner.list_versions(name)
            
            if not versions:
                return jsonify({'error': 'Prompt not found'}), 404
            
            total_calls = 0
            total_cost = 0.0
            total_tokens = 0
            all_latencies = []
            all_quality_scores = []
            models_used = set()
            version_stats = []
            
            for v in versions:
                summary = app.versioner.storage.get_metrics_summary(v['id'])
                if summary and summary.get('call_count', 0) > 0:
                    total_calls += summary.get('call_count', 0)
                    total_cost += summary.get('total_cost', 0)
                    total_tokens += summary.get('total_tokens_used', 0)
                    
                    if summary.get('avg_latency'):
                        all_latencies.append(summary['avg_latency'])
                    if summary.get('avg_quality'):
                        all_quality_scores.append(summary['avg_quality'])
                    
                    metrics = app.versioner.storage.get_metrics(v['id'])
                    for m in metrics:
                        if m.get('model_name'):
                            models_used.add(m['model_name'])
                    
                    version_stats.append({
                        'version': v['version'],
                        'timestamp': v['timestamp'],
                        'summary': summary,
                    })
            
            return jsonify({
                'name': name,
                'total_versions': len(versions),
                'total_calls': total_calls,
                'total_cost_eur': round(total_cost, 4),
                'total_tokens': total_tokens,
                'avg_latency_ms': round(sum(all_latencies) / len(all_latencies), 2) if all_latencies else 0,
                'avg_quality_score': round(sum(all_quality_scores) / len(all_quality_scores), 2) if all_quality_scores else 0,
                'models_used': list(models_used),
                'version_stats': version_stats,
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/prompts/<name>/ab-tests')
    def get_ab_tests(name: str) -> Any:
        """Get available versions for A/B testing."""
        try:
            versions = app.versioner.list_versions(name)
            
            testable_versions = []
            for v in versions:
                summary = app.versioner.storage.get_metrics_summary(v['id'])
                if summary and summary.get('call_count', 0) >= 5:
                    testable_versions.append({
                        'version': v['version'],
                        'timestamp': v['timestamp'],
                        'call_count': summary['call_count'],
                        'avg_quality': summary.get('avg_quality', 0),
                        'avg_cost': summary.get('avg_cost', 0),
                        'avg_latency': summary.get('avg_latency', 0),
                    })
            
            return jsonify(testable_versions)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/prompts/<name>/compare')
    def compare_versions_api(name: str) -> Any:
        """Compare two versions with A/B test style analysis."""
        try:
            version_a = request.args.get('version_a')
            version_b = request.args.get('version_b')
            metric = request.args.get('metric', 'quality_score')
            
            if not version_a or not version_b:
                return jsonify({'error': 'Missing version_a or version_b'}), 400
            
            v_a = app.versioner.get_version(name, version_a)
            v_b = app.versioner.get_version(name, version_b)
            
            if not v_a or not v_b:
                return jsonify({'error': 'Version not found'}), 404
            
            summary_a = app.versioner.storage.get_metrics_summary(v_a['id'])
            summary_b = app.versioner.storage.get_metrics_summary(v_b['id'])
            
            metric_map = {
                'quality_score': 'avg_quality',
                'cost': 'avg_cost',
                'latency': 'avg_latency',
                'accuracy': 'avg_accuracy'
            }
            
            summary_metric = metric_map.get(metric, 'avg_quality')
            
            value_a = summary_a.get(summary_metric, 0) if summary_a else 0
            value_b = summary_b.get(summary_metric, 0) if summary_b else 0
            
            if metric in ['cost', 'latency']:
                winner = 'a' if value_a < value_b else 'b'
                improvement = abs(value_b - value_a) / value_a * 100 if value_a > 0 else 0
            else:
                winner = 'a' if value_a > value_b else 'b'
                improvement = abs(value_b - value_a) / value_a * 100 if value_a > 0 else 0
            
            return jsonify({
                'version_a': version_a,
                'version_b': version_b,
                'metric': metric,
                'summary_a': summary_a,
                'summary_b': summary_b,
                'value_a': value_a,
                'value_b': value_b,
                'winner': version_b if winner == 'b' else version_a,
                'improvement_percent': improvement,
                'call_count_a': summary_a.get('call_count', 0) if summary_a else 0,
                'call_count_b': summary_b.get('call_count', 0) if summary_b else 0,
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/prompts/<name>/diff')
    def get_diff(name: str) -> Any:
        """Get diff between two versions."""
        try:
            v1 = request.args.get('version1')
            v2 = request.args.get('version2')
            
            if not all([name, v1, v2]):
                return jsonify({'error': 'Missing parameters'}), 400
            
            diff = app.versioner.diff(name, v1, v2)
            return jsonify({
                'summary': diff.summary,
                'system_similarity': diff.system_similarity,
                'user_similarity': diff.user_similarity,
                'total_similarity': diff.total_similarity,
            })
        except ValueError as e:
            return jsonify({'error': str(e)}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    @app.route('/api/prompts/<name>/alerts')
    def get_alerts(name: str) -> Any:
        """Get performance alerts for a prompt."""
        try:
            from prompt_versioner.monitoring import PerformanceMonitor
            
            versions = app.versioner.list_versions(name)
            if len(versions) < 2:
                return jsonify([])
            
            monitor = PerformanceMonitor(app.versioner)
            
            latest = versions[0]
            previous = versions[1]
            
            alerts = monitor.check_regression(
                name=name,
                current_version=latest["version"],
                baseline_version=previous["version"],
                thresholds={
                    "cost": 0.20,
                    "latency": 0.30,
                    "quality": -0.10,
                    "error_rate": 0.05
                }
            )
            
            alerts_data = []
            for alert in alerts:
                alerts_data.append({
                    "type": alert.alert_type.value,
                    "message": alert.message,
                    "metric_name": alert.metric_name,
                    "baseline_value": alert.baseline_value,
                    "current_value": alert.current_value,
                    "change_percent": alert.change_percent,
                    "threshold": alert.threshold,
                    "current_version": alert.current_version,
                    "baseline_version": alert.baseline_version
                })
            
            return jsonify(alerts_data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/alerts')
    def get_all_alerts() -> Any:
        """Get all performance alerts across all prompts."""
        try:
            from prompt_versioner.monitoring import PerformanceMonitor
            
            all_alerts = []
            prompts = app.versioner.list_prompts()
            monitor = PerformanceMonitor(app.versioner)
            
            for prompt_name in prompts:
                versions = app.versioner.list_versions(prompt_name)
                if len(versions) < 2:
                    continue
                
                latest = versions[0]
                previous = versions[1]
                
                alerts = monitor.check_regression(
                    name=prompt_name,
                    current_version=latest["version"],
                    baseline_version=previous["version"]
                )
                
                for alert in alerts:
                    all_alerts.append({
                        "prompt_name": prompt_name,
                        "type": alert.alert_type.value,
                        "message": alert.message,
                        "metric_name": alert.metric_name,
                        "baseline_value": alert.baseline_value,
                        "current_value": alert.current_value,
                        "change_percent": alert.change_percent,
                        "threshold": alert.threshold,
                        "current_version": alert.current_version,
                        "baseline_version": alert.baseline_version
                    })
            
            return jsonify(all_alerts)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/prompts/<name>/export')
    def export_prompt_endpoint(name: str) -> Any:
        """Export a prompt to JSON file."""
        try:
            temp_file = Path(tempfile.gettempdir()) / f"{name}.json"
            app.versioner.export_prompt(name, temp_file, format="json", include_metrics=True)
            
            return send_file(
                temp_file,
                as_attachment=True,
                download_name=f"{name}_export.json",
                mimetype='application/json'
            )
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/prompts/import', methods=['POST'])
    def import_prompt_endpoint() -> Any:
        """Import a prompt from uploaded JSON file."""
        try:
            if 'file' not in request.files:
                return jsonify({'error': 'No file uploaded'}), 400
            
            file = request.files['file']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400
            
            temp_file = Path(tempfile.gettempdir()) / file.filename
            file.save(temp_file)
            
            result = app.versioner.import_prompt(temp_file, overwrite=False)
            
            temp_file.unlink()
            
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/export-all')
    def export_all_endpoint() -> Any:
        """Export all prompts as ZIP."""
        try:
            temp_dir = Path(tempfile.gettempdir()) / "prompt_export"
            temp_dir.mkdir(exist_ok=True)
            
            app.versioner.export_all(temp_dir, format="json")
            
            zip_path = Path(tempfile.gettempdir()) / "all_prompts.zip"
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for json_file in temp_dir.glob("*.json"):
                    zipf.write(json_file, json_file.name)
            
            for json_file in temp_dir.glob("*.json"):
                json_file.unlink()
            temp_dir.rmdir()
            
            return send_file(
                zip_path,
                as_attachment=True,
                download_name="all_prompts.zip",
                mimetype='application/zip'
            )
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return app