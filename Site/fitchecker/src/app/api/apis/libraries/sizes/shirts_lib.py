from typing import List, Dict, Union, Tuple
from dataclasses import dataclass
import json
from enum import Enum

class SizeLabel(Enum):
    XS = 1
    S = 2
    M = 3
    L = 4
    XL = 5
    XXL = 6

@dataclass
class SizeRange:
    label: str
    chest: List[int]
    waist: List[int]
    shoulder: List[int]

@dataclass
class Brand:
    brand: str
    sizes: List[SizeRange]

def load_size_data() -> List[Brand]:
    """Load and parse the size data from JSON."""
    with open('./data/size_data_shirts.json', 'r') as f:
        data = json.load(f)
    
    brands = []
    for brand_data in data:
        sizes = []
        for size in brand_data['sizes']:
            sizes.append(SizeRange(
                label=size['label'],
                chest=size['chest'],
                waist=size['waist'],
                shoulder=size['shoulder']
            ))
        brands.append(Brand(brand=brand_data['brand'], sizes=sizes))
    return brands

def find_size_category(measurement: int, ranges: List[List[int]]) -> List[int]:
    """Find matching size indices for a given measurement."""
    matching_sizes = []
    for i, (min_val, max_val) in enumerate(ranges):
        if min_val <= measurement <= max_val:
            matching_sizes.append(i)
    return matching_sizes

def get_best_size(brand_name: str, chest: int, waist: int, shoulder: int) -> Tuple[str, Dict[str, str]]:
    """
    Determine the best size for given measurements and brand.
    
    Args:
        brand_name (str): Name of the brand (e.g., "Zara", "H&M", "Dior")
        chest (int): Chest measurement in centimeters
        waist (int): Waist measurement in centimeters
        shoulder (int): Shoulder measurement in centimeters
    
    Returns:
        Tuple[str, Dict[str, str]]: Recommended size label and detailed fit information
    """
    brands = load_size_data()
    
    # Find the brand
    brand = next((b for b in brands if b.brand.lower() == brand_name.lower()), None)
    if not brand:
        raise ValueError(f"Brand '{brand_name}' not found")
    
    # Get all size ranges for the brand
    chest_ranges = [size.chest for size in brand.sizes]
    waist_ranges = [size.waist for size in brand.sizes]
    shoulder_ranges = [size.shoulder for size in brand.sizes]
    
    # Find matching sizes for each measurement
    chest_sizes = find_size_category(chest, chest_ranges)
    waist_sizes = find_size_category(waist, waist_ranges)
    shoulder_sizes = find_size_category(shoulder, shoulder_ranges)
    
    # If any measurement doesn't fit in any range
    if not chest_sizes or not waist_sizes or not shoulder_sizes:
        measurements_info = {
            "chest": "too small" if chest < chest_ranges[0][0] else "too large" if chest > chest_ranges[-1][1] else "ok",
            "waist": "too small" if waist < waist_ranges[0][0] else "too large" if waist > waist_ranges[-1][1] else "ok",
            "shoulder": "too small" if shoulder < shoulder_ranges[0][0] else "too large" if shoulder > shoulder_ranges[-1][1] else "ok"
        }
        return "No exact fit", measurements_info
    
    # Calculate the average size index
    all_indices = chest_sizes + waist_sizes + shoulder_sizes
    avg_size_index = round(sum(all_indices) / len(all_indices))
    
    # Get the recommended size label
    recommended_size = brand.sizes[avg_size_index].label
    
    # Prepare detailed fit information
    fit_info = {
        "chest": "perfect" if avg_size_index in chest_sizes else "tight" if avg_size_index > max(chest_sizes) else "loose",
        "waist": "perfect" if avg_size_index in waist_sizes else "tight" if avg_size_index > max(waist_sizes) else "loose",
        "shoulder": "perfect" if avg_size_index in shoulder_sizes else "tight" if avg_size_index > max(shoulder_sizes) else "loose"
    }
    
    return recommended_size, fit_info

def print_size_recommendation(brand: str, chest: int, waist: int, shoulder: int) -> None:
    """
    Print a formatted size recommendation.
    
    Args:
        brand (str): Brand name
        chest (int): Chest measurement in cm
        waist (int): Waist measurement in cm
        shoulder (int): Shoulder measurement in cm
    """
    try:
        size, fit_info = get_best_size(brand, chest, waist, shoulder)
        print(f"\nSize Recommendation for {brand}:")
        print(f"Recommended size: {size}")
        print("\nFit Details:")
        print(f"Chest: {fit_info['chest']}")
        print(f"Waist: {fit_info['waist']}")
        print(f"Shoulder: {fit_info['shoulder']}")
    except ValueError as e:
        print(f"Error: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Example measurements
    print_size_recommendation("Zara", 95, 80, 43)  # Example measurements
