from dataclasses import dataclass

@dataclass
class BodyMeasurements:
    shoulder: float  # in cm
    chest: float     # in cm
    waist: float     # in cm

def determine_fit(measurements: BodyMeasurements) -> str:
    """
    Determine the general fit based on shoulder, chest, and waist measurements.
    
    The algorithm uses two simple ratios:
      - waist-to-chest ratio: a lower ratio suggests a more tapered torso (slim fit).
      - chest-to-shoulder ratio: a higher ratio suggests a broader chest relative to the shoulder,
        which is often associated with a slimmer profile.
    
    Thresholds (assumed for demonstration purposes):
      - Slim Fit: waist/chest < 0.85 and chest/shoulder >= 1.45
      - Regular Fit: waist/chest between 0.85 and 0.95 and chest/shoulder between 1.3 and 1.45
      - Loose Fit: any measurements outside the above ranges
    
    Args:
        measurements (BodyMeasurements): User measurements in centimeters.
    
    Returns:
        str: A recommendation of 'Slim Fit', 'Regular Fit', or 'Loose Fit'.
    """
    # Calculate ratios
    waist_chest_ratio = measurements.waist / measurements.chest
    chest_shoulder_ratio = measurements.chest / measurements.shoulder

    # Determine fit based on ratio thresholds
    if waist_chest_ratio < 0.85 and chest_shoulder_ratio >= 1.45:
        return "Slim Fit"
    elif 0.85 <= waist_chest_ratio <= 0.95 and 1.3 <= chest_shoulder_ratio < 1.45:
        return "Regular Fit"
    else:
        return "Loose Fit"

def get_fit(shoulder: float, chest: float, waist: float) -> str:
    """
    Get a fit recommendation based on input measurements.
    
    Args:
        shoulder (float): Shoulder measurement in cm.
        chest (float): Chest measurement in cm.
        waist (float): Waist measurement in cm.
    
    Returns:
        str: The recommended fit category.
    """
    measurements = BodyMeasurements(shoulder=shoulder, chest=chest, waist=waist)
    return determine_fit(measurements)

if __name__ == "__main__":
    # Example interactive usage:
    try:
        shoulder_input = float(input("Enter your shoulder measurement (cm): "))
        chest_input = float(input("Enter your chest measurement (cm): "))
        waist_input = float(input("Enter your waist measurement (cm): "))
    except ValueError:
        print("Please enter valid numeric values.")
        exit(1)
    
    recommended_fit = get_fit(shoulder_input, chest_input, waist_input)
    print(f"Based on your measurements, your recommended fit is: {recommended_fit}")
