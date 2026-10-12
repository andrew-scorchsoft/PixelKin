# The Old Light — level scoring rubric

A rubric for judging the Old Light (`pearlmoor_oldlight_1..6`, `_top`), the seven-floor
comedy lighthouse ("jest-house") on Lightkeeper's Point. It's the middle leg of the Causeway
Bell chain (walkthrough/01-south.md) and the optional grind bed before Reyl (ace 16) and the
fen (16–19). Score each dimension 0–10. Multiply by the dimension's weight and divide by 10.
The total is out of 100.

**The ship bar is 85.** Any single dimension under 6 blocks shipping, whatever the total.

| # | Dimension | Weight | What a 10 looks like | What a 4 looks like |
|---|-----------|-------:|----------------------|---------------------|
| 1 | **Comedy & charm** | 15 | Nearly every prop and person has a gag that lands, in many registers (slapstick, wordplay, absurd machines, timing jokes). It is cosy and never mean or creepy. Paul would quote lines back. | Gags are thin, repetitive or only flavour text. Long stretches have nothing to press A on. |
| 2 | **Escalating derangement** | 10 | Each floor is visibly, audibly and mechanically stranger than the last: tileset warp, music, battle backdrop, room logic, joke style. The top is a delirium payoff. | The floors feel interchangeable. Escalation shows only in the text. |
| 3 | **Navigation & level design** | 15 | Floors are big enough to make you walk (the classic haunted-tower climb): stairs on alternating corners, a hall to cross, alcoves and side pockets, no dead air. The route reads at a glance and is never a maze for its own sake. | Floors are corridors from stair to stair, or confusing with no visual lead. |
| 4 | **Story & emotional arc** | 15 | Tam, Reyl, the cut rope and eleven winters unfold a floor at a time and land at the top: laugh, then a lump in the throat. The player supplies Tam's punchline. | The story is only told at the end, or is unclear. |
| 5 | **Companionship & encouragement** | 5 | A non-battling character travels the climb with you, cheers you on and carries part of the story. The tower feels inhabited by people who care, not just by trainers. | Only trainers and signs. Nobody is on your side. |
| 6 | **Battle balance & levelling purpose** | 10 | The optional trainers and wild tables climb smoothly (about 9 to 14). Fights are fair and never walls, and a full clear leaves you ready for Reyl and the fen. The payouts follow the economy formula. | There are spikes or no reason to fight, or the floors under-level you for the next leg. |
| 7 | **Creature fit** | 10 | The tower has its own kin that belong nowhere else (clowns that are cute, not creepy). They are balanced against the roster (the sim passes), their kindling lines feel earned, and their sprites are full-body, clear and charming. | It reuses generic kin from elsewhere, or new kin are off-tone or out of balance. |
| 8 | **Clarity & softlock safety** | 10 | It's always clear what unlocks the next stair. Gates speak (blocked lines). Leaving with the job half-done is caught (the rope reminder). There's no softlock in any flag order, and Andrew's hints cover it. | A player can stall without knowing why, or get stuck. |
| 9 | **Rest & pacing** | 5 | Heal or rest points come at sensible intervals (lower floors and near the top). Encounter rates are gentle enough to explore and present enough to grind. Every screen holds something. | Long stretches with no rest, or encounters so frequent that exploring hurts. |
| 10 | **Polish & technical correctness** | 5 | All audits pass (flow, warps, footing, journey, content, rebuild). Art is crisp (props, sprites, backdrops) and the music loops cleanly. | Placeholders, audit warnings, broken loops. |

## How to score

1. Read `tools/maps/build_pearlmoor_oldlight.py`, `src/game/content/oldlight.ts`,
   `src/game/content/regions/jesthouse.ts`, the tower rows in `content/trainers.ts`, and
   the new kin (#167–#171 in `src/game/data/species/`).
2. Look at the renders (`python3 tools/maps/render_map.py pearlmoor_oldlight_N`), the battle
   backdrops (`public/assets/backgrounds/battle/oldlight-*.webp`) and the kin sprites.
3. Score each dimension, with one line of evidence for each score. Give the weighted total and
   the three cheapest changes that would raise it most.

## Score history

The newest score is first.

| Date | Iteration | Total | Notes |
|------|-----------|------:|-------|
