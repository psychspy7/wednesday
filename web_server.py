"""
web_server.py — Flask backend for the React web frontend.

Provides a simple REST API:
  POST /api/chat     — Send a message, get a response
  GET  /api/status   — Get current status (mood, name, etc.)
  POST /api/mood     — Change mood
  POST /api/clear    — Clear memory
  GET  /             — Serve the React frontend

Start with: python main.py --web
"""

import logging
from pathlib import Path

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from core.orchestrator import Orchestrator
import config

logger = logging.getLogger("buddy.web")


def create_app(orchestrator: Orchestrator) -> Flask:
    """
    Create and configure the Flask app.

    Args:
        orchestrator: The initialized Orchestrator instance.

    Returns:
        Configured Flask app.
    """
    app = Flask(
        __name__,
        static_folder=str(Path(__file__).parent / "frontend"),
        static_url_path="",
    )
    CORS(app)

    # ── Routes ────────────────────────────────────────────────────────

    @app.route("/")
    def index():
        """Serve the React frontend."""
        return send_from_directory(app.static_folder, "index.html")

    @app.route("/api/chat", methods=["POST"])
    def chat():
        """
        Process a chat message.

        Request body: {"message": "user's message"}
        Response: {"response": "buddy's response", "mood": "funny"}
        """
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Missing 'message' field"}), 400

        user_message = data["message"].strip()
        if not user_message:
            return jsonify({"error": "Empty message"}), 400

        logger.info(f"Web chat: {user_message[:100]}")

        try:
            response = orchestrator.process(user_message)
            return jsonify({
                "response": response,
                "mood": orchestrator.mood,
                "buddy_name": config.BUDDY_NAME,
            })
        except Exception as e:
            logger.error(f"Chat error: {e}")
            return jsonify({"error": str(e)}), 500

    @app.route("/api/status", methods=["GET"])
    def status():
        """Get current assistant status."""
        return jsonify({
            "buddy_name": config.BUDDY_NAME,
            "user_name": config.USER_NAME,
            "mood": orchestrator.mood,
            "provider": config.LLM_PROVIDER,
            "model": config.LLM_MODEL,
            "memory_size": len(orchestrator.memory),
            "plugins": orchestrator.plugins.list_plugins(),
        })

    @app.route("/api/mood", methods=["POST"])
    def set_mood():
        """Change the mood mode."""
        data = request.get_json()
        mood = data.get("mood", "").lower()
        valid = ["funny", "serious", "savage", "chill"]

        if mood not in valid:
            return jsonify({"error": f"Invalid mood. Options: {valid}"}), 400

        result = orchestrator._cmd_mood(mood)
        return jsonify({"result": result, "mood": orchestrator.mood})

    @app.route("/api/clear", methods=["POST"])
    def clear_memory():
        """Clear conversation memory."""
        orchestrator.memory.clear()
        return jsonify({"result": "Memory cleared", "mood": orchestrator.mood})

    return app
