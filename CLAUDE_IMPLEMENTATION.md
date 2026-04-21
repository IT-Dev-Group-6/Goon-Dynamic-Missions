# CLAUDE.md Implementation - Mission Generator

## Overview

The `mission_generator.py` script has been completely rewritten to implement the full CLAUDE.md specification for generating automated, persistent Cold War or Modern dynamic missions for 8-man squad gameplay.

## Key Features Implemented

### 1. Data-Driven Generation (JSON Integration)

The generator now uses a **configuration-first** approach:

- **mission_config.json**: Central mission configuration
  - Era selection (cold_war/modern)
  - Terrain selection
  - Active zones count
  - Spawn cap (default: 40 groups)
  - Proximity radius for unit activation

- **zones.json**: Grid definition and state
  - Origin coordinates (origin_x, origin_y)
  - Cell size in meters (cell_size_m)
  - Grid dimensions (rows, cols)
  - Zone ownership and inclusion status

- **cold_war.json** / **modern.json**: Era-specific unit templates
  - Vehicle types with pydcs IDs
  - Aircraft types
  - Unit count ranges (min/max per zone)

### 2. Grid System (Z_row_col Naming)

The grid is built from `zones.json` with the `Z_row_col` naming convention:

```
Z_0_0  Z_0_1  Z_0_2  Z_0_3  Z_0_4
Z_1_0  Z_1_1  Z_1_2  Z_1_3  Z_1_4
Z_2_0  Z_2_1  Z_2_2  Z_2_3  Z_2_4
Z_3_0  Z_3_1  Z_3_2  Z_3_3  Z_3_4
Z_4_0  Z_4_1  Z_4_2  Z_4_3  Z_4_4
```

Each zone:
- Has a row and column index
- Tracks owner (red/blue/contested)
- Tracks inclusion status (playable/inactive)
- Generates unique grid positions from origin coordinates

### 3. Active Zone Selection

The generator automatically selects **3 active zones** based on frontline proximity:

1. **Frontline Priority**: Contested zones are prioritized for selection
2. **Included Status**: Only zones marked as "included" in zones.json are considered
3. **Randomization**: Within priority tiers, selection is randomized
4. **Smart Fallback**: If insufficient contested zones, fills with red/blue zones

### 4. F10 Map Drawing Objects

Colored grid squares are drawn on the F10 map for active zones:

- **Red (#FF00007F)**: Enemy-controlled zones
- **Blue (#0000FF7F)**: Friendly/captured zones
- **Gray (#8080807F)**: Contested/objective zones
- Semi-transparent rectangles with labels (e.g., "Z_2_1 (CONTESTED)")

### 5. Lua Stack Injection Framework

The generator prepares injection of the following Lua scripts (in order):

1. Moose.lua - Core framework
2. Splash_Damage_3.4.1_leka.lua - Damage extension
3. EWRS.lua - Early warning radar system
4. Foothold Config.lua - Configuration
5. Foothold CTLD.lua - Command/transport logistics
6. AIEN.lua - AI enhancement
7. MA_Setup_CA.lua - Mission automation setup

**Note**: Actual Lua file injection requires locating these files in the workspace and implementing zipfile manipulation for `.miz` mission files.

### 6. Performance & Locality

- **Spawn Cap**: Enforced at 40 groups maximum (configurable)
- **Group Counter**: Tracks spawned groups and prevents exceeding cap
- **Proximity Activation**: Framework supports 40km radius (configurable) for unit spawn triggers
- **Smart Scaling**: Blue forces scaled 50-100% based on zone owner

## Configuration Files Reference

### mission_config.json

```json
{
  "era": "cold_war",           // or "modern"
  "terrain": "caucasus",        // Terrain selection
  "description": "...",         // Mission description
  "squad_size": 8,              // Player squad size
  "active_zones": 3,            // Number of active zones
  "spawn_cap": 40,              // Maximum group count
  "proximity_radius_km": 40     // Unit activation radius
}
```

### zones.json Structure

```json
{
  "grid": {
    "origin_x": 0,              // Grid origin X coordinate
    "origin_y": 0,              // Grid origin Y coordinate
    "cell_size_m": 40000,       // Size of each grid cell in meters
    "rows": 5,                  // Number of rows
    "cols": 5                   // Number of columns
  },
  "zones": {
    "Z_row_col": {
      "owner": "red|blue|contested",  // Zone owner
      "included": true|false          // Whether zone is playable
    }
  }
}
```

### Unit Templates (cold_war.json / modern.json)

```json
{
  "era": "cold_war",
  "red_side": {
    "country": "Russia",
    "vehicles": [
      {"name": "T-90", "pydcs_id": "T_90"},
      ...
    ],
    "aircraft": [...]
  },
  "blue_side": {
    "country": "USA",
    "vehicles": [...],
    "aircraft": [...]
  },
  "units_per_zone": {"min": 20, "max": 30}
}
```

## Usage

### Basic Usage

```bash
python mission_generator.py
```

The script will:
1. Load `mission_config.json` for configuration
2. Load `zones.json` for grid definition
3. Load the appropriate era template (cold_war.json or modern.json)
4. Create a new DCS mission on the specified terrain
5. Select 3 active zones based on frontline proximity
6. Spawn units in those zones with spawn cap enforcement
7. Generate colored F10 map markers
8. Prepare Lua script injection
9. Save mission as `goon_{era}_dynamic_auto_gen.miz`

### Customization

#### Change Era
Edit `mission_config.json`:
```json
{
  "era": "modern"
}
```

#### Change Terrain
Edit `mission_config.json`:
```json
{
  "terrain": "syria"
}
```

#### Adjust Frontline
Edit `zones.json` to modify zone ownership and inclusion:
```json
{
  "Z_1_2": {"owner": "contested", "included": true},
  "Z_1_3": {"owner": "blue", "included": false}
}
```

#### Change Spawn Cap
Edit `mission_config.json`:
```json
{
  "spawn_cap": 60
}
```

## Class Reference

### MissionZone

Represents a single grid cell in the Z_row_col system.

**Key Methods:**
- `get_f10_color()` - Returns RGBA color tuple based on owner
- `contains_point(x, y)` - Check if point is in zone
- `random_point_in_zone()` - Generate random position in zone

**Key Attributes:**
- `zone_id` - Zone identifier (e.g., "Z_0_1")
- `row`, `col` - Grid position
- `center_x`, `center_y` - World coordinates
- `owner` - Zone owner (red/blue/contested)
- `included` - Whether zone is playable

### ZoneGridSystem

Manages the complete grid loaded from zones.json.

**Key Methods:**
- `get_active_zones_by_frontline(num_zones)` - Select frontline-proximate zones
- `get_all_zones()` - Get all zones
- `get_frontline_zones()` - Get contested zones only
- `get_zone_by_id(zone_id)` - Look up zone by ID

### DynamicMissionGenerator

Main generator class that orchestrates mission creation.

**Key Methods:**
- `create_mission()` - Initialize DCS mission
- `add_zone_objectives()` - Spawn units in active zones
- `add_mission_briefing()` - Add mission description
- `generate_mission(output_path)` - Complete mission generation
- `_inject_lua_scripts()` - Inject Lua stack (framework)

**Key Attributes:**
- `era` - Selected era (cold_war/modern)
- `zone_grid` - ZoneGridSystem instance
- `active_zones` - List of selected active zones
- `group_count` - Current group count (spawn cap tracking)

## Next Steps for Full Implementation

### 1. Lua Script Injection
- Locate Lua files from workspace:
  - MOOSE/Moose_2026_02-06_test.lua
  - Lekas-Foothold/Common Scripts/AIEN.lua
  - Lekas-Foothold/Common Scripts/EWRS.lua
  - Lekas-Foothold/Setup files/Foothold Config.lua, Foothold CTLD.lua, MA_Setup_CA.lua
- Implement actual zipfile-based injection into `.miz` files
- Parse mission file structure for trigger insertion

### 2. Proximity Activation
- Implement in generated Lua code: `DCS.getDistance` checks
- Create spawn/initialization triggers based on player distance

### 3. Airfield Handling
- Identify airfield zones in grid
- Enforce CTLD troop insertion requirement for airfields
- Limit airframe availability based on campaign state

### 4. MISSION_START Trigger
- Parse mission file Lua structure
- Inject master loader trigger that loads scripts in correct order
- Add initialization routines for Moose -> Splash -> EWRS -> Foothold -> AIEN -> MA_Setup

### 5. Testing & Validation
- Test with actual DCS mission files
- Verify F10 map drawing objects appear
- Validate unit spawning and group caps
- Test era switching (cold_war ↔ modern)

## Technical Notes

- **Non-Destructive**: Output always written to `*_auto_gen.miz` files
- **pydcs Patches**: Ensure Syria airport crash patch and fog patches are applied
- **Zone Locality**: All zone calculations use grid origin and cell size from JSON
- **State Persistence**: Zone ownership/inclusion state determines mission flow
- **Scalability**: Grid system supports any NxM configuration via zones.json

## Troubleshooting

### Mission won't load
- Verify pydcs is installed: `pip install pydcs`
- Check JSON files are valid: `python -c "import json; json.load(open('mission_config.json'))"`
- Ensure terrain name is supported (caucasus, nevada, syria, gulf, marianas)

### Groups not spawning
- Check spawn_cap in mission_config.json
- Verify zones.json has `"included": true` for desired zones
- Check unit templates in cold_war.json / modern.json

### F10 markers missing
- Verify active zones were selected (check console output)
- Ensure DCS supports drawing objects (usually available)

### Lua scripts not found
- Copy Lua files to mission_generator.py directory
- Check exact filenames match LUA_SCRIPTS list

## References

- CLAUDE.md - Core architectural specification
- zones.json - Grid and state definitions
- mission_config.json - Mission parameters
- cold_war.json / modern.json - Unit templates
