#!/usr/bin/env python3
"""
Dynamic Mission Generator for DCS
Generates DCS missions with zone-based unit spawning (20-30 units per zone).
Loads a base mission and creates a grid-based dynamic mission system.
"""

import sys
import os
import math
import random
from typing import List, Tuple, Dict, Optional
from pathlib import Path

try:
    import dcs
    from dcs import terrain
    from dcs.mapping import Point, Vector2
    from dcs.unit import Vehicle
    from dcs.country import Country
    from dcs.countries import USA, Russia
    from dcs.vehicles import Armor, Infantry
    from dcs.unitgroup import Group, VehicleGroup
except ImportError:
    print("ERROR: pydcs not installed. Install with: pip install pydcs")
    sys.exit(1)


class MissionZone:
    """Represents a geographic zone on the map."""
    
    def __init__(self, zone_id: int, center_x: float, center_y: float, 
                 size: float = 20000):
        """
        Args:
            zone_id: Unique identifier for the zone
            center_x: X coordinate of zone center (meters)
            center_y: Y coordinate of zone center (meters)
            size: Size of the zone (radius in meters)
        """
        self.zone_id = zone_id
        self.center_x = center_x
        self.center_y = center_y
        self.size = size
        self.units_count = random.randint(20, 30)  # Random between 20-30
        
    def contains_point(self, x: float, y: float) -> bool:
        """Check if a point is within this zone."""
        distance = math.sqrt((x - self.center_x)**2 + (y - self.center_y)**2)
        return distance <= self.size
    
    def random_point_in_zone(self) -> Tuple[float, float]:
        """Generate a random point within the zone."""
        angle = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, self.size)
        x = self.center_x + radius * math.cos(angle)
        y = self.center_y + radius * math.sin(angle)
        return x, y
    
    def __repr__(self):
        return f"Zone(id={self.zone_id}, center=({self.center_x}, {self.center_y}), units={self.units_count})"


class ZoneGridSystem:
    """Manages a grid of zones across the map."""
    
    def __init__(self, map_width: float, map_height: float, 
                 zone_size: float = 40000, zones_per_row: int = 5):
        """
        Args:
            map_width: Width of the map in meters
            map_height: Height of the map in meters
            zone_size: Size of each zone in meters
            zones_per_row: Number of zones per row in the grid
        """
        self.map_width = map_width
        self.map_height = map_height
        self.zone_size = zone_size
        self.zones_per_row = zones_per_row
        self.zones: List[MissionZone] = []
        self._create_zones()
    
    def _create_zones(self):
        """Create a grid of zones across the map."""
        zone_id = 1
        # Create a grid of zones
        num_zones_x = max(1, int(self.map_width / self.zone_size))
        num_zones_y = max(1, int(self.map_height / self.zone_size))
        
        for y_idx in range(num_zones_y):
            for x_idx in range(num_zones_x):
                center_x = (x_idx + 0.5) * self.zone_size
                center_y = (y_idx + 0.5) * self.zone_size
                
                # Only create zone if center is within map bounds
                if center_x <= self.map_width and center_y <= self.map_height:
                    zone = MissionZone(zone_id, center_x, center_y, 
                                      size=self.zone_size / 2.5)
                    self.zones.append(zone)
                    zone_id += 1
    
    def get_zones(self) -> List[MissionZone]:
        """Get all zones."""
        return self.zones
    
    def get_zone_for_point(self, x: float, y: float) -> Optional[MissionZone]:
        """Find the zone containing a given point."""
        for zone in self.zones:
            if zone.contains_point(x, y):
                return zone
        return None
    
    def get_active_zones(self, count: int = 3) -> List[MissionZone]:
        """Select random active zones for mission objectives."""
        return random.sample(self.zones, min(count, len(self.zones)))


class DynamicMissionGenerator:
    """Generates dynamic DCS missions with zone-based spawning."""
    
    # Vehicle types for red forces (using common armor)
    RED_VEHICLES = [
        Armor.T_90,
        Armor.T_80B,
        Armor.T_72B,
        Armor.BMP_3,
        Armor.BMP_2,
    ]
    
    # Vehicle types for blue forces
    BLUE_VEHICLES = [
        Armor.M_1_Abrams,
        Armor.M_1_Abrams,  # Weight more for blue
        Armor.M1128_Stryker_MGS,
        Armor.M1045_HMMWV_TOW,
    ]
    
    # List of supported terrains in pydcs
    SUPPORTED_TERRAINS = {
        'caucasus': lambda: terrain.Caucasus(),
        'nevada': lambda: terrain.Nevada(),
        'syria': lambda: terrain.Syria(),
        'gulf': lambda: terrain.PersianGulf(),
        'marianas': lambda: terrain.MarianaIslands(),
    }
    
    def __init__(self, output_mission_path: str, terrain_name: str = 'caucasus'):
        """
        Args:
            output_mission_path: Path for the output generated mission
            terrain_name: Name of the terrain ('caucasus', 'nevada', 'syria', 'gulf', 'marianas')
        """
        self.output_mission_path = output_mission_path
        self.terrain_name = terrain_name.lower()
        self.mission: Optional[dcs.Mission] = None
        self.terrain: Optional[terrain.Terrain] = None
        self.zone_grid: Optional[ZoneGridSystem] = None
    
    def create_mission(self) -> bool:
        """Create a new mission from scratch."""
        try:
            print(f"Creating mission on terrain: {self.terrain_name}")
            
            # Create terrain
            if self.terrain_name not in self.SUPPORTED_TERRAINS:
                print(f"ERROR: Unsupported terrain '{self.terrain_name}'")
                print(f"Supported: {', '.join(self.SUPPORTED_TERRAINS.keys())}")
                return False
            
            terrain_func = self.SUPPORTED_TERRAINS[self.terrain_name]
            self.terrain = terrain_func()
            
            # Create mission
            self.mission = dcs.Mission(terrain=self.terrain)
            self.mission.description_text = "Dynamic Zone-Based Combat Mission"
            
            # Initialize zone grid based on terrain
            print(f"Terrain: {self.terrain.__class__.__name__}")
            self._initialize_zone_grid()
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to create mission: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _initialize_zone_grid(self):
        """Initialize the zone grid system."""
        # Estimate map size (these are approximate for different terrains)
        map_width = 100000  # Default 100km x 100km
        map_height = 100000
        
        # Adjust for known terrains
        terrain_name = self.terrain.__class__.__name__
        if terrain_name == "Caucasus":
            map_width = map_height = 180000
        elif terrain_name == "Nevada":
            map_width = map_height = 200000
        elif terrain_name == "Syria":
            map_width = map_height = 200000
        
        print(f"Map size estimate: {map_width/1000:.0f}km x {map_height/1000:.0f}km")
        self.zone_grid = ZoneGridSystem(map_width, map_height, 
                                       zone_size=40000, zones_per_row=5)
        print(f"Created {len(self.zone_grid.get_zones())} zones")
    
    def add_zone_objectives(self, num_active_zones: int = 3):
        """Add objectives to randomly selected zones."""
        if not self.mission or not self.zone_grid:
            print("ERROR: Mission not loaded or zone grid not initialized")
            return
        
        # Get active zones
        active_zones = self.zone_grid.get_active_zones(num_active_zones)
        print(f"\nActivating {len(active_zones)} zones as objectives")
        
        red = self.mission.country("Russia")
        blue = self.mission.country("USA")
        
        for zone_idx, zone in enumerate(active_zones, 1):
            print(f"\nZone {zone_idx}: {zone}")
            
            # Add red ground units (defending)
            self._add_ground_group(red, zone, "Red", coalition_side="red")
            
            # Add blue ground units (attacking) - smaller force
            self._add_ground_group(blue, zone, "Blue", coalition_side="blue", 
                                  scale=0.3)
    
    def _add_ground_group(self, country: Country, zone: MissionZone, 
                         group_prefix: str, coalition_side: str, 
                         scale: float = 1.0) -> Optional[VehicleGroup]:
        """Add a ground unit group to a zone."""
        try:
            num_units = max(5, int(zone.units_count * scale))
            
            # Choose vehicle types based on coalition
            if coalition_side == "red":
                vehicle_types = self.RED_VEHICLES
            else:
                vehicle_types = self.BLUE_VEHICLES
            
            # Create a vehicle group
            group = VehicleGroup(self.mission.next_group_id(), 
                                name=f"{group_prefix}-Zone{zone.zone_id}")
            
            # Get starting position
            start_x, start_y = zone.random_point_in_zone()
            
            # Add units to the group
            for unit_idx in range(num_units):
                # Offset each unit slightly from the group starting position
                offset_x = random.uniform(-500, 500)
                offset_y = random.uniform(-500, 500)
                pos_x = start_x + offset_x
                pos_y = start_y + offset_y
                
                vehicle_type = random.choice(vehicle_types)
                unit = Vehicle(self.mission.next_unit_id(), 
                             f"{group_prefix}-Unit-{zone.zone_id}-{unit_idx}",
                             vehicle_type.id)
                unit.position = Point(pos_x, pos_y, 0)
                unit.heading = random.randint(0, 360)
                
                group.add_unit(unit)
            
            # Add a waypoint to the group so it has a valid route
            waypoint_x, waypoint_y = zone.random_point_in_zone()
            group.add_waypoint(Point(waypoint_x, waypoint_y, 0), speed=0)
            
            # Add the group to the country
            country.add_vehicle_group(group)
            
            print(f"  Added {group.name} with {num_units} units")
            return group
            
        except Exception as e:
            print(f"  WARNING: Failed to add group: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def add_mission_briefing(self):
        """Add mission briefing and objectives."""
        if not self.mission or not self.zone_grid:
            return
        
        briefing = """
MISSION: ZONE CLEARANCE OPERATION
Objective: Destroy all enemy units and structures in designated zones.
Rules of Engagement: Destroy all hostile forces in active zones.
        """
        
        self.mission.description_text = briefing
        print("\nMission briefing added")
    
    def generate_mission(self, num_active_zones: int = 3) -> bool:
        """Generate the complete mission."""
        try:
            print("\n" + "="*60)
            print("GENERATING DYNAMIC MISSION")
            print("="*60)
            
            if not self.create_mission():
                return False
            
            self.add_zone_objectives(num_active_zones)
            self.add_mission_briefing()
            
            # Save the mission
            print(f"\nSaving mission to: {self.output_mission_path}")
            self.mission.save(self.output_mission_path)
            
            print("\n" + "="*60)
            print("MISSION GENERATION COMPLETE")
            print("="*60)
            print(f"Output: {self.output_mission_path}")
            print(f"Total zones created: {len(self.zone_grid.get_zones())}")
            print(f"Active zones: {min(num_active_zones, len(self.zone_grid.get_zones()))}")
            
            return True
            
        except Exception as e:
            print(f"ERROR: Mission generation failed: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main entry point."""
    # Configuration
    script_dir = Path(__file__).parent
    output_mission = script_dir / "goon_coldwar_dynamic.miz"
    
    # Generate mission on Caucasus terrain
    generator = DynamicMissionGenerator(str(output_mission), terrain_name='caucasus')
    success = generator.generate_mission(num_active_zones=3)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
