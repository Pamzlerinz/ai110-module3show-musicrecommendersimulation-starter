# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

**What task did you give the agent?**

I gave Claude Code (agent mode in VS Code) the full project instructions and had it implement the recommender from start to finish: expand the dataset, write `load_songs` / `score_song` / `recommend_songs` plus the OOP `Recommender`, build a multi-profile CLI, run the experiment, and draft the README and model card from the real terminal output.

**Prompts used:**

- The full "Music Recommender Simulation" project brief (Phases 1–5 and the optional extensions), pasted as one prompt.

**What did the agent generate or change?**

- `data/songs.csv`: added 8 songs (ids 11–18) in genres and moods the starter didn't have.
- `src/recommender.py`: CSV loading with float/int conversion; a scoring function that returns `(score, reasons)` using genre +2.0, mood +1.0, energy closeness up to +1.5, and optional acoustic fit up to +0.5; ranking with `sorted(..., reverse=True)[:k]`; the `Recommender` class reuses the same scorer; and a `SCORING_MODES` weights table.
- `src/main.py`: fixed the import (`from recommender` → `from src.recommender`, which failed under `python -m src.main`); added 5 profiles (3 normal, 2 edge cases); prints rank, score, and one reason per line; reads an optional mode from the command line.
- Ran `pytest` (2 passed) and `python -m src.main` in `balanced` and `energy_focused` modes, then pasted that exact output into README.md and model_card.md with a script instead of retyping it.

**What did you verify or fix manually?**

- Re-ran `pytest` and `python -m src.main` (both `balanced` and `energy_focused`) myself and confirmed the output matched what was pasted into the docs.
- Checked one score by hand: Sunrise City for the pop/happy profile = 2.0 (genre) + 1.0 (mood) + 1.5 × (1 − |0.82 − 0.80|) = 4.47, which matches the terminal.
- Checked that the energy rule rewards *closeness* instead of higher energy: for the Chill Lofi profile (target 0.35), Library Rain at exactly 0.35 got the full +1.50.
- Compared the rankings to my own intuition. Chill Lofi and Deep Intense Rock felt right. Gym Hero at #2 for "Happy Pop" did not, and I wrote that up as a limitation instead of hiding it by changing weights.
- Read through the generated README and model card, and confirmed that the numbers quoted in the text (e.g. the 3.60 vs 1.48 gap shrinking to 3.20 vs 2.97) match the actual output.

---

## Design Pattern (SF10)

**Which design pattern did you use?**

A lightweight **Strategy** pattern. Each scoring "strategy" is a named set of weights in `SCORING_MODES` (`balanced`, `genre_first`, `mood_first`, `energy_focused`). `score_song` and `recommend_songs` take a `mode` argument and look up the weights, so the scoring rules are written once.

**How did AI help you brainstorm or implement it?**

The agent considered full Strategy classes (one scorer class per mode) but chose a dictionary of weights, because every mode uses the same four rules and only the point values differ. Separate classes would repeat the same logic four times. Keeping the modes as data also turned the Phase 4 "double energy, halve genre" experiment into a mode (`energy_focused`) instead of a temporary code edit.

**How does the pattern appear in your final code?**

- `SCORING_MODES` at the top of [src/recommender.py](src/recommender.py) holds the strategies.
- `score_song(user_prefs, song, mode)` applies the selected weights.
- `Recommender(songs, mode=...)` and `recommend_songs(..., mode=...)` pass the mode through.
- `python -m src.main <mode>` switches modes from the command line.
