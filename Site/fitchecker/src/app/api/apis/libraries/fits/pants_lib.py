from dataclasses import dataclass

@dataclass
class PantsMeasurements:
    waist: float    # in cm
    hips: float     # in cm
    leg_length: float  # in cm

def determine_fit(measurements: PantsMeasurements) -> str:
    """
    Determine the general fit for pants based on waist, hips, and leg length measurements.
    
    The algorithm uses two ratios:
      - Waist-to-Hips Ratio: Lower ratios typically suggest a more tapered (slim) waist.
      - Leg-to-Hips Ratio: Higher values indicate longer legs relative to hip size.
    
    Assumed thresholds for demonstration purposes:
      - Slim Fit: if waist/hips < 0.80 and leg_length/hips >= 1.15
      - Regular Fit: if 0.80 <= waist/hips <= 0.90 and 1.05 <= leg_length/hips < 1.15
      - Loose Fit: otherwise
    
    Args:
        measurements (PantsMeasurements): The measurements for waist, hips, and leg length.
        
    Returns:
        str: A recommendation of 'Slim Fit', 'Regular Fit', or 'Loose Fit'.
    """
    waist_to_hip = measurements.waist / measurements.hips
    leg_to_hip = measurements.leg_length / measurements.hips

    if waist_to_hip < 0.80 and leg_to_hip >= 1.15:
        return "Slim Fit"
    elif 0.80 <= waist_to_hip <= 0.90 and 1.05 <= leg_to_hip < 1.15:
        return "Regular Fit"
    else:
        return "Loose Fit"

def get_fit(waist: float, hips: float, leg_length: float) -> str:
    """
    Get a fit recommendation for pants based on input measurements.
    
    Args:
        waist (float): Waist measurement in cm.
        hips (float): Hip measurement in cm.
        leg_length (float): Leg length measurement in cm.
        
    Returns:
        str: The recommended pants fit category.
    """
    measurements = PantsMeasurements(waist=waist, hips=hips, leg_length=leg_length)
    return determine_fit(measurements)

if __name__ == "__main__":
    try:
        waist_input = float(input("Enter your waist measurement (cm): "))
        hips_input = float(input("Enter your hip measurement (cm): "))
        leg_length_input = float(input("Enter your leg length measurement (cm): "))
    except ValueError:
        print("Please enter valid numeric values.")
        exit(1)
    
    recommended_fit = get_fit(waist_input, hips_input, leg_length_input)
    print(f"Based on your measurements, your recommended fit for pants is: {recommended_fit}")
