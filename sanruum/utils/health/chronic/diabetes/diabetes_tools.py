from __future__ import annotations

from sqlalchemy.orm import Session

from sanruum.database.core.db import SessionLocal
from sanruum.database.managers.user_manager import UserManager
from sanruum.database.repository import get_user

# Instantiate (this could be done at a higher level in your application)
user_manager = UserManager()


def calculate_blood_sugar_level(
        blood_sugar: float,
) -> str:
    """
    This function checks if the blood sugar level is within a safe range (in mmol/L).
    The general ranges are:
    - Hypoglycemia: Below 3.9 mmol/L
    – Normal: Between 3.9 and 7.8 mmol/L
    – Hyperglycemia: Above 7.8 mmol/L.

    Args:
        blood_sugar (float): The current blood sugar level in mmol/L.

    Returns:
        str: A message indicating whether the level is 'normal', 'high', or 'low'.
    """
    if blood_sugar < 3.9:
        return 'Your blood sugar is low. Please take necessary action to raise it.'
    elif 3.9 <= blood_sugar <= 7.8:
        return 'Your blood sugar is in healthy range.'
    else:
        return 'Your blood sugar is high. Please take necessary action to lower it.'


def carb_counting(
        carb_intake: float,
        meal_type: str = 'meal',
        user_id: int | None = None,
) -> str:
    """
    Estimates carbohydrate intake and provides feedback
        based on standard recommendations.
    Optionally uses user-specific data to adjust thresholds.
    """
    if carb_intake < 0:
        return 'Invalid carbohydrate amount. Please enter a positive value.'

    meal_type = meal_type.lower()

    # Default recommended ranges
    recommended_meal_low, recommended_meal_high = 45, 60
    recommended_snack_low, recommended_snack_high = 15, 30

    # Override with user-specific data if available
    if user_id is not None:
        user = user_manager.get_user(user_id)
        if user:
            recommended_meal_low, recommended_meal_high = user.get(
                'meal_carb_range', (45, 60),
            )
            recommended_snack_low, recommended_snack_high = user.get(
                'snack_carb_range', (15, 30),
            )
    if meal_type == 'meal':
        if carb_intake <= recommended_meal_low:
            return (
                f'Your carbohydrate intake of {carb_intake}g is on the lower '
                f'side for a meal. Consider adding more healthy carbs (e.g., '
                f' whole grains, fruits).'
            )
        elif recommended_meal_low < carb_intake <= recommended_meal_high:
            return (
                f'Your carbohydrate intake of '
                f'{carb_intake}g is within the optimal range for a meal.'
            )
        else:
            return (
                f'Your carbohydrate intake of {carb_intake}g is high for a '
                f'meal. Consider reducing portion sizes or balancing with '
                f'protein and fiber.'
            )

    elif meal_type == 'snack':
        if carb_intake <= recommended_snack_low:
            return (
                f'Your carbohydrate intake of '
                f'{carb_intake}g is on the lower side for a snack.'
            )
        elif recommended_snack_low < carb_intake <= recommended_snack_high:
            return (
                f'Your carbohydrate intake of '
                f'{carb_intake}g is within the optimal range for a snack.'
            )
        else:
            return (
                f'Your carbohydrate intake of {carb_intake}g is high for a '
                f'snack. Consider choosing a lighter snack option.'
            )

    return "Invalid meal type. Please specify 'meal' or 'snack'."


def insulin_calculation(
        blood_sugar: float,
        carb_intake: float,
        user_id: int | None = None,
        target_bg: float = 5.5,
        insulin_to_carb_ratio: float = 10,
        correction_factor: float = 2,
        time_of_day: str = 'afternoon',
        recent_exercise: bool = False,
        meal_glycemic_index: float | None = None,
        round_increment: float = 0.5,
) -> float:
    """
    Calculates the total insulin dose required based on the current
       blood sugar and carbohydrate intake.
    If a user_id is provided, personalized settings from the user
       profile will override defaults.


    Uses the formulas:
        - Meal bolus = carb_intake / insulin_to_carb_ratio
        - Correction bolus = (
              (blood_sugar - target_bg) /
              correction_factor, if blood_sugar >
              target_bg; otherwise 0.
              )
        - Total insulin dose = meal bolus + correction bolus
    Args:
        blood_sugar (float): The current blood sugar level in mmol/L.
        carb_intake (float): Carbohydrate intake in grams.
        user_id (int, optional): The unique identifier of the user.
            If provided, personalized settings will override defaults.

        target_bg (float, optional): Target blood sugar level (mmol/L).
            Default is 5.5.
        insulin_to_carb_ratio (float, optional): Grams of carbohydrate per
            unit of insulin. Default is 10.
        correction_factor (float, optional):
            How many mmol/L above target are reduced by one unit of insulin.
            Default is 2.
        time_of_day (str, optional): Time of day (morning, afternoon, evening).
            Default is 'afternoon'.
        recent_exercise (bool, optional):
            Whether the user has exercised recently (reduces correction dose).
            Default is False.
        meal_glycemic_index (float, optional):

            Glycemic index of the meal; if high, may increase required insulin.
        round_increment (float, optional): The increment to rounded to the
            specified increment.

    Returns:
        float: The total insulin dose (in units), rounded to two decimal places.
    """
    # Input validation
    if blood_sugar < 0 or carb_intake < 0:
        raise ValueError(
            'Blood sugar and carbohydrate intake must be non-negative.',
        )
    if insulin_to_carb_ratio <= 0 or correction_factor <= 0:
        raise ValueError(
            'Insulin to carb ratio and correction factor must be positive.',
        )

    # If user_id is provided, try to load personalized settings
    if user_id:
        db: Session = SessionLocal()
        user = get_user(db, user_id)
        if user and user.profile:
            insulin_to_carb_ratio = user.profile.insulin_to_carb_ratio
            correction_factor = user.profile.correction_factor
            target_bg = user.profile.target_bg
        db.close()

    # Meal bolus calculation
    meal_bolus = carb_intake / insulin_to_carb_ratio

    # Adjust meal bolus based on the glycemic index of the meal if provided
    if meal_glycemic_index is not None:
        if meal_glycemic_index > 70:
            meal_bolus *= 1.1
        elif meal_glycemic_index < 55:
            meal_bolus *= 0.9

    # Correction bolus calculation
    correction_bolus = 0.0
    if blood_sugar > target_bg:
        correction_bolus = (blood_sugar - target_bg) / correction_factor

    # Adjust correction_bolus based on time of day
    time_adjustments = {'morning': 1.2, 'afternoon': 1.0, 'evening': 0.9}
    correction_bolus *= time_adjustments.get(time_of_day.lower(), 1.0)

    # Reduce correction bolus if recent exercise was performed
    if recent_exercise:
        correction_bolus *= 0.9

    total_dose = meal_bolus + correction_bolus

    # Safety check and rounding
    if total_dose > 15:
        print(
            'Warning: Calculated insulin dose is unusually high. '
            'Please consult your healthcare provider.',
        )
    rounded_dose = round(total_dose / round_increment) * round_increment

    return round(rounded_dose, 2)


def symptoms_checker(
        symptoms: list[str],
) -> str:
    """
    Checks if any symptoms match common diabetes-related symptoms.

    Args:
        symptoms (list[str]): A list of symptom descriptions.

    Returns:
        str: A message indicating whether common diabetes-related symptoms
            were detected.
    """
    # Define a set of common diabetes-related symptoms.
    common_symptoms = {
        'increased thirst',
        'frequent urination',
        'fatigue',
        'blurred vision',
        'unexplained weight loss',
        'slow healing wounds',
        'tingling or numbness in hands or feet',
        'hunger',
        'dry mouth',
        'headache',
        'irritability',
        'frequent infections',
    }

    # Normalize input symptoms (lowercase and strip whitespace)
    normalized_input = (s.lower().strip() for s in symptoms)

    # Identify matches using simple substring matching
    detected = []
    for input_symptom in normalized_input:
        for common in common_symptoms:
            # If the input symptom is a substring of a common symptom or vice versa
            if input_symptom in common or common in input_symptom:
                detected.append(common)

    # Remove duplicates
    detected = list(set(detected))

    if detected:
        return (
            f'The following symptoms are commonly associated with diabetes: '
            f"{', '.join(detected)}. Please consult your healthcare provider "
            f'for an accurate diagnosis.'
        )
    else:
        return (
            'The reported symptoms do not appear to match common diabetes-related '
            'symptoms. If you feel unwell, please consult a healthcare provider.'
        )


def blood_sugar_trend_analysis(
        blood_sugar_readings: list[float],
) -> str:
    """
    Analyzes blood sugar trends over time by calculating the average change
        between readings.

    Args:
        blood_sugar_readings (list[float]): A list of blood sugar readings
            in mmol/L.

    Returns:
        str: A message indicating whether the blood sugar trend is rising,
            dropping, or steady, along with the average change per reading.
    """
    if len(blood_sugar_readings) < 2:
        return 'Not enough data to analyze trends.'

    # Calculate differences between consecutive readings
    differences = [
        blood_sugar_readings[i + 1] - blood_sugar_readings[i]
        for i in range(len(blood_sugar_readings) - 1)
    ]

    average_diff = sum(differences) / len(differences)
    # Define a threshold below which the change is considered negligible
    threshold = 0.1  # mmol/L per reading

    if average_diff > threshold:
        trend = 'rising'
    elif average_diff < -threshold:
        trend = 'dropping'
    else:
        trend = 'steady'
    return (
        f'Your blood sugar trend is {trend} (average change: {average_diff:.2f} '
        f'mmol/L per reading).'
    )


def exercise_impact_on_blood_sugar(
        exercise_type: str,
        intensity: str,
) -> str:
    """
    Estimates how physical activity might affect blood sugar levels based on
        exercise type and intensity.

    Args:
        exercise_type (str): Type of exercise (e.g., 'aerobic', 'resistance',
            'hiit').
        intensity (str): Intensity level (e.g., low, moderate, high).

    Returns:
        str: A message describing the estimated impact on blood sugar levels.
    """
    # Normalize input
    exercise_type = exercise_type.lower().strip()
    intensity = intensity.lower().strip()

    impact_messages = {
        'aerobic': {
            'low': 'Low-intensity aerobic exercise may lead to a slight '
                   'decrease in blood sugar level.\n',
            'moderate': 'Moderate-intensity aerobic exercise is likely to help '
                        'lower blood sugar levels steadily.\n',
        },

        'resistance': {
            'low': 'Low-intensity resistance training might have minimal '
                   'effect on blood sugar levels\n but it still contribute to '
                   'overall metabolic health.',
            'moderate': 'Moderate-intensity resistance training ',
            'high': 'High-intensity resistance training can  initially cause '
                    'slight increase in blood sugar due stress hormones, '
                    'followed by stabilization as your muscles use glucose '
                    'for recovery.',
        },
        'hiit': {
            'low': 'Even low-intensity HIIT can cause notable fluctuations '
                   "in blood sugar levels.\nMonitor closely if you're new to "
                   'this type of exercise.',
            'moderate': 'Moderate HIIT is likely to result in significant '
                        'blood sugar reduction during recovery phases.',
            'high': 'High-intensity HIIT may lead to rapid decreases in '
                    'blood sugar levels, with a risk of hypoglycemia.\n'
                    'It is essential to have a plan to manage your glucose '
                    'levels before, during, and after exercise.',
        },
    }

    # Normalize synonyms
    synonyms = {
        'cardio': 'aerobic',
        'strength': 'resistance',
        'high-intensity interval training': 'hiit',
    }
    exercise_type = synonyms.get(exercise_type, exercise_type)

    # Get the appropriate message
    message = impact_messages.get(exercise_type, {}).get(intensity)

    if message:
        return message
    elif exercise_type not in impact_messages:
        return (
            'Exercise type not recognized. Please specify "aerobic", '
            '"resistance", or "hiit" for accurate assessment.'
        )
    else:
        return (
            f'Unknown intensity level for {exercise_type}. '
            f"Please specify 'low', 'moderate', or 'high'."
        )


def diet_recommendations(
        blood_sugar_level: float,
        user_id: int | None = None,
) -> str:
    """

    Recommends low-carb or diabetes-friendly foods based on blood sugar levels.
    Optionally uses user-specific dietary preferences if provided.
    """
    # Default recommendations
    if blood_sugar_level < 3.9:
        recommendation = (
            'Consider consuming a small, balanced snack to help '
            'you blood sugar.'
        )
    elif 3.9 <= blood_sugar_level <= 7.8:
        recommendation = (
            'Your blood sugar is in a healthy range. Focus on balanced '
            'meals rich in fiber, lean proteins, and healthy fats.'
        )
    else:
        recommendation = (
            'High blood sugar detected. Consider a low-carb meal to help '
            'stabilize your levels.'
        )

    # If user_id is provided, you could adjust the recommendation based on user
    # dietary preferences.
    if user_id:
        user = user_manager.get_user(user_id)
        if user:
            # For example, if user has a known preference or a prescribed diet,
            # incorporate that. This is illustrative; real logic would use more
            # detailed user dietary data.
            recommendation += (
                '(Personalized dietary adjustments have been applied based'
                ' on your profile.)'
            )

    return recommendation


def medication_reminder(
        medication_schedule: dict,
        user_id: int | None = None,
) -> str:
    """
    Helps user track and reminds them of their insulin or medication schedule.
    If user_id provided, the function can pull the user's personalized.
    """
    # If user_id is provided, override the default medication_schedule with
    # the user's data
    if user_id:
        user = user_manager.get_user(user_id)
        # Make sure medication_schedule exists
        if user and hasattr(user, 'medication_schedule'):
            medication_schedule = user.medication_schedule or {}

    # For now, simply return a summary of the provided schedule.
    if not medication_schedule:
        return 'No medication schedule available. Please update your schedule.'

    reminders = []
    for time, medication in medication_schedule.items():
        reminders.append(f'At {time}, take {medication}.')
    return 'Medication reminder:\n' + '\n'.join(reminders)


def glucose_level_predictor(
        time_of_day: str,
        recent_meal: str,
        activity: str,
        user_id: int | None = None,
) -> float:
    """
    Predicts glucose levels based on time of day, meal type, and recent activity.
    Optionally uses user-specific data to adjust predictions.


    Args:
         time_of_day (str): Time of day ('morning', 'afternoon', 'evening').
         recent_meal (str):Description of the recent meal
            (e.g., "high-carb", “balanced”, “low-carb”, “fasting”).
        activity (str): Recent activity
            ('exercise', 'active', 'sedentary', etc.).
        user_id (str):

    Returns:
        float: Predicted glucose levels in mmol/L.
    """
    # Base glucose level (target level)
    predicted_glucose = 5.5

    # Time-of-day adjustments
    t = time_of_day.lower().strip()
    if t == 'morning':
        predicted_glucose += 1.0  # Consider the dawn phenomenon
    elif t == 'afternoon':
        predicted_glucose += 0.5
    elif t == 'evening':
        predicted_glucose -= 0.5

    # Meal impact adjustment
    meal = recent_meal.lower().strip()
    if 'high-carb' in meal:
        predicted_glucose += 2.0
    elif 'balanced' in meal:
        predicted_glucose += 1.0
    elif 'low-carb' in meal:
        predicted_glucose += 0.5
    elif 'fasting' in meal or 'none' in meal:
        predicted_glucose -= 0.5

    # Activity impact adjustments
    act = activity.lower().strip()
    if 'exercise' in act or 'active' in act:
        predicted_glucose -= 1.0
    elif 'sedentary' in act:
        predicted_glucose += 0.5

    # Use user-specific adjustments if available
    if user_id:
        user = user_manager.get_user(user_id)
        if user:
            # Example: adjust prediction if user's target_bg is different
            predicted_glucose = (predicted_glucose + user.target_bg) / 2

    return round(predicted_glucose, 2)


def emergency_help(
        blood_sugar_level: float,
) -> str:
    """
    Provides emergency instructions if the user experiences extreme hypo- or
     hyperglycemia symptoms.

    Args:
        blood_sugar_level (float): The user's current blood sugar level
         in mmol/L.

    Returns:
        str: Emergency instructions based on the blood sugar level.
    """
    if blood_sugar_level < 3.00:
        return (
            '🚨 **Severe Hypoglycemia Alert!**\n'
            '- Consume 15-20g of fast-acting carbs (e.g., glucose tablets, '
            'juice, regular soda).\n'
            '- Recheck blood sugar in 15 minutes.\n'
            '- If still low, repeat the process.\n'
            '- **Seek emergency medical assistance if unconscious or unable '
            'to consume glucose.**'
        )

    elif 3.00 <= blood_sugar_level <= 3.9:
        return (
            '✅ **Your blood sugar is within the target range.** No '
            'emergency action needed.'
        )

    elif 10.00 < blood_sugar_level <= 13.8:
        return (
            '⚠️ **Moderate Hyperglycemia Warning.**\n'
            '- Drink water to stay hydrated.\n'
            '- If prescribed, take insulin as directed.\n'
            '- Engage in light physical activity if safe.\n'
            '- Monitor blood sugar levels regularly.'
        )
    else:
        return (
            '🚨 **Severe Hyperglycemia Alert!**\n'
            '- Check for ketones if possible.\n'
            '- Drink water and avoid carbohydrate-heavy foods.\n'
            '- If ketones are present or symptoms worsen (e.g., nausea, '
            'vomiting, confusion), '
            'seek **immediate** medical help.\n'
            '- Contact a healthcare provider or go to the emergency room if '
            'blood sugar remains high despite treatment.'
        )


def sleep_impact_on_blood_sugar(
        sleep_duration: float,
        sleep_quality: str,
) -> str:
    """
    Analyzes the impact of sleep duration and quality on blood sugar levels.

    Args:
        sleep_duration (float): The total hours of sleep.
        sleep_quality (str): A descriptor
            for sleep quality (e.g., 'poor', 'fair', 'good', 'excellent').

    Returns:
        str: A message describing how your sleep might be impacting your
         blood sugar levels.
    """
    # Normalize sleep quality
    sleep_quality = sleep_quality.lower().strip()

    # Assess sleep duration
    if sleep_duration < 6:
        duration_assessment = 'insufficient'
    elif 6 <= sleep_duration < 7:
        duration_assessment = 'borderline insufficient'
    elif 7 <= sleep_duration <= 9:
        duration_assessment = 'optimal'
    else:
        duration_assessment = 'excessive'

    # Assess sleep quality
    if sleep_quality in ['poor', 'bad']:
        quality_assessment = 'poor'
    elif sleep_quality in ['fair', 'average']:
        quality_assessment = 'average'
    elif sleep_quality in ['good', 'excellent']:
        quality_assessment = 'good'
    else:
        quality_assessment = 'unknown'

    # Combine assessments to generate a tailored message
    if duration_assessment == 'optimal' and quality_assessment == 'good':
        return (
            'Your sleep duration and quality are optimal, which likely '
            'supports stable blood sugar levels.'
        )

    elif duration_assessment in ['insufficient', 'borderline insufficient']:
        return (
            f'Your sleep duration is {duration_assessment}, which may '
            f'contribute to elevated blood sugar levels. Consider '
            f'adjusting your sleep schedule to aim for 7-9 hours of '
            f'quality sleep.'
        )
    elif duration_assessment == 'excessive':
        return (
            'Your sleeping more than the typically recommended duration. '
            'While adequate sleep is important, excessive sleep may '
            'sometimes be linked with irregular blood sugar levels. '
            'Aim for a balanced schedule.'
        )

    elif duration_assessment == 'poor':
        return (
            'Poor sleep quality can adversely affect blood sugar control. '
            'Consider adopting better sleep hygiene practices to improve '
            'your sleep quality.'
        )
    else:
        return (
            'Your sleep pattern appears variable. Monitoring and improving '
            'both duration and quality may help in stabilizing your '
            'blood sugar levels.'
        )


def stress_impact_on_blood_sugar(
        stress_level: str,
) -> str:
    """
    Assesses the impact of stress on blood sugar
     levels based on the reported stress level.

    Args:
        stress_level (str): A descriptor of stress level
            (e.g., 'low', 'moderate', 'high').

    Returns:
        str: A message indicating the potential impact of stress
         ``  on blood sugar and suggestion for management.
             ("The provided stress level is not recognized."
             " Please specify 'low', 'moderate', or 'high' for a correct assessment.")
    """
    # Normalize input
    stress_level = stress_level.lower().strip()

    # Define messages for various stress levels
    messages = {
        'low': (
            'Your stress level is low, which is unlikely'
            ' to have significant impact on your blood sugar levels. '
            'Keep up with your stress management practices.'
        ),
        'moderate': (
            'High stress levels can lead to a noticeable increase in'
            ' blood sugar levels due to stress hormones. '
            'It is recommended to practice stress-reducing activities'
            ' like meditation, exercise, or speaking with a professional. '
            'If high stress persists, consider consulting'
            ' your healthcare provider for further'
        ),
    }

    # Return the corresponding message or a default message
    # if the stress level is not recognized
    return messages.get(
        stress_level,
        'The provided stress level is not recognized. '
        "Please specify 'low', 'moderate', or 'high' for an accurate assessment.",

    )


def estimate_hba1c(
        blood_sugar_readings: list[float],
) -> float:
    """
    Estimates HbA1c (%) based on blood sugar readings in mmol/L.

    The formula used is:
        1. Calculate the average blood glucose (mmol/L).
        2. Convert the average to mg/dL by multiplying by 18.
        3. Estimate HbA1c using: HbA1c (%) = (avg_mg/dL + 46.7) / 28.7
    Args:
        blood_sugar_readings (list[float]): A list of blood sugar readings in mmol/L.

    Returns:
        float: The estimated HbA1c value, rounded to two decimal places.
    """
    if not blood_sugar_readings:
        raise ValueError(
            'At least one blood sugar reading is required to estimate HbA1c',
        )

    avg_mmol = sum(blood_sugar_readings) / len(blood_sugar_readings)
    avg_mg_dl = avg_mmol * 18  # Convert mmol/L to mg/dL.
    hba1c = (avg_mg_dl + 46.7) / 28.7
    return round(hba1c, 2)


def get_hba1c_trend(
        user_id: int | None,
) -> str:
    """
    Retrieves HbA1c trend data for a specific
        user by analyzing historical HbA1c readings.

    This placeholder function simulates data retrieval and determines
        if the HbA1c values are improving, worsening, or remaining stable over time.

    Args:
        user_id (int): The user's identifier.

    Returns:
        str: A message describing the HbA1c trend.
    """

    # Ensure user_id is not None before attempting to fetch user data
    if user_id is None:
        return 'User ID is required to retrieve HbA1c data.'

    readings = user_manager.get_user(user_id)

    if readings is None:
        return 'Not enough HbA1c data to analyze trend.'

    # Compare the first and last reading to determine the trend
    first_reading = readings[0]
    latest_reading = readings[-1]

    if latest_reading < first_reading:
        trend = 'improving'
    elif latest_reading > first_reading:
        trend = 'worsening'
    else:
        trend = 'stable'

    return f'Your HbA1c trend is {trend} based on your recent readings.'


def log_blood_sugar(
        reading: float,
        timestamp: str,
) -> None:
    """
    """


def get_blood_sugar_history(
        user_id: str,
) -> None:
    """
    """
    pass


def get_blood_sugar_trend(
        user_id: str,
) -> None:
    """
    """
    pass


def calculate_insulin_sensitivity_factor(
        weight: float,
        age: int,
) -> None:
    """
    """
    pass


def calculate_insulin_to_carb_ratio(
        total_daily_insulin: float,
        total_daily_carbs: float,
) -> None:
    """
    """
    pass
