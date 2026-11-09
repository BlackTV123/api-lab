import pytest


# The pizza never needs a tool that the customer excluded.
@pytest.mark.parametrize(
    "excluded",
    [
        [],
        ["Knife"],
        ["Scissors"],
        ["Knife", "Scissors"],
    ],
)
def test_excluded_tool_is_not_used(api, auth, excluded):
    res = api.post(
        "/api/pizza",
        json={"excludedTools": excluded},
        headers=auth,
    )
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded


# Excluding every tool must return a client error with a JSON message.
@pytest.mark.xfail(
    reason="Defect 1: Excluding all tools returns 500 instead of 400 with a JSON error",
    strict=True,
)
def test_excluding_all_tools_is_refused(api, auth):
    res = api.post(
        "/api/pizza",
        json={"excludedTools": ["Knife", "Pizza cutter", "Scissors"]},
        headers=auth,
    )
    assert res.status_code == 400
    assert res.headers["Content-Type"].startswith("application/json")
    assert isinstance(res.json()["error"], str)
    assert res.json()["error"].strip() != ""