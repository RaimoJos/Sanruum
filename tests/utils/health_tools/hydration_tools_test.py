from __future__ import annotations

from sanruum.utils.health.general_health.hydration_tools import calculate_hydration


def test_hydration_basic() -> None:
    result = calculate_hydration(70, 'sedentary', 20)
    assert 'Your recommended daily water intake is' in result
    assert 'L' in result  # Should contain L (liters) in the result


def test_hydration_active() -> None:
    # Test for an athlete with 70kg weight, athletic activity level
    result = calculate_hydration(70, 'athletic', 20)
    assert 'Your recommended daily water intake is' in result
    assert 'L' in result


def test_hydration_hot_weather() -> None:
    # Test for hot weather adjustment (temperature > 30)
    result = calculate_hydration(70, 'sedentary', 35)
    assert 'Your recommended daily water intake is' in result
    assert 'L' in result


def test_hydration_health_conditions() -> None:
    # Test for someone with diabetes (requires more water)
    result = calculate_hydration(70, 'sedentary', 20, health_condition='diabetes')
    assert 'Your recommended daily water intake is' in result
    assert 'L' in result


def test_hydration_age() -> None:
    # Test for a child (age < 18)
    result = calculate_hydration(40, 'sedentary', 20, age=10)
    assert 'Your recommended daily water intake is' in result
    assert 'L' in result

    # Test for elderly (age > 65)
    result = calculate_hydration(70, 'sedentary', 20, age=70)
    assert 'Your recommended daily water intake is' in result
    assert 'L' in result


def test_hydration_gender() -> None:
    # Test for male (higher hydration needs)
    result = calculate_hydration(70, 'sedentary', 20, gender='male')
    assert 'Your recommended daily water intake is' in result
    assert 'L' in result

    # Test for female (slightly lower hydration needs)
    result = calculate_hydration(70, 'sedentary', 20, gender='female')
    assert 'Your recommended daily water intake is' in result
    assert 'L' in result


def test_hydration_time_of_day() -> None:
    # Test for hydration suggestion in the evening (adjusted for sleep)
    result = calculate_hydration(70, 'sedentary', 20, time_of_day='evening')
    assert 'Your recommended daily water intake is' in result
    assert 'L' in result


def test_hydration_high_intake() -> None:
    # Test for a high intake (athletic, high temperature, illness)
    result = calculate_hydration(70, 'athletic', 35, health_condition='ill')
    assert 'Your recommended daily water intake is' in result
    assert 'L' in result


def test_hydration_low_intake() -> None:
    # Test for low hydration suggestion (sedentary, low weight, and normal temperature)
    result = calculate_hydration(40, 'sedentary', 20)
    assert 'Your recommended daily water intake is' in result
    assert 'L' in result
    assert 'on the lower side' in result


def test_hydration_large_intake() -> None:
    # Test for high hydration suggestion (high weight and very active)
    result = calculate_hydration(120, 'athletic', 20)
    assert 'Your recommended daily water intake is' in result
    assert 'L' in result
    assert 'high water intake' in result
