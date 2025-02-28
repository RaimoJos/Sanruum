from __future__ import annotations


def calculate_hydration(
        weight_kg: float,
        activity_level: str,
        temperature: float = 20,
        health_condition: str = '',
        age: int = 30,
        gender: str = 'male',
        time_of_day: str = 'morning',
) -> str:
    """
    Calculate the recommended daily water intake based on weight,
     activity level, temperature, health condition, age, gender, and time of day.

    Args:
        weight_kg (float): The user's weight in kilograms.
        activity_level (str):
            The activity level ("sedentary", "lightly_active",
             "moderately_active", "very_active", "athletic").
        temperature (float): The current temperature in Celsius (default: 20°C).
        health_condition (str):
            A health condition that affects hydration
             (e.g., "diabetes", "pregnant", "ill").
        age (int): The user's age.
        gender (str): The user's gender ("male" or "female").
        time_of_day (str): Time of day ("morning", "afternoon", "evening").

    Returns:
        str: A personalized recommendation message for daily water intake.
    """

    # Base water intake recommendation (30-35 mL per kg of body weight)
    base_intake = weight_kg * 30  # 30 mL per kg

    # Adjust base intake based on activity level
    if activity_level == 'sedentary':
        base_intake += 0  # no extra
    elif activity_level == 'lightly_active':
        base_intake += 300  # add 300 mL for lightly active
    elif activity_level == 'moderately_active':
        base_intake += 500  # add 500 mL for moderate activity
    elif activity_level == 'very_active':
        base_intake += 800  # add 800 mL for very active
    elif activity_level == 'athletic':
        base_intake += 1000  # add 1000 mL for athletic activity

    # Adjust for high temperatures
    if temperature > 30:
        base_intake += 500  # add 500 mL for hot weather

    # Adjust hydration for health conditions
    if health_condition == 'diabetes':
        base_intake += 300  # people with diabetes may need more hydration
    elif health_condition == 'pregnant':
        base_intake += 300  # pregnant women should drink more
    elif health_condition == 'ill':
        base_intake += 500  # illness can lead to dehydration, increase intake

    # Adjust for age and gender
    if age < 18:
        base_intake *= 0.8  # Children typically need less water
    elif age > 65:
        base_intake += 300  # Elderly people may need more hydration

    if gender == 'female':
        base_intake *= 0.9  # Women typically need slightly less water than men

    # Time of Day Adjustments
    if time_of_day == 'evening':
        # Reduce intake in the evening to prevent excessive night drinking
        base_intake -= 200

    # Hydration tips
    hydration_tip = ''
    if base_intake < 2000:
        hydration_tip = (
            'Your recommended intake is on the lower side. '
            'Make sure to drink water regularly!'
        )
    elif base_intake > 4000:
        hydration_tip = (
            "That's a high water intake. "
            'Ensure you spread your hydration throughout the day.'
        )

    # Format the response
    return (
        f'Your recommended daily water intake is '
        f'{base_intake / 1000:.2f} L. {hydration_tip} Stay hydrated!'
    )


# Example of using the function
print(
    calculate_hydration(
        weight_kg=63,
        age=37,
        activity_level='lightly_extra',
        temperature=24,
        gender='male',
        health_condition='diabetes',
    ),
)
