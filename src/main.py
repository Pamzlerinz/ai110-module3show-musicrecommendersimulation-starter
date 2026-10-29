"""
Command line runner for the Music Recommender Simulation.

Usage:
    python -m src.main                  # balanced mode, all profiles
    python -m src.main energy_focused   # any key from SCORING_MODES
"""

import sys

from src.recommender import load_songs, recommend_songs, SCORING_MODES

PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9, "likes_acoustic": False},
    # Edge cases: conflicting prefs, and a genre that isn't in the catalog
    "Edge: Sad but High Energy": {"genre": "folk", "mood": "sad", "energy": 0.9},
    "Edge: Unknown Genre (k-pop)": {"genre": "k-pop", "mood": "happy", "energy": 0.7},
}


def print_recommendations(name: str, prefs: dict, recommendations: list) -> None:
    """Prints one profile's ranked results with scores and reasons."""
    print("=" * 72)
    print(f"Profile: {name}")
    print(f"Prefs:   {prefs}")
    print("-" * 72)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} - {song['artist']} [{song['genre']}/{song['mood']}]")
        print(f"   Score: {score:.2f}")
        for reason in explanation.split("; "):
            print(f"     - {reason}")
    print()


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else "balanced"
    if mode not in SCORING_MODES:
        sys.exit(f"Unknown mode '{mode}'. Choose from: {', '.join(SCORING_MODES)}")

    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")
    print(f"Scoring mode: {mode} {SCORING_MODES[mode]}\n")

    for name, prefs in PROFILES.items():
        recommendations = recommend_songs(prefs, songs, k=5, mode=mode)
        print_recommendations(name, prefs, recommendations)


if __name__ == "__main__":
    main()
