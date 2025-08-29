#!/usr/bin/env python3
"""
Test the updated LightingPlanner with story-driven approach.
"""

from backend.agents.lighting_planner.lighting_planner import LightingPlanner
from backend.models.app_data import AppData

def test_story_driven_planning():
    """Test the story-driven lighting planning approach."""
    print("🎭 Testing Story-Driven Lighting Planner")
    print("=" * 50)

    # Initialize AppData and load a song
    app_data = AppData()
    app_data.load_song("born_slippy")

    # Create the LightingPlanner agent
    planner = LightingPlanner()

    print("📊 Testing analysis summary extraction...")
    analysis_summary = planner._extract_analysis_summary(0, 30)  # First 30 seconds
    print(f"✅ Extracted summary: {len(analysis_summary)} fields")
    print(f"   - Tempo: {analysis_summary.get('tempo')}")
    print(f"   - Key: {analysis_summary.get('key')}")
    print(f"   - Beats in segment: {analysis_summary.get('beat_count')}")
    print(f"   - Structure sections: {len(analysis_summary.get('structure', []))}")

    print("\n📝 Testing context preparation...")
    planner.parse_song_context("born_slippy", start_time=0, end_time=30)

    print("✅ Context prepared and saved to logs/lighting_planner.context.txt")
    print("\n🎬 Story-driven planning test complete!")
    print("\n💡 The template now focuses on:")
    print("   - Creating emotional lighting narratives")
    print("   - Using story-driven language")
    print("   - Emphasizing musical storytelling")
    print("   - Providing precise beat timing without redundancy")

if __name__ == "__main__":
    test_story_driven_planning()
