# from flext-quality_tests/README.md:240
from __future__ import annotations


def test_should_do_something_when_condition():
    """Test description following should/when pattern.

    Tests that the system performs expected behavior under specific
    conditions, validating both success and failure scenarios.
    """
    # Given (Arrange)
    test_data = create_test_data()
    service = create_test_service()

    # When (Act)
    result = service.perform_operation(test_data)

    # Then (Assert) - Using current API
    data = result.unwrap_or(None)
    assert data is not None
    assert data.expected_property == expected_value
