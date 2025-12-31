---
name: testing
description: Cabin testing philosophy and patterns. Use when planning, writing, or reviewing tests. Enforces minimal regression-focused testing with no mock theater.
---

<objective>
Guide test creation with a minimal, regression-focused philosophy. Tests exist to catch regressions, not to achieve coverage metrics. Every test must verify real behavior, never mock interactions.
</objective>

<essential_principles>

**1. Tests catch regressions, not edge cases**

Write the minimum tests needed to catch breaks. If code works today, a test should fail when it breaks tomorrow. Don't write tests for every possible input - test the happy path and the one or two failure modes that actually matter.

**2. No mock theater - EVER**

Mock theater = tests that verify you called a mock correctly. These tests prove nothing.

```python
# MOCK THEATER - DELETE THIS
async def test_create_bookmark(self):
    mock_client.table.return_value.insert.return_value.execute.return_value.data = [{"id": "123"}]
    result = await repo.create({"url": "https://example.com"})
    mock_client.table.assert_called_with("bookmarks")  # Worthless
    assert result["id"] == "123"  # Of course it equals what we told the mock to return!
```

**The test**: "If I deleted the implementation and returned hardcoded values matching the mock, would this test still pass?" If yes, delete the test.

**3. No HTTP calls in tests**

Tests must be fast and isolated. The `mock_httpx_client` fixture in `tests/fixtures/httpx.py` auto-blocks all HTTP. If a test needs network behavior, configure the mock's return value - never make real calls.

**4. Never test passthrough code**

If a function just calls a library/service and returns the result, don't unit test it. There's no logic to verify.

```python
# PASSTHROUGH - NO TEST NEEDED
async def get_user(self, user_id: str):
    return await self.client.table("users").select("*").eq("id", user_id).execute()
```

This has zero testable logic. Testing it means mocking supabase and verifying you called `table()` - that's mock theater.

**5. Test transformations and decisions**

Only unit test code that transforms data or makes decisions:

```python
# TESTABLE - has logic
def apply_keyword_boost(results: list, query: str) -> list:
    """Boost results where title contains query terms."""
    # This transforms data based on conditions - test it

# TESTABLE - has validation logic
def validate_pagination(limit: int, offset: int) -> None:
    if limit < 0 or offset < 0:
        raise ValidationError("cannot be negative")
    # This makes decisions - test it

# TESTABLE - has parsing logic
def parse_duration(text: str) -> int:
    """Parse '5:32' or '1:23:45' to seconds."""
    # This transforms input - test it
```

</essential_principles>

<quick_start>

Before writing any test, answer these questions:

1. **What regression does this catch?** If you can't name a specific break scenario, don't write the test.

2. **Is there actual logic here?** Transformations, validations, decisions = testable. Passthrough = not testable.

3. **Am I testing the mock or the code?** If the test would pass with hardcoded return values, it's mock theater.

</quick_start>

<what_to_test>

**DO test:**
- Pure functions with inputs → outputs
- Data transformations (parsing, formatting, mapping)
- Validation logic (input checking, error conditions)
- Business rules and decisions
- State machines and workflows with multiple paths

**DON'T test:**
- Database CRUD operations (passthrough)
- API client calls (passthrough)
- Simple getters/setters
- Constructor assignments
- Code that just orchestrates other tested code

</what_to_test>

<test_structure>

**Naming**: `test_<behavior>_<condition>`
```python
def test_parse_duration_handles_hours_minutes_seconds():
def test_validate_url_rejects_javascript_protocol():
def test_boost_increases_score_for_keyword_match():
```

**Arrange-Act-Assert**: Keep tests focused
```python
def test_sanitize_removes_sql_operators():
    # Arrange
    dangerous_input = "SELECT * FROM users; DROP TABLE"

    # Act
    result = sanitize_search_term(dangerous_input)

    # Assert
    assert "SELECT" not in result
    assert "DROP" not in result
```

**One behavior per test**: If a test name has "and" in it, split it.

</test_structure>

<fixtures>

**Use project fixtures** in `tests/fixtures/`:
- `httpx.py` - Auto-blocks HTTP (autouse)
- `openai.py` - Mock OpenAI responses
- `jina.py` - Mock Jina reranker
- `bookmarks.py` - Sample bookmark data
- `html_samples.py` - HTML test data

**Prefer real data over mocks**: Use actual sample data from fixtures when possible. Mocks should simulate external services, not internal logic.

</fixtures>

<when_to_skip_tests>

It's OK to have no unit tests for:

- Repository classes (database passthrough)
- API route handlers that just call services
- Client wrappers around external APIs
- Simple data classes with no methods
- Configuration loading

These are better verified by integration tests or manual testing.

</when_to_skip_tests>

<success_criteria>

Tests are good when:
- Each test catches a specific regression scenario
- Tests run fast (no network, no heavy setup)
- Deleting implementation code causes test failures
- Tests verify outputs, not mock call counts
- Test count is minimal - tens, not hundreds

</success_criteria>
