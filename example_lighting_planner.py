#!/usr/bin/env python3
"""
Example usage of the LightingPlanner agent with song analysis integration.
"""

from backend.agents.lighting_planner.lighting_planner import LightingPlanner
from backend.models.app_data import AppData

def main():
    # Initialize AppData and load a song
    app_data = AppData()
    app_data.load_song("born_slippy")

    # Create the LightingPlanner agent
    planner = LightingPlanner()

    # Example 1: Plan for the entire song
    print("🎵 Planning lighting for entire song...")
    planner.parse_song_context("born_slippy")

    # Example 2: Plan for a specific segment (intro section)
    print("\n🎵 Planning lighting for intro section (0-30s)...")
    planner.parse_song_context("born_slippy", start_time=0, end_time=30)

    # Example 3: Plan for chorus section
    print("\n🎵 Planning lighting for chorus section (120-130s)...")
    planner.parse_song_context("born_slippy", start_time=120, end_time=130)

    print("\n✅ LightingPlanner implementation complete!")
    print("📝 Context files saved to logs/lighting_planner.context.txt")

if __name__ == "__main__":
    main()
