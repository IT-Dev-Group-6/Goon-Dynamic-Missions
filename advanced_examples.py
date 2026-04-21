#!/usr/bin/env python3
"""
Advanced Mission Generation Examples
Shows how to customize and extend the mission generator
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from mission_generator import DynamicMissionGenerator, ZoneGridSystem, MissionZone
import random


def example_1_intense_mission():
    """Example 1: Create an intense mission with many zones and units"""
    print("\n" + "="*60)
    print("Example 1: Intense Combat Mission")
    print("="*60)
    
    script_dir = Path(__file__).parent
    output = script_dir / "intense_mission.miz"
    
    generator = DynamicMissionGenerator(str(output), terrain_name='caucasus')
    
    # Generate with 5 active zones instead of 3
    success = generator.generate_mission(num_active_zones=5)
    
    if success:
        print(f"✓ Mission saved to: {output}")
    else:
        print("✗ Failed to create mission")
    
    return success


def example_2_small_skirmish():
    """Example 2: Create a small skirmish with fewer units"""
    print("\n" + "="*60)
    print("Example 2: Small Skirmish Mission")
    print("="*60)
    
    script_dir = Path(__file__).parent
    output = script_dir / "skirmish_mission.miz"
    
    generator = DynamicMissionGenerator(str(output), terrain_name='caucasus')
    
    # Override zone configuration for smaller skirmish
    # Create a smaller zone grid
    generator.zone_grid = ZoneGridSystem(100000, 100000, zone_size=30000, zones_per_row=3)
    
    success = generator.generate_mission(num_active_zones=2)
    
    if success:
        print(f"✓ Mission saved to: {output}")
    else:
        print("✗ Failed to create mission")
    
    return success


def example_3_nevada_mission():
    """Example 3: Create a mission on the Nevada terrain"""
    print("\n" + "="*60)
    print("Example 3: Nevada Desert Mission")
    print("="*60)
    
    script_dir = Path(__file__).parent
    output = script_dir / "nevada_mission.miz"
    
    generator = DynamicMissionGenerator(str(output), terrain_name='nevada')
    success = generator.generate_mission(num_active_zones=4)
    
    if success:
        print(f"✓ Mission saved to: {output}")
    else:
        print("✗ Failed to create mission")
    
    return success


def example_4_custom_vehicles():
    """Example 4: Create mission with custom vehicle types"""
    print("\n" + "="*60)
    print("Example 4: Custom Vehicle Mission")
    print("="*60)
    
    from dcs.vehicles import Armor
    
    script_dir = Path(__file__).parent
    output = script_dir / "custom_vehicles_mission.miz"
    
    generator = DynamicMissionGenerator(str(output), terrain_name='caucasus')
    
    # Override vehicle types
    generator.RED_VEHICLES = [
        Armor.T_90,
        Armor.T_90,  # More T-90s
        Armor.BMP_3,
        Armor.BMP_2,
    ]
    
    generator.BLUE_VEHICLES = [
        Armor.M_1_Abrams,
        Armor.M_1_Abrams,  # All Abrams
    ]
    
    success = generator.generate_mission(num_active_zones=3)
    
    if success:
        print(f"✓ Mission saved to: {output}")
        print("  Vehicle mix: Russian T-90s vs US Abrams")
    else:
        print("✗ Failed to create mission")
    
    return success


def example_5_large_scale():
    """Example 5: Create a large-scale mission (warning: many units)"""
    print("\n" + "="*60)
    print("Example 5: Large-Scale Military Operation")
    print("="*60)
    
    script_dir = Path(__file__).parent
    output = script_dir / "large_scale_mission.miz"
    
    generator = DynamicMissionGenerator(str(output), terrain_name='caucasus')
    
    # Create more zones across the map
    generator.zone_grid = ZoneGridSystem(
        map_width=180000, 
        map_height=180000, 
        zone_size=25000,  # Smaller zones = more zones
        zones_per_row=7
    )
    
    success = generator.generate_mission(num_active_zones=8)
    
    if success:
        print(f"✓ Mission saved to: {output}")
        print(f"  Total zones: {len(generator.zone_grid.get_zones())}")
        print("  ⚠ Warning: This mission may have significant performance impact")
    else:
        print("✗ Failed to create mission")
    
    return success


def example_6_all_terrains():
    """Example 6: Generate missions for all supported terrains"""
    print("\n" + "="*60)
    print("Example 6: Multi-Terrain Mission Set")
    print("="*60)
    
    script_dir = Path(__file__).parent
    terrains = ['caucasus', 'nevada', 'syria', 'gulf', 'marianas']
    
    for terrain_name in terrains:
        output = script_dir / f"mission_{terrain_name}.miz"
        
        try:
            generator = DynamicMissionGenerator(str(output), terrain_name=terrain_name)
            success = generator.generate_mission(num_active_zones=2)
            
            if success:
                print(f"✓ {terrain_name.upper():12} mission saved")
            else:
                print(f"✗ {terrain_name.upper():12} mission failed")
        except Exception as e:
            print(f"✗ {terrain_name.upper():12} error: {e}")
    
    return True


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("DCS Mission Generator - Advanced Examples")
    print("="*60)
    print("\nThese examples show various ways to customize mission generation.")
    print("Choose one or run all by uncommenting in the main() function.\n")
    
    # Uncomment any examples you want to run:
    examples = [
        ("1 - Intense Mission", example_1_intense_mission),
        ("2 - Small Skirmish", example_2_small_skirmish),
        ("3 - Nevada Terrain", example_3_nevada_mission),
        ("4 - Custom Vehicles", example_4_custom_vehicles),
        ("5 - Large Scale", example_5_large_scale),
        ("6 - All Terrains", example_6_all_terrains),
    ]
    
    print("Available examples:")
    for desc, _ in examples:
        print(f"  {desc}")
    
    print("\n" + "-"*60)
    print("Running all examples...\n")
    
    results = []
    for desc, example_func in examples:
        try:
            result = example_func()
            results.append((desc, result))
        except Exception as e:
            print(f"\n✗ Error in {desc}: {e}")
            import traceback
            traceback.print_exc()
            results.append((desc, False))
    
    # Summary
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    
    successful = sum(1 for _, result in results if result)
    total = len(results)
    
    for desc, result in results:
        status = "✓" if result else "✗"
        print(f"{status} {desc}")
    
    print(f"\nCompleted: {successful}/{total} missions successfully generated")
    
    if successful == total:
        print("\n✓ All examples completed successfully!")
        print("\nYou can now open the generated .miz files in DCS World.")
        print("Check the script_dir for the mission files.")
    
    return 0 if successful == total else 1


if __name__ == "__main__":
    sys.exit(main())
