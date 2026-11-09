## Input domain model: POST /api/ratings

| Characteristic | Blocks | Test values |
| --- | --- | --- |
| C1: Value of stars | Below 1 / 1–5 (base) / Above 5 | 0 / 3 / 6 |
| C2: Type of stars | Integer (base) / Decimal / Text / Missing | 3 / 3.5 / "3" / No stars field |
| C3: Pizza | Exists (base) / Does not exist | New pizza ID / 999999999 |
| C4: Token | User's own (base) / None / Wrong length | auth fixture / No header / token short |

## Base choice coverage

The base test uses 3 integer stars, an existing pizza, and the user's own token.
Each additional case changes one characteristic from the base.

| Block | Test |
| --- | --- |
| Base: valid stars, integer type, existing pizza, own token | test_base_choice_is_saved |
| C1: Below 1 | test_stars_out_of_range[0] |
| C1: Above 5 | test_stars_out_of_range[6] |
| C2: Decimal | test_decimal_stars_are_refused |
| C2: Text | test_text_stars_are_refused |
| C2: Missing | test_missing_stars_are_refused |
| C3: Pizza does not exist | test_nonexistent_pizza_is_refused |
| C4: No token | test_missing_token_is_refused |
| C4: Wrong-length token | test_wrong_length_token_is_refused |