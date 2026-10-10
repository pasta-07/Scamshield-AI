"""
Pytest Configuration & Database Isolation Fixtures
RAKSHAM AI Cybersecurity Hackathon | IIT Delhi (Problem Statement 2)
"""

import os
import pytest
from src.storage import init_db, get_db_connection


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    test_db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "test_scamshield.db")
    os.environ["SCAMSHIELD_DB_PATH"] = test_db_path
    init_db()
    yield test_db_path
    # Cleanup after session
    try:
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
    except Exception:
        pass


@pytest.fixture(autouse=True)
def clean_tables_per_test():
    """Wipes table rows before each test to maintain clean state."""
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM alerts")
        cursor.execute("DELETE FROM analysis_history")
        conn.commit()
    yield
