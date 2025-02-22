from typing import List, Dict, Tuple
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
    waist: List[int]
    hip: List[int]
    length: List[int]

@dataclass
class Brand:
    brand: str
    sizes: List[SizeRange]

def load_size_data() -> List[Brand]:
    """Load and parse the size data from JSON."""
    with open('./data/size_data_pants.json', 'r') as f:
        data = json.load(f)
    
    brands = []
    for brand_data in data:
        sizes = []
        for size in brand_data['sizes']:
            sizes.append(SizeRange(
                label=size['label'],
                waist=size['waist'],
                hip=size['hip'],
                length=size['length']
            ))
        brands.append(Brand(brand=brand_data['brand'], sizes=sizes))
    return brands

def find_size_category(measurement: int, ranges: List[List[int]]) -> List[int]:
    """Find matching size indices for a given measurement."""
    return [i for i, (min_val, max_val) in enumerate(ranges) if min_val <= measurement <= max_val]

def get_best_size(brand_name: str, waist: int, hip: int, length: int) -> Tuple[str, Dict[str, str]]:
    """
    Determine the best size for given measurements and brand.
    
    Args:
        brand_name (str): Name of the brand
        waist (int): Waist measurement in cm
        hip (int): Hip measurement in cm
        length (int): Pants length in cm
    
    Returns:
        Tuple[str, Dict[str, str]]: Recommended size label and detailed fit information
    """
    brands = load_size_data()
    
    brand = next((b for b in brands if b.brand.lower() == brand_name.lower()), None)
    if not brand:
        raise ValueError(f"Brand '{brand_name}' not found")
    
    waist_ranges = [size.waist for size in brand.sizes]
    hip_ranges = [size.hip for size in brand.sizes]
    length_ranges = [size.length for size in brand.sizes]
    
    waist_sizes = find_size_category(waist, waist_ranges)
    hip_sizes = find_size_category(hip, hip_ranges)
    length_sizes = find_size_category(length, length_ranges)
    
    if not waist_sizes or not hip_sizes or not length_sizes:
        measurements_info = {
            "waist": "too small" if waist < waist_ranges[0][0] else "too large" if waist > waist_ranges[-1][1] else "ok",
            "hip": "too small" if hip < hip_ranges[0][0] else "too large" if hip > hip_ranges[-1][1] else "ok",
            "length": "too short" if length < length_ranges[0][0] else "too long" if length > length_ranges[-1][1] else "ok"
        }
        return "No exact fit", measurements_info
    
    all_indices = waist_sizes + hip_sizes + length_sizes
    avg_size_index = round(sum(all_indices) / len(all_indices))
    
    recommended_size = brand.sizes[avg_size_index].label
    
    fit_info = {
        "waist": "perfect" if avg_size_index in waist_sizes else "tight" if avg_size_index > max(waist_sizes) else "loose",
        "hip": "perfect" if avg_size_index in hip_sizes else "tight" if avg_size_index > max(hip_sizes) else "loose",
        "length": "perfect" if avg_size_index in length_sizes else "short" if avg_size_index > max(length_sizes) else "long"
    }
    
    return recommended_size, fit_info

def print_size_recommendation(brand: str, waist: int, hip: int, length: int) -> None:
    """
    Print a formatted size recommendation.
    
    Args:
        brand (str): Brand name
        waist (int): Waist measurement in cm
        hip (int): Hip measurement in cm
        length (int): Pants length in cm
    """
    try:
        size, fit_info = get_best_size(brand, waist, hip, length)
        print(f"\nSize Recommendation for {brand}:")
        print(f"Recommended size: {size}")
        print("\nFit Details:")
        print(f"Waist: {fit_info['waist']}")
        print(f"Hip: {fit_info['hip']}")
        print(f"Length: {fit_info['length']}")
    except ValueError as e:
        print(f"Error: {str(e)}")

# Example usage
if __name__ == "__main__":
    print_size_recommendation("Zara", 80, 95, 105)
