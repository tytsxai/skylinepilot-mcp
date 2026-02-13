from src.skylinepilot.interfaces.web_api.response import ok_response, error_response


def test_ok_response_shape():
    payload = {"x": 1}
    result = ok_response(payload)
    assert result["ok"] is True
    assert result["data"] == payload
    assert result["error"] is None


def test_error_response_shape():
    result = error_response("参数错误", code="VALIDATION")
    assert result["ok"] is False
    assert result["data"] is None
    assert result["error"]["code"] == "VALIDATION"
    assert result["error"]["message"] == "参数错误"

