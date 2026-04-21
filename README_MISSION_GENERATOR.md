# DCS Dynamic Mission Generator

A Python-based mission generator for DCS (Digital Combat Simulator) that creates zone-based combat missions with dynamic unit spawning.

## Features

- **Zone-Based Combat**: Missions are divided into multiple geographic zones (16 zones by default)
- **Dynamic Unit Spawning**: Each zone generates 20-30 randomly positioned units
- **Coalition Forces**: Red forces (Russian tanks & APCs) defend while Blue forces (US tanks & vehicles) attack
- **Scalable Difficulty**: Easy to adjust unit counts, zone sizes, and number of active zones
- **Multiple Terrains**: Supports Caucasus, Nevada, Syria, Persian Gulf, and Mariana Islands
- **Modular Design**: Well-organized code for easy customization

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup

```bash
# Install required dependencies
pip install pydcs

# Navigate to the mission generator directory
cd path/to/mission_generator
```

## Usage

### Basic Mission Generation

```bash
python mission_generator.py
```

This generates a mission with:
- Terrain: Caucasus
- Active Zones: 3 (randomly selected from 16 total)
- Output: `goon_coldwar_dynamic.miz` (DCS mission file)

### Customizing Mission Generation

Edit `mission_generator.py` to customize the mission:

```python
# In the main() function:
def main():
    script_dir = Path(__file__).parent
    output_mission = script_dir / "my_custom_mission.miz"
    
    # Choose terrain: 'caucasus', 'nevada', 'syria', 'gulf', 'marianas'
    generator = DynamicMissionGenerator(str(output_mission), terrain_name='nevada')
    
    # Generate mission with N active zones
    success = generator.generate_mission(num_active_zones=5)
    
    return 0 if success else 1
```

## Configuration

### Adjusting Unit Counts

To change the unit count per zone, modify the `MissionZone` class:

```python
class MissionZone:
    def __init__(self, zone_id, center_x, center_y, size=20000):
        # Change the range (20, 30) to your desired min/max units
        self.units_count = random.randint(20, 30)
```

### Adjusting Zone Grid

Change grid properties in the main function or `ZoneGridSystem` class:

```python
# In _initialize_zone_grid()
self.zone_grid = ZoneGridSystem(
    map_width, 
    map_height,
    zone_size=40000,  # Size of each zone in meters
    zones_per_row=5   # Number of zones per row
)
```

### Vehicle Types

Modify the vehicle lists to use different unit types:

```python
RED_VEHICLES = [
    Armor.T_90,        # Soviet main battle tank
    Armor.T_80B,       # Soviet main battle tank
    Armor.T_72B,       # Soviet main battle tank
    Armor.BMP_3,       # Soviet infantry fighting vehicle
    Armor.BMP_2,       # Soviet infantry fighting vehicle
]

BLUE_VEHICLES = [
    Armor.M_1_Abrams,      # US main battle tank
    Armor.M1128_Stryker_MGS,  # US tank destroyer
    Armor.M1045_HMMWV_TOW,    # US HMMWV with TOW missiles
]
```

## Mission Structure

### Zones
- **Total Zones**: 16 (arranged in a grid across the map)
- **Active Zones**: 3 (randomly selected per mission generation)
- **Zone Size**: Approximately 16km radius per zone
- **Units per Zone**: 20-30 random units

### Forces
- **Red Force** (Defending):
  - 20-30 units per zone
  - Mix of tanks and APCs
  - Positioned randomly within the zone

- **Blue Force** (Attacking):
  - ~30% of Red force strength (6-9 units per zone)
  - Same vehicle types as Red (for simplicity, easily customizable)
  - Positioned randomly within the zone

### Terrain Map Sizes
- **Caucasus**: 180km x 180km
- **Nevada**: 200km x 200km
- **Syria**: 200km x 200km
- **Persian Gulf**: Variable
- **Mariana Islands**: Variable

## Output

The script generates a `.miz` file which is a DCS mission package. The file can be:
- Directly opened in DCS World
- Placed in your DCS Missions folder
- Edited in the DCS Mission Editor for further customization

### Typical Output
```
============================================================
GENERATING DYNAMIC MISSION
============================================================
Creating mission on terrain: caucasus
Terrain: Caucasus
Map size estimate: 180km x 180km
Created 16 zones

Activating 3 zones as objectives

Zone 1: Zone(id=7, center=(100000.0, 60000.0), units=20)
  Added Red-Zone7 with 20 units
  Added Blue-Zone7 with 6 units
  
[... more zones ...]

Mission generation complete
Output: goon_coldwar_dynamic.miz
Total zones created: 16
Active zones: 3
```

## Example Custom Mission Generator

```python
#!/usr/bin/env python3
from mission_generator import DynamicMissionGenerator
from pathlib import Path

def create_intense_mission():
    """Create a high-intensity mission with 5 active zones"""
    script_dir = Path(__file__).parent
    output_path = script_dir / "intense_combat.miz"
    
    generator = DynamicMissionGenerator(str(output_path), terrain_name='caucasus')
    success = generator.generate_mission(num_active_zones=5)
    
    if success:
        print(f"Mission created: {output_path}")
        print("Load in DCS World and enjoy!")
    else:
        print("Failed to create mission")

if __name__ == "__main__":
    create_intense_mission()
```

## Troubleshooting

### "pydcs not installed" error
```bash
pip install pydcs
```

### Mission fails to open in DCS
- Ensure the generated `.miz` file is valid (check file size > 5KB)
- Try regenerating with a different terrain
- Check that DCS supports your chosen terrain

### Units not appearing in mission
- Verify the mission file opens in DCS (may need to run the scenario)
- Check that the zone coordinates are within the map bounds
- Ensure vehicle types are valid (check pydcs documentation)

## Extending the Generator

### Adding Custom Mission Objectives

```python
def add_mission_objectives(self):
    """Add custom objectives like destroy, protect, etc."""
    # Add custom objective logic here
    pass
```

### Adding Air Support

```python
def add_air_support(self, coalition_side="red"):
    """Add aircraft to provide support"""
    # Use mission.country().add_plane_group() or add_helicopter_group()
    pass
```

### Adding Weather Effects

```python
self.mission.weather.turbulence_to_max_alt = 2000  # Turbulence up to 2000m
self.mission.weather.wind.speed = 10  # 10 m/s wind
self.mission.weather.visibility.distance = 5000  # 5km visibility
```

## Performance Notes

- Small missions (1-3 zones): ~100-150 units total, minimal performance impact
- Medium missions (4-6 zones): ~200-300 units, moderate impact
- Large missions (8+ zones): 300+ units, noticeable impact on frame rates

Adjust zone size and unit counts based on your system performance.

## License

This script uses pydcs (LGPL v3). Refer to the pydcs repository for licensing details.

## Useful Resources

- [pydcs Documentation](https://github.com/pydcs/dcs)
- [DCS World Community Wiki](https://wiki.hoggitworld.com/)
- [DCS Scripting Guide](https://wiki.hoggitworld.com/view/Scripting)

## Future Enhancements

- [ ] Support for different mission types (CAS, CAP, SEAD, etc.)
- [ ] Dynamic unit reinforcements during mission
- [ ] Air defense systems (SAMs, AAA)
- [ ] Mission briefing generation with map markers
- [ ] Randomized vehicle loadouts
- [ ] Support for custom vehicle mixes per faction
- [ ] Integration with popular mission mods

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review pydcs documentation
3. Examine the generated `.miz` file structure
4. Consider joining DCS community forums for additional help
