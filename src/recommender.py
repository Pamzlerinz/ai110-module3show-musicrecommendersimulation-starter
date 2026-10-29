import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

# Point weights for each scoring mode (Strategy-style: same scorer, swappable weights).
# "balanced" is the Algorithm Recipe; "energy_focused" is the Phase 4 weight-shift
# experiment (genre halved, energy doubled).
SCORING_MODES: Dict[str, Dict[str, float]] = {
    "balanced":       {"genre": 2.0, "mood": 1.0, "energy": 1.5, "acoustic": 0.5},
    "genre_first":    {"genre": 3.0, "mood": 0.5, "energy": 1.0, "acoustic": 0.5},
    "mood_first":     {"genre": 1.0, "mood": 2.5, "energy": 1.5, "acoustic": 0.5},
    "energy_focused": {"genre": 1.0, "mood": 1.0, "energy": 3.0, "acoustic": 0.5},
}

NUMERIC_FIELDS = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

    def to_prefs(self) -> Dict:
        """Converts the profile into the prefs dict used by score_song."""
        return {
            "genre": self.favorite_genre,
            "mood": self.favorite_mood,
            "energy": self.target_energy,
            "likes_acoustic": self.likes_acoustic,
        }

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song], mode: str = "balanced"):
        self.songs = songs
        self.mode = mode

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k Song objects for the user, highest score first."""
        prefs = user.to_prefs()
        return sorted(
            self.songs,
            key=lambda s: score_song(prefs, asdict(s), self.mode)[0],
            reverse=True,
        )[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a readable explanation of why the song scored the way it did."""
        score, reasons = score_song(user.to_prefs(), asdict(song), self.mode)
        return f"Score {score:.2f}: " + "; ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Reads the songs CSV into a list of dicts with numeric fields converted."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for field in NUMERIC_FIELDS:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict, mode: str = "balanced") -> Tuple[float, List[str]]:
    """Scores one song against the user's prefs and returns (score, reasons)."""
    weights = SCORING_MODES[mode]
    score = 0.0
    reasons = []

    if song["genre"].lower() == user_prefs.get("genre", "").lower():
        score += weights["genre"]
        reasons.append(f"genre match (+{weights['genre']:.2f})")

    if song["mood"].lower() == user_prefs.get("mood", "").lower():
        score += weights["mood"]
        reasons.append(f"mood match (+{weights['mood']:.2f})")

    # Closeness, not size: a perfect energy match earns the full weight,
    # and the points shrink linearly as the gap grows.
    if "energy" in user_prefs:
        gap = abs(song["energy"] - user_prefs["energy"])
        energy_points = weights["energy"] * (1 - gap)
        score += energy_points
        reasons.append(f"energy {song['energy']:.2f} vs target {user_prefs['energy']:.2f} (+{energy_points:.2f})")

    if "likes_acoustic" in user_prefs:
        fit = song["acousticness"] if user_prefs["likes_acoustic"] else 1 - song["acousticness"]
        acoustic_points = weights["acoustic"] * fit
        score += acoustic_points
        reasons.append(f"acoustic fit (+{acoustic_points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, mode: str = "balanced") -> List[Tuple[Dict, float, str]]:
    """Scores every song, sorts highest first, and returns the top k as (song, score, explanation)."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, mode)
        scored.append((song, score, "; ".join(reasons)))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
