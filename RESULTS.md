# API lab results

## Part 0
- Step 0.1, the number of pizza names: 18

- Step 0.4, the name of your pizza: The Happy Calzone

- Step 0.16, blocks of "how many of the three tools are excluded": 0, 1, 2, and 3 tools.

## Part A
- Step A4, status codes when the other user reads, changes and deletes:
  - Read (GET): 404
  - Change (PUT): 400
  - Delete (DELETE): 400
- All three attempts were refused, and the owner's rating remained unchanged.

## Part B

1. API tests can detect failures in real server-to-database integration
   and authentication or load-balancer configuration that unit tests
   with stubs may miss. Unit tests are still useful because they run
   quickly and help isolate faults in individual functions.

2. Each test creates a uniquely named user to keep its data independent
   of other tests and users. Using the public token could allow shared
   data to change unexpectedly. In Project 2, I will create uniquely
   identified test data and modify or delete only data my tests created.

3. A session preserves cookies, including AWSALB, so requests reach the
   same backend server. QuickPizza servers maintain their own user data,
   so registration and login could reach different servers without the
   cookie, causing login failures. I skipped optional Step 0.12.

4. The block excluding all three tools revealed the defect.
   The API returned 500 with an empty body instead of 400 with a JSON
   error message. The empty response gives the calling application
   no useful explanation of the invalid request.
   The test remains as xfail to document and track the defect.
   With strict=True, an unexpected pass fails the suite, prompting
   removal of the xfail marker after the defect is fixed.

5. The four characteristics contain 3, 4, 2, and 3 blocks.
   Base choice coverage requires:
   1 + (3 - 1) + (4 - 1) + (2 - 1) + (3 - 1) = 9 test cases.
   All combinations coverage requires:
   3 × 4 × 2 × 3 = 72 test cases.

6. Another user's read, update, and delete attempts returned
   404, 400, and 400 respectively. All attempts were refused,
   and the owner's rating remained unchanged.
   I would generally expect 403 Forbidden for an authenticated user
   without permission. A 404 can also hide the resource's existence.
   The different status codes alone do not violate this lab's
   requirement, which accepts any 400–499 response as long as
   the rating remains unchanged.

7. Using the made-up token 0000000000000000 with GET /api/ratings
   returned 200 OK and a list of ratings instead of 401 Unauthorized.
   This is a defect under the requirement that access needs a valid
   token obtained through login. On a real system, an unauthorized
   person could read information that should require authentication.
   This experiment demonstrated read access only; I did not attempt
   to create, update, or delete data using this token.

8. API tests directly inspect status codes, JSON fields, and responses
   to invalid inputs. Tests through web pages can check visual layout
   and whether buttons and forms work correctly for the user.