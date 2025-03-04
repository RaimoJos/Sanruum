from __future__ import annotations

from sanruum.utils.health.chronic.diabetes.diabetes_tools import (
    calculate_blood_sugar_level,
)


def test_calculate_blood_sugar_level() -> None:
    # Test cases for different blood sugar levels in mmol/L
    test_cases = [
        (3.5, 'Your blood sugar is low. Please take necessary action to raise it.'),
        (5.0, 'Your blood sugar is in healthy range.'),
        (8.0, 'Your blood sugar is high. Please take necessary action to lower it.'),
    ]

    for blood_sugar, expected_response in test_cases:
        result = calculate_blood_sugar_level(blood_sugar)
        assert result == expected_response, \
            f'Expected: {expected_response}, but got: {result}'

    print('All tests passed!')
