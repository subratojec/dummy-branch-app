# app/routes/health.py
from flask import Blueprint, jsonify, current_app
from sqlalchemy import text, create_engine
import logging
import os

bp = Blueprint("health", __name__)
log = logging.getLogger(__name__)

def _probe_db_via_extension():
    ext = current_app.extensions.get("sqlalchemy")
    if ext:
        db_inst = getattr(ext, "db", None)
        if db_inst is not None:
            return db_inst.engine
    return None

def _probe_db_via_import():
    try:
        # common pattern: app.db exists after initialization
        from app import db as app_db
        engine = getattr(app_db, "engine", None)
        if engine is None:
            try:
                engine = app_db.get_engine(current_app)
            except Exception:
                engine = None
        return engine
    except Exception:
        return None

def _probe_db_via_env():
    url = os.environ.get("DATABASE_URL") or current_app.config.get("DATABASE_URL") \
          or os.environ.get("SQLALCHEMY_DATABASE_URI") or current_app.config.get("SQLALCHEMY_DATABASE_URI")
    if not url:
        return None
    try:
        return create_engine(url)
    except Exception:
        log.exception("create_engine failed")
        return None

@bp.route("/health", methods=["GET"])
def health():
    engine = _probe_db_via_extension() or _probe_db_via_import() or _probe_db_via_env()

    if engine is None:
        msg = "Flask-SQLAlchemy extension not initialized and DATABASE_URL not available"
        log.error(msg)
        return jsonify({"status": "fail", "error": msg}), 500

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as exc:
        log.exception("DB probe failed")
        return jsonify({"status": "fail", "error": str(exc)}), 500

    return jsonify({"status": "ok"}), 200
