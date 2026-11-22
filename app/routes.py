
from flask import Blueprint, jsonify, request, render_template

bp = Blueprint("api", __name__)
MAX_MESSAGE_LENGTH = 1000


def mock_financial_assistant(message):
    """Deterministic mock: not an LLM."""
    lower = message.lower()

    if "budget" in lower or "бюджет" in lower:
        return "You can start by tracking your income and expenses."

    if "sav" in lower or "сбереж" in lower:
        return "Consider setting a monthly savings goal and tracking your progress."

    return "I can share general budgeting and saving tips, but not personal financial advice."


@bp.get("/")
def home():
    return render_template("index.html")


@bp.get("/health")
def health():
    return jsonify(status="healthy")


@bp.post("/api/chat")
def chat():
    if not request.is_json:
        return jsonify(error="Content-Type must be application/json"), 415

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify(error="Invalid JSON object"), 400

    if "message" not in data:
        return jsonify(error="Missing message"), 400

    message = data["message"]

    if not isinstance(message, str):
        return jsonify(error="Message must be a string"), 400

    message = message.strip()

    if not message:
        return jsonify(error="Message cannot be empty"), 400

    if len(message) > MAX_MESSAGE_LENGTH:
        return jsonify(error="Message too long"), 400

    answer = mock_financial_assistant(message)

    if not isinstance(answer, str) or len(answer) > 2000:
        return jsonify(error="Invalid assistant output"), 500

    return jsonify(response=answer)
