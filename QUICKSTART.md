# Quick Start Guide - DCS Mission Generator

## 5-Minute Setup

### 1. Install Python Requirements
```bash
pip install pydcs
```

### 2. Run the Generator
```bash
python mission_generator.py
```

This creates `goon_coldwar_dynamic.miz` with:
- 16 total zones across the map
- 3 active zones (randomly selected)
- 20-30 units per zone
- ~80-120 total units in the mission
- Red force (defending) vs Blue force (attacking)

### 3. Use in DCS
1. Copy the `.miz` file to your DCS Missions folder
2. Open DCS World
3. Load the mission from the mission list
4. Fly!

## What You Get

```
goon_coldwar_dynamic.miz (8-12 KB)
│
├─ Mission file with:
│  ├─ 16 geographical zones
│  ├─ 3 active combat zones  
│  ├─ ~60 Red units (T-90, T-80B, T-72B, BMP-2, BMP-3)
│  └─ ~20 Blue units (M-1 Abrams, Stryker MGS, HMMWV TOW)
│
└─ Each zone has:
   ├─ Random unit positions
   ├─ Random headings/orientations
   ├─ Mix of vehicle types
   └─ Different force ratios (3:1 Red to Blue)
```

## Customize in 2 Minutes

### Change Terrain
Edit the last line of `mission_generator.py`:

```python
def main():
    script_dir = Path(__file__).parent
    output_mission = script_dir / "goon_coldwar_dynamic.miz"
    
    # Change 'caucasus' to: 'nevada', 'syria', 'gulf', or 'marianas'
    generator = DynamicMissionGenerator(str(output_mission), terrain_name='nevada')
    success = generator.generate_mission(num_active_zones=3)
    return 0 if success else 1
```

### Change Number of Active Zones
```python
generator.generate_mission(num_active_zones=5)  # 5 zones instead of 3
```

### Run Advanced Examples
```bash
python advanced_examples.py
```

This generates 6 different mission variations showcasing customization options.

## Output Structure

Generated mission contains:
- **Map Zones**: Grid of geographic areas (1-16)
- **Zone Objectives**: Combat areas with mixed forces
- **Unit Groups**: Organized vehicle platoons
- **Starting Position**: All units positioned for immediate combat
- **Briefing**: Mission description and context

## Mission Features

✓ Zone-based combat system
✓ Dynamic unit placement  
✓ Balanced force ratios
✓ Multiple terrain support
✓ Easy to extend and customize
✓ Generates valid DCS mission files

## Typical Mission Profile

**Mission Type**: Zone Clearance / Armored Engagement
**Duration**: 30-60 minutes
**Difficulty**: Medium (AI forces)
**Player Role**: Blue commander - destroy Red forces in zones
**Recommended**: 1-4 players

## File Structure

```
mission_generator.py          ← Main script (run this)
advanced_examples.py          ← Example customizations
README_MISSION_GENERATOR.md   ← Full documentation
QUICKSTART.md                 ← This file

Output:
goon_coldwar_dynamic.miz      ← Generated mission (copy to DCS)
mission_nevada.miz            ← Example outputs (from advanced_examples.py)
mission_syria.miz
mission_caucasus.miz
[etc...]
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `pydcs not installed` | Run: `pip install pydcs` |
| Mission won't open | Check file size > 5KB, regenerate |
| Units not visible | Mission may need to start with F2 camera |
| Performance issues | Reduce `num_active_zones` parameter |
| Wrong terrain | Change `terrain_name` parameter |

## Next Steps

1. ✓ Install pydcs
2. ✓ Run mission_generator.py
3. ✓ Copy .miz file to DCS Missions folder
4. ✓ Load in DCS World
5. ✓ Fly the mission!

## Want More Control?

See `README_MISSION_GENERATOR.md` for:
- Detailed API documentation
- Vehicle customization options
- Zone configuration parameters
- Weather and environment settings
- Advanced mission scripting

See `advanced_examples.py` for:
- Multiple mission types
- Different terrain examples
- Custom vehicle loadouts
- Large-scale operations

## Support

**Script Location**: `c:\Users\kelvi\OneDrive\Documents\GitHub\goon-drop-point\`
**Generated Missions**: Same directory as script
**Dependencies**: pydcs library (handles DCS file format)

---

**Happy flying! 🛩️**
