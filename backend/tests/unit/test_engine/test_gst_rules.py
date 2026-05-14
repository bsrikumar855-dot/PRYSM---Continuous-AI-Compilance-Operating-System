"""Test GST rules."""

from app.engine.rules.gst.v1 import GSTINFormatRule, GSTRateRule


def test_gstin_valid():
    rule = GSTINFormatRule()
    result = rule.evaluate({"gstin": "29ABCDE1234F1Z5"})
    assert result["status"] == "pass"


def test_gstin_invalid():
    rule = GSTINFormatRule()
    result = rule.evaluate({"gstin": "INVALID123"})
    assert result["status"] == "fail"


def test_gst_rate_valid():
    rule = GSTRateRule()
    result = rule.evaluate({"gst_rate": 18})
    assert result["status"] == "pass"


def test_gst_rate_invalid():
    rule = GSTRateRule()
    result = rule.evaluate({"gst_rate": 15})
    assert result["status"] == "fail"
