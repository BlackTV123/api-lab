import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"


# Base choice: 3 stars as an integer, a real pizza, and the user's token.
def test_base_choice_is_saved(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)

    assert res.status_code == 201
    assert res.json()["stars"] == 3
    assert res.json()["pizza_id"] == pizza_id


# C1: Stars below 1 or above 5 are refused with an error message.
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    new = {"pizza_id": pizza_id, "stars": stars}
    res = api.post("/api/ratings", json=new, headers=auth)

    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}

# C2: Decimal stars are refused because stars must be an integer.
def test_decimal_stars_are_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3.5}
    res = api.post("/api/ratings", json=new, headers=auth)

    assert res.status_code == 400
    assert res.json() == {
        "error": "json: cannot unmarshal number 3.5 into Go struct field Rating.stars of type int"
    }

# C2: Text stars are refused because stars must be an integer.
def test_text_stars_are_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": "3"}
    res = api.post("/api/ratings", json=new, headers=auth)

    assert res.status_code == 400
    assert res.json() == {
        "error": "json: cannot unmarshal string into Go struct field Rating.stars of type int"
    }

# C2: A request without the stars field is refused.
def test_missing_stars_are_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id}
    res = api.post("/api/ratings", json=new, headers=auth)

    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}

# C3: A rating for a nonexistent pizza is refused.
def test_nonexistent_pizza_is_refused(api, auth):
    new = {"pizza_id": 999999999, "stars": 3}
    res = api.post("/api/ratings", json=new, headers=auth)

    assert res.status_code == 400
    assert res.json() == {"error": "pizza ID 999999999 not found"}

# C4: Creating a rating without a token is refused.
def test_missing_token_is_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    res = api.post("/api/ratings", json=new)

    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}

# C4: Creating a rating with a wrong-length token is refused.
def test_wrong_length_token_is_refused(api, auth, pizza_id):
    new = {"pizza_id": pizza_id, "stars": 3}
    wrong_auth = {"Authorization": "token short"}
    res = api.post("/api/ratings", json=new, headers=wrong_auth)

    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}