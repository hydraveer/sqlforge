from pathlib import Path

import pytest

from src.evaluate import is_correct

DB_PATH = str(Path(__file__).resolve().parent.parent / "data/spider/database/concert_singer/concert_singer.sqlite")


@pytest.fixture(autouse=True)
def require_db() -> None:
    if not Path(DB_PATH).exists():
        pytest.skip(f"Spider database not found at {DB_PATH}")


def test_identical_query_is_correct() -> None:
    sql = "SELECT name, age FROM singer"
    correct, error = is_correct(DB_PATH, sql, sql)
    assert correct
    assert error is None


def test_different_order_without_order_by_is_correct() -> None:
    gold = "SELECT name FROM singer"
    pred = "SELECT name FROM singer ORDER BY name DESC"
    correct, error = is_correct(DB_PATH, gold, pred)
    assert correct
    assert error is None


def test_different_order_with_order_by_is_wrong() -> None:
    gold = "SELECT name FROM singer ORDER BY age ASC"
    pred = "SELECT name FROM singer ORDER BY age DESC"
    correct, _ = is_correct(DB_PATH, gold, pred)
    assert not correct


def test_invalid_sql_is_wrong_with_error() -> None:
    gold = "SELECT name FROM singer"
    pred = "SELECT nme FROM no_such_table"
    correct, error = is_correct(DB_PATH, gold, pred)
    assert not correct
    assert error


def test_different_results_is_wrong() -> None:
    gold = "SELECT name FROM singer"
    pred = "SELECT name FROM singer WHERE age > 30"
    correct, error = is_correct(DB_PATH, gold, pred)
    assert not correct
    assert error is None
