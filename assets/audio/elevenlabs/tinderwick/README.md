# Tinderwick — ElevenLabs candidates (2026-10, not yet wired)

Raw `music_v2_5` renders (84 s, instrumental) + the exact prompts. The game loop is
cut from a raw take with `tools/audio/make_loop.py` (take A: 5.13→46.86 s = 16 bars
at 92 BPM; take B: 3.60→51.60 s). The served track stays `tinderwick-a.mp3` until a
take is approved.

## v3 — structured + loop-glued (2026-10)
Take B uploaded (`/v1/music/upload`, song_id `LDWhGzDt5IwjtK9QD5oj_upload`) as the MOTIF SOURCE.
`v3_*_plan.json`: Intro (4 bars) → Theme → Theme+flute → A-minor Bridge → Theme return, the
intro chunk conditioned on Take B 15–45 s (`high` / `xhigh` strength). `v3_*_glue_plan.json`
re-renders the song + a 4 s generated [Turnaround] + the theme's opening, so the end leads
into the theme by construction (reference chunks are re-synthesised, not sample-copied — find
the seam with make_loop, don't trust plan ms). `v3_*_game.mp3` = intro + loop; loop_start
13.328 s (high) / 13.026 s (xhigh), seam 0.11 / 0.17.
