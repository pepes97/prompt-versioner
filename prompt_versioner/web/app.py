"""Web dashboard for prompt versioner - Flask application factory."""

from flask import Flask, render_template
from typing import Any
import os

from prompt_versioner.web.config import config
from prompt_versioner.web.services.metrics_service import MetricsService
from prompt_versioner.web.services.diff_service import DiffService
from prompt_versioner.web.services.alert_service import AlertService
from prompt_versioner.web.controllers.prompts_view import prompts_bp
from prompt_versioner.web.controllers.versions_view import versions_bp
from prompt_versioner.web.controllers.alerts_view import alerts_bp
from prompt_versioner.web.controllers.export_import_view import export_import_bp


def create_app(versioner: Any, config_name: str = None) -> Flask:
    """Create and configure Flask application.

    Args:
        versioner: PromptVersioner instance
        config_name: Configuration name ('development', 'production', or 'default')

    Returns:
        Configured Flask app
    """
    # Determine config
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")

    config_class = config.get(config_name, config["default"])

    # Create Flask app
    app = Flask(
        __name__,
        template_folder=config_class.TEMPLATE_FOLDER,
        static_folder=config_class.STATIC_FOLDER,
    )

    # Load configuration
    app.config.from_object(config_class)

    # Store versioner
    app.versioner = versioner

    # Initialize services
    app.metrics_service = MetricsService(versioner)
    app.diff_service = DiffService(versioner)
    app.alert_service = AlertService(versioner, app.config)

    # Register blueprints
    app.register_blueprint(prompts_bp)
    app.register_blueprint(versions_bp)
    app.register_blueprint(alerts_bp)
    app.register_blueprint(export_import_bp)

    # Main route
    @app.route("/")
    def index():
        """Render dashboard."""
        return render_template("dashboard.html")

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {"error": "Not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        return {"error": "Internal server error"}, 500

    return app
