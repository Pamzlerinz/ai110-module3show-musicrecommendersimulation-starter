# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

---

## 2. Intended Use  

VibeFinder suggests the top 5 songs from a small catalog that best fit one listener's stated taste: a favorite genre, a favorite mood, a target energy level, and optionally whether they like acoustic sound.

- It assumes the user can describe their taste in those few words and numbers, and that their taste stays the same.
- It is built for **classroom exploration**: learning how scoring and ranking turn data into recommendations.

**Not intended for:** real users or a real product, making decisions about artists (payouts, promotion, charts), or any claim about what someone "really" likes. It has no listening history and doesn't learn.

---

## 3. How the Model Works  

Think of it as a judge holding a scorecard for every song:

- **Same genre as you like?** Big bonus: 2 points.
- **Same mood?** Smaller bonus: 1 point.
- **Energy:** up to 1.5 points, based on *how close* the song's energy is to the energy you asked for. A perfect match gets all 1.5 points. A song that is much calmer or much more intense than you wanted gets fewer.
- **Acoustic (optional):** up to 0.5 points if the song is as acoustic (or as electronic) as you like.

The points are added up, every song in the catalog gets a total, and the five highest totals are the recommendations. Each one comes with its list of reasons, such as "genre match (+2.00)".

**Changes from the starter:** I implemented loading, scoring, and ranking; made energy reward *closeness* instead of "more is better"; added the optional acoustic rule; and added four swappable "scoring modes" (balanced, genre-first, mood-first, energy-focused) so the weights can be compared without editing code.

---

## 4. Data  

- **18 songs**: the 10 starter songs plus 8 I added to cover genres and moods the starter didn't have (hip-hop, classical, metal, r&b, country, edm, reggae, folk; confident, melancholy, angry, romantic, nostalgic, euphoric, sad).
- Each song has: genre, mood, energy, tempo, valence, danceability, acousticness. The scorer only uses genre, mood, energy, and acousticness.
- **Imbalances:** lofi has 3 songs, pop has 2, and almost every other genre has 1. "chill" is the most common mood (3 songs).
- **Missing:** lyrics, language, artist popularity, release year, anything about culture or region, and any listening behavior. All of the numbers were made up for this simulation; none come from real audio analysis.

---

## 5. Strengths  

- When a user's genre, mood, and energy all agree (like **Chill Lofi** or **Deep Intense Rock**), the top result is exactly the song I'd pick by hand. Library Rain and Storm Runner each scored 4.93 out of a possible 5.0.
- Energy closeness works well as a tie-breaker. After the label matches run out, the remaining slots fill with songs that *feel* similar: calm jazz and ambient for the lofi fan, edm and metal for the rock fan.
- Every recommendation is explainable. You can see exactly which rules fired and how many points each one added.

---

## 6. Limitations and Bias 

**Main weakness: the labels outweigh the sound.** Genre and mood are worth up to 3 points, but energy can only move a song by 1.5 points, so a song with the "right" tags beats songs that actually sound the way the user asked. With the "Sad but High Energy" profile, the #1 result was Empty Platform, a quiet folk ballad with 0.30 energy, even though the user asked for 0.9. It won on its two labels alone. The matching is also exact-text, so a "k-pop" fan gets zero genre points from every song, and "indie pop" gets no credit as "pop". This creates a filter bubble that favors whoever's taste uses the same words as the catalog. Since most genres have only one song, a metal or folk fan gets one real match and then a list of strangers, while a lofi fan gets three good matches.

Other issues:

- **Energy never gives up.** Even a song at the opposite end of the energy scale earns some energy points, so energy can't really *rule out* a song.
- **Repeat appearances.** Gym Hero (pop / intense / 0.93 energy) appears in the top 5 for Happy Pop, Deep Intense Rock, and Sad but High Energy. High-energy songs with common labels show up again and again.

---

## 7. Evaluation  

I tested five profiles in balanced mode, then ran all five again in `energy_focused` mode (genre halved, energy doubled).

| Profile | genre | mood | energy | acoustic |
|---|---|---|---|---|
| High-Energy Pop | pop | happy | 0.8 | – |
| Chill Lofi | lofi | chill | 0.35 | likes |
| Deep Intense Rock | rock | intense | 0.9 | dislikes |
| Edge: Sad but High Energy | folk | sad | 0.9 | – |
| Edge: Unknown Genre (k-pop) | k-pop | happy | 0.7 | – |

### What surprised me

- **Gym Hero showing up for "Happy Pop."** In plain terms: the system gives a big bonus just for having the word "pop" on the song, and Gym Hero is pop and nearly as energetic as the user wanted. It isn't happy at all, but the pop bonus (2 points) is worth twice as much as the happy bonus (1 point). So it beats Rooftop Lights, which *is* happy and upbeat but is tagged "indie pop", and the system treats that as a completely different word.
- **The edge case "won" with the wrong song.** I expected the sad-but-energetic profile to pull up intense songs, but the slow folk ballad came first because it matched both labels.
- **Unknown genre still works, sort of.** The k-pop fan got reasonable upbeat, happy songs, but only because mood and energy carried the score. Their top score was 2.41, compared with ~4.5–4.9 for users whose genre exists in the catalog.

### Comparing profiles (pairs)

- **High-Energy Pop vs Chill Lofi:** The pop list is all upbeat (energy 0.75–0.93), while the lofi list is all calm (0.28–0.42) and leans acoustic. This makes sense: the energy target splits the catalog into two halves.
- **High-Energy Pop vs Deep Intense Rock:** Both want high energy, so they share Gym Hero and Sunrise City. The rock list adds edm and metal (louder, less acoustic) because that user dislikes acoustic sound and asked for "intense" instead of "happy".
- **Chill Lofi vs Deep Intense Rock:** No songs in common. They are opposite on energy and on acoustic preference, which is the clearest sign that the profile can tell "intense rock" from "chill lofi".
- **Deep Intense Rock vs Sad but High Energy:** Positions 2–5 are almost identical (Storm Runner/Gym Hero/Laser Bloom/Ashfall) because both ask for ~0.9 energy. Only #1 differs, and that's purely the label bonus.
- **High-Energy Pop vs Unknown Genre (k-pop):** Same mood, similar energy, so they share Rooftop Lights, Sunrise City, Night Drive Loop and Concrete Crown. Without a genre match, the k-pop list loses Gym Hero, which only made the pop list because of its genre.
- **Chill Lofi vs Sad but High Energy:** The lofi list is consistent (calm everywhere), while the sad list is split: one quiet song at #1, then four loud ones. This shows the edge profile's preferences pulling in two directions.

### Weight-shift experiment

Halving genre and doubling energy made the results **somewhat more accurate for the pop user**: Rooftop Lights (happy) moved above Gym Hero (intense). For the sad-energetic user, the gap between the ballad and the loud songs shrank from 2.12 to 0.23 points. It made the lofi results **different, not better**: two near-equal chill songs swapped places. No #1 result changed for any profile.

### Full output, balanced mode

```
========================================================================
Profile: High-Energy Pop
Prefs:   {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}
------------------------------------------------------------------------
1. Sunrise City - Neon Echo [pop/happy]
   Score: 4.47
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.82 vs target 0.80 (+1.47)
2. Gym Hero - Max Pulse [pop/intense]
   Score: 3.30
     - genre match (+2.00)
     - energy 0.93 vs target 0.80 (+1.30)
3. Rooftop Lights - Indigo Parade [indie pop/happy]
   Score: 2.44
     - mood match (+1.00)
     - energy 0.76 vs target 0.80 (+1.44)
4. Concrete Crown - Verse Theory [hip-hop/confident]
   Score: 1.47
     - energy 0.78 vs target 0.80 (+1.47)
5. Night Drive Loop - Neon Echo [synthwave/moody]
   Score: 1.42
     - energy 0.75 vs target 0.80 (+1.42)
```

```
========================================================================
Profile: Chill Lofi
Prefs:   {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'likes_acoustic': True}
------------------------------------------------------------------------
1. Library Rain - Paper Lanterns [lofi/chill]
   Score: 4.93
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.35 vs target 0.35 (+1.50)
     - acoustic fit (+0.43)
2. Midnight Coding - LoRoom [lofi/chill]
   Score: 4.75
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.42 vs target 0.35 (+1.40)
     - acoustic fit (+0.35)
3. Focus Flow - LoRoom [lofi/focused]
   Score: 3.81
     - genre match (+2.00)
     - energy 0.40 vs target 0.35 (+1.42)
     - acoustic fit (+0.39)
4. Spacewalk Thoughts - Orbit Bloom [ambient/chill]
   Score: 2.85
     - mood match (+1.00)
     - energy 0.28 vs target 0.35 (+1.40)
     - acoustic fit (+0.46)
5. Coffee Shop Stories - Slow Stereo [jazz/relaxed]
   Score: 1.92
     - energy 0.37 vs target 0.35 (+1.47)
     - acoustic fit (+0.45)
```

```
========================================================================
Profile: Deep Intense Rock
Prefs:   {'genre': 'rock', 'mood': 'intense', 'energy': 0.9, 'likes_acoustic': False}
------------------------------------------------------------------------
1. Storm Runner - Voltline [rock/intense]
   Score: 4.93
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.91 vs target 0.90 (+1.48)
     - acoustic fit (+0.45)
2. Gym Hero - Max Pulse [pop/intense]
   Score: 2.93
     - mood match (+1.00)
     - energy 0.93 vs target 0.90 (+1.46)
     - acoustic fit (+0.47)
3. Laser Bloom - Kitewave [edm/euphoric]
   Score: 1.91
     - energy 0.95 vs target 0.90 (+1.43)
     - acoustic fit (+0.48)
4. Ashfall - Iron Choir [metal/angry]
   Score: 1.88
     - energy 0.97 vs target 0.90 (+1.40)
     - acoustic fit (+0.48)
5. Sunrise City - Neon Echo [pop/happy]
   Score: 1.79
     - energy 0.82 vs target 0.90 (+1.38)
     - acoustic fit (+0.41)
```

```
========================================================================
Profile: Edge: Sad but High Energy
Prefs:   {'genre': 'folk', 'mood': 'sad', 'energy': 0.9}
------------------------------------------------------------------------
1. Empty Platform - Grey Harbor [folk/sad]
   Score: 3.60
     - genre match (+2.00)
     - mood match (+1.00)
     - energy 0.30 vs target 0.90 (+0.60)
2. Storm Runner - Voltline [rock/intense]
   Score: 1.48
     - energy 0.91 vs target 0.90 (+1.48)
3. Gym Hero - Max Pulse [pop/intense]
   Score: 1.46
     - energy 0.93 vs target 0.90 (+1.46)
4. Laser Bloom - Kitewave [edm/euphoric]
   Score: 1.43
     - energy 0.95 vs target 0.90 (+1.43)
5. Ashfall - Iron Choir [metal/angry]
   Score: 1.40
     - energy 0.97 vs target 0.90 (+1.40)
```

```
========================================================================
Profile: Edge: Unknown Genre (k-pop)
Prefs:   {'genre': 'k-pop', 'mood': 'happy', 'energy': 0.7}
------------------------------------------------------------------------
1. Rooftop Lights - Indigo Parade [indie pop/happy]
   Score: 2.41
     - mood match (+1.00)
     - energy 0.76 vs target 0.70 (+1.41)
2. Sunrise City - Neon Echo [pop/happy]
   Score: 2.32
     - mood match (+1.00)
     - energy 0.82 vs target 0.70 (+1.32)
3. Night Drive Loop - Neon Echo [synthwave/moody]
   Score: 1.42
     - energy 0.75 vs target 0.70 (+1.42)
4. Concrete Crown - Verse Theory [hip-hop/confident]
   Score: 1.38
     - energy 0.78 vs target 0.70 (+1.38)
5. Dirt Road Daydream - Hollis Creek [country/nostalgic]
   Score: 1.32
     - energy 0.58 vs target 0.70 (+1.32)
```

### Full output, energy_focused mode (experiment)

```
========================================================================
Profile: High-Energy Pop
Prefs:   {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}
------------------------------------------------------------------------
1. Sunrise City - Neon Echo [pop/happy]
   Score: 4.94
     - genre match (+1.00)
     - mood match (+1.00)
     - energy 0.82 vs target 0.80 (+2.94)
2. Rooftop Lights - Indigo Parade [indie pop/happy]
   Score: 3.88
     - mood match (+1.00)
     - energy 0.76 vs target 0.80 (+2.88)
3. Gym Hero - Max Pulse [pop/intense]
   Score: 3.61
     - genre match (+1.00)
     - energy 0.93 vs target 0.80 (+2.61)
4. Concrete Crown - Verse Theory [hip-hop/confident]
   Score: 2.94
     - energy 0.78 vs target 0.80 (+2.94)
5. Night Drive Loop - Neon Echo [synthwave/moody]
   Score: 2.85
     - energy 0.75 vs target 0.80 (+2.85)
```

```
========================================================================
Profile: Chill Lofi
Prefs:   {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'likes_acoustic': True}
------------------------------------------------------------------------
1. Library Rain - Paper Lanterns [lofi/chill]
   Score: 5.43
     - genre match (+1.00)
     - mood match (+1.00)
     - energy 0.35 vs target 0.35 (+3.00)
     - acoustic fit (+0.43)
2. Midnight Coding - LoRoom [lofi/chill]
   Score: 5.14
     - genre match (+1.00)
     - mood match (+1.00)
     - energy 0.42 vs target 0.35 (+2.79)
     - acoustic fit (+0.35)
3. Spacewalk Thoughts - Orbit Bloom [ambient/chill]
   Score: 4.25
     - mood match (+1.00)
     - energy 0.28 vs target 0.35 (+2.79)
     - acoustic fit (+0.46)
4. Focus Flow - LoRoom [lofi/focused]
   Score: 4.24
     - genre match (+1.00)
     - energy 0.40 vs target 0.35 (+2.85)
     - acoustic fit (+0.39)
5. Coffee Shop Stories - Slow Stereo [jazz/relaxed]
   Score: 3.38
     - energy 0.37 vs target 0.35 (+2.94)
     - acoustic fit (+0.45)
```

```
========================================================================
Profile: Edge: Sad but High Energy
Prefs:   {'genre': 'folk', 'mood': 'sad', 'energy': 0.9}
------------------------------------------------------------------------
1. Empty Platform - Grey Harbor [folk/sad]
   Score: 3.20
     - genre match (+1.00)
     - mood match (+1.00)
     - energy 0.30 vs target 0.90 (+1.20)
2. Storm Runner - Voltline [rock/intense]
   Score: 2.97
     - energy 0.91 vs target 0.90 (+2.97)
3. Gym Hero - Max Pulse [pop/intense]
   Score: 2.91
     - energy 0.93 vs target 0.90 (+2.91)
4. Laser Bloom - Kitewave [edm/euphoric]
   Score: 2.85
     - energy 0.95 vs target 0.90 (+2.85)
5. Ashfall - Iron Choir [metal/angry]
   Score: 2.79
     - energy 0.97 vs target 0.90 (+2.79)
```

The automated tests (`pytest`) also check that the OOP `Recommender` ranks a pop/happy song first for a pop/happy user and gives a non-empty explanation.

---

## 8. Future Work  

1. **Fuzzy matching:** treat related genres and moods as partial matches (e.g. "indie pop" ≈ "pop" for +1.0, "relaxed" ≈ "chill"), so the system is less tied to exact words.
2. **Make energy able to say no:** use a steeper penalty (like squaring the gap, or zero points beyond a 0.4 gap), so a 0.3-energy song can't win for someone who asked for 0.9.
3. **Diversity in the top 5:** subtract points from a song if its artist or genre is already in the list, so one sound doesn't fill every slot. Also use the unused features (tempo, valence, danceability) to break ties.

---

## 9. Personal Reflection  

<!-- TODO (write in your own words — this section is graded on YOUR reflection):
  - What was your biggest learning moment during this project?
  - How did using AI tools help you, and when did you need to double-check them?
  - What surprised you about how simple algorithms can still "feel" like recommendations?
  - What would you try next if you extended this project? -->
