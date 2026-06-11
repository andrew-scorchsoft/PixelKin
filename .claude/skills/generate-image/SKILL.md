---
name: generate-image
description: Generate brand-aligned images for the product and e-learning content via Google Nano Banana Pro (preferred) or OpenAI gpt-image-2. Use whenever the user asks for an image, illustration, infographic, hero, icon, or any visual asset that should be saved into the repo. Accepts optional input images for edit / restyle / compose / reference workflows. Strips standard EXIF/XMP metadata, re-encodes to WebP for repo-friendly size, and supports a brand-aligned style preset library.
---

# generate-image

A skill for producing images that fit the Control Standard brand and the e-learning content built on top of it. The heavy lifting is a single Python script; this document tells you when and how to use it.

## When to use

- The user asks for an image, illustration, infographic, hero, icon, chart, or sketch.
- You are producing e-learning content and need visuals to go alongside it.
- An existing image needs to be regenerated in a different style or aspect ratio.

Do **not** invoke this for: simple SVG icons you can hand-write, CSS-only graphics, or anything where a static asset already exists in the repo and the user has not asked for a replacement.

## Prerequisites

The script needs `Pillow` and `requests`, both of which come in via the project's `requirements.txt` (Pillow transitively through `qrcode[pil]`). **Always invoke via the project venv** — `./venv/bin/python ...` from the repo root. Bare `python` is not on `PATH` in this environment and will fail with `command not found`, and the system `python3` won't have the project's deps. If you hit `ModuleNotFoundError: No module named 'PIL'`, you're running outside the venv.

At least one provider key must be set in the environment:

| Env var                    | Provider | Model (default)              | Notes                |
|----------------------------|----------|------------------------------|----------------------|
| `GOOGLE_AI_STUDIO_API_KEY` | Google   | `gemini-3-pro-image-preview` | Nano Banana Pro. **Preferred** when both are set. |
| `OPENAI_API_KEY`           | OpenAI   | `gpt-image-2`                | Fallback.            |

Optional overrides: `GOOGLE_IMAGE_MODEL`, `OPENAI_IMAGE_MODEL`.

If neither is set, the script exits with a clear error — surface that to the user and ask which key they'd like to add.

## How to call it

The script lives at `.claude/skills/generate-image/scripts/generate.py`. Run it via Bash from the repo root, using the project venv's Python:

```bash
./venv/bin/python .claude/skills/generate-image/scripts/generate.py \
  --prompt "A diagram showing the four phases of the Control Standard loop" \
  --style brand-flat-infographic \
  --aspect 16:9 \
  --output app/static/images/elearning/control-loop.webp
```

Do not use bare `python` (not on `PATH`) or `python3` (lacks project deps) — always `./venv/bin/python`.

It prints a JSON summary on success (path, dimensions, bytes, provider, model).

### Arguments worth knowing

- `--prompt` *(required)* — the brief. Keep it concrete; describe content, composition, mood. The style preset handles palette/look.
- `--output` *(required)* — destination path. Extension picks the format: `.webp` (default choice for the repo), `.png`, `.jpg`. **Prefer `.webp`.**
- `--style` — preset key (see below). Omit for a raw, unstyled generation.
- `--aspect` — one of `1:1 4:3 3:4 16:9 9:16 3:2 2:3`. Default `1:1`.
- `--quality` — WebP/JPEG quality (1–100). Default 85, which is the sweet spot for repo files.
- `--lossless` — switch to lossless WebP. Use only when the user explicitly needs it; files get much larger.
- `--max-dim` — longest edge in pixels; the image is downscaled if larger. Default 2048. Set `0` to disable.
- `--provider` — force `google` or `openai`. Skip this unless the user asks.
- `--transparent` — produce a real alpha-channel transparent background. Requires `.png` or `.webp` output. When set, the script auto-prefers OpenAI over Google (Google has no native alpha) and auto-selects `gpt-image-1` instead of the default `gpt-image-2` (only `gpt-image-1` accepts `background=transparent`). Both auto-selections are skipped if the caller hard-pins via `--provider` or `OPENAI_IMAGE_MODEL`. Behaviour differs by provider:
  - **OpenAI**: native — passes `background=transparent` to `gpt-image-1`, which returns a PNG with real alpha.
  - **Google Nano Banana / Gemini**: the image endpoint does **not** support native alpha output. The script prepends an anti-checkerboard preamble asking the model to render on pure magenta `#FF00FF`, then chroma-keys that colour out with feathered edges in post-processing. Side effects: do not ask for magenta/pink elements inside the subject (they'll be deleted), and verify the output with `Read` — the chroma-key occasionally leaves a faint pink halo on soft edges; regenerate with a request for crisper edges if it does. The JSON summary reports `transparency_method: "chroma_key"` vs `"native"` so you know which path ran. **Failure mode:** the model sometimes ignores the magenta instruction and bakes an OPAQUE background (white / grey / a checkerboard) the key can't strip — the script then prints a loud `⚠️ TRANSPARENCY LIKELY FAILED` warning. When you see it, **don't ship the result**: regenerate with native alpha (let it default to OpenAI — don't force `--provider google`) and add *"fully transparent background, render nothing behind it, NO checkerboard / grey squares / grid"* to the prompt. **Prefer native alpha for any object that must drop cleanly onto a map.**
- `--input-image` — path to a local image file to feed into the model as visual context. **Repeat the flag for multiple inputs** (e.g. `--input-image hero.png --input-image logo.png`). Accepts `.png`, `.jpg`, `.jpeg`, `.webp` up to 20 MiB each. See "Using existing images as input" below.
- `--openai-route` — `edits` (default) or `responses`. Only relevant when `--input-image` is set and the provider is OpenAI. See "Using existing images as input" below.
- `--list-styles` — print all presets with descriptions.

### Using existing images as input

Both providers accept image input alongside the text prompt. The image isn't necessarily *being edited* — it can also serve as a style reference, composition reference, character reference, mood/lighting reference, or background asset to compose into a larger scene. The prompt decides which role each image plays.

**Google Nano Banana / Gemini** sends input images as `inlineData` parts on the multimodal `contents.parts` array — a single route that handles everything. Gemini was designed for this and tends to preserve subject identity well; it's the **preferred** path for most image-input workflows.

**OpenAI** has two routes, selectable via `--openai-route`:

| Route | Endpoint | Model | When to use |
|-------|----------|-------|-------------|
| `edits` *(default)* | `/v1/images/edits` | `gpt-image-2` (or `gpt-image-1` if `--transparent`) | **One-shot** generation with reference/edit images. The endpoint is named "edits" but with `gpt-image-1`/`gpt-image-2` it accepts up to 16 input images as references — the prompt decides whether they're edited, restyled, composed, or just used for style/colour/mood guidance. Best when you want to pin the image model explicitly. |
| `responses` | `/v1/responses` | `gpt-5` (override via `OPENAI_RESPONSES_MODEL`) | **Multimodal context.** The input images become real visual context on a text model, which then calls the `image_generation` tool to produce the output. Better mental model when the images are *background context* (mood board, brand guidelines, layout inspiration) rather than the subject of an edit. |

For day-to-day use, leave `--openai-route` at its default `edits`. Reach for `responses` when you want the model to reason over the inputs as conversational context — e.g. "look at these three brand boards and synthesise something in that direction" — rather than treating any one of them as the canvas to modify.

When to reach for input images at all:

- *Edit an existing visual*: "make the sky stormy", "swap the suit for chef's whites", "remove the laptop and put a clipboard in their hands".
- *Restyle*: take a photographic reference and ask for the same composition rendered in `brand-flat-infographic`.
- *Compose multiple inputs*: pass a character sheet plus a background plate and brief the model on how to combine them.
- *Visual reference, not literal copy*: "match the colour palette and lighting of this image" — pass the reference and say so explicitly in the prompt.
- *Character/brand consistency across a batch*: pass the same reference image to every generation in a set to keep faces, props, or brand marks consistent.

Practical notes:

- **Be explicit about each image's role** when passing more than one. "Image 1 is the product; preserve it accurately. Image 2 is only for lighting mood. Image 3 is layout inspiration." Otherwise the model will blend everything in ways you didn't intend.
- **What to change vs. preserve** — "keep the pose and lighting; change the jacket from leather to wool" beats "edit this jacket".
- The `--style` preset suffix still applies to the *output* — useful for "take this rough photo and rebuild it in the brand line-illustration style".
- `--aspect` controls the output canvas, not the input crop. Set it explicitly if you need the output to match the input.
- The self-check loop runs as normal. Image-input generations often need 2-3 iterations to land — name what's wrong specifically when regenerating.
- The JSON summary echoes the resolved input paths under `input_images` and the OpenAI route used under `openai_route` (`generations` / `edits` / `responses`).

Examples:

```bash
# One-shot edit (default route — /v1/images/edits, gpt-image-2)
./venv/bin/python .claude/skills/generate-image/scripts/generate.py \
  --prompt "Keep the pose and the lighting. Change the jacket from leather to a navy wool peacoat." \
  --input-image app/static/images/elearning/leadership/reference-portrait.webp \
  --style brand-photo-editorial \
  --aspect 3:4 \
  --output app/static/images/elearning/leadership/portrait-peacoat.webp

# Multiple references with explicit roles (still one-shot edits route)
./venv/bin/python .claude/skills/generate-image/scripts/generate.py \
  --prompt "Image 1 is the character; preserve face and outfit. Image 2 is the room background. Compose them into a single editorial shot." \
  --input-image refs/character.png \
  --input-image refs/room.png \
  --style brand-photo-editorial \
  --output app/static/images/content/composed-shot.webp

# Multimodal context via Responses API (reasons over references, then generates)
./venv/bin/python .claude/skills/generate-image/scripts/generate.py \
  --prompt "Synthesise a hero illustration in the direction implied by these three brand boards. Don't copy any one of them; produce a fresh composition that captures the shared mood." \
  --input-image refs/board-1.png \
  --input-image refs/board-2.png \
  --input-image refs/board-3.png \
  --openai-route responses \
  --provider openai \
  --output app/static/images/content/synth-hero.webp
```

## Style presets

Defined in `scripts/styles.json`. The `brand-*` presets are pinned to the Control Standard palette (paper `#F5F1EA`, ink `#0F1B2D`, signal red `#C8211B`) and should be your default for anything that lives inside the product or its e-learning content.

| Key                       | Use it for                                                              |
|---------------------------|-------------------------------------------------------------------------|
| `brand-flat-infographic`  | Concept diagrams, process flows, comparison panels.                     |
| `brand-isometric-diagram` | Systems, architectures, multi-step processes in 3/4 perspective.        |
| `brand-line-illustration` | Section openers, chapter headers, quiet supporting visuals.             |
| `brand-whiteboard-sketch` | Explainer-style sketches for e-learning walkthroughs.                   |
| `brand-photo-editorial`   | Module heroes and chapter opener photography.                           |
| `brand-icon-mark`         | Single-concept icons for UI, course nav, inline content.                |
| `brand-data-viz`          | Mock charts and dashboards (illustrative, not real data).               |
| `brand-artifact-mockup`   | Rendered emails, status updates, Slack messages, tickets, sign-off notes — when the document itself is the lesson. |
| `brand-timeline`          | Horizontal time-axis visuals: cycles, review cadences, spaced-review beats, escalation rhythms. |
| `neutral-flat-vector`     | Flat vector when brand alignment isn't required.                        |
| `neutral-photo`           | General-purpose photography when brand alignment isn't required.        |

### When no preset fits — defining a custom style inline

The preset list is the default; it is not a cage. If you've looked through it and genuinely none of the brand presets fit the moment, you may **omit `--style` and bake style direction into `--prompt` itself**. The script applies the style suffix only when `--style` is set, so a prompt with no `--style` flag is delivered to the model as-is — write the brief and the style guidance together.

Keep the bar high:

- The image must still sit inside the Control Standard palette (paper `#F5F1EA`, ink `#0F1B2D`, signal red `#C8211B`) and the brand's no-gradient / no-3D / no-stock-photo rules. The presets aren't the brand; the brand is the brand.
- Spell the style direction in the same shape the presets use — surface, palette with hex codes, line weight or texture, what to avoid. Hand-wavy direction ("modern infographic style") will produce hand-wavy output.
- Note in your response to the user that you used a custom style and why no preset fit. This is the signal that triggers the next rule.
- **If you find yourself reaching for the same custom style twice, propose adding it to `styles.json`.** A one-off is fine; a recurring "ad-hoc" style is a preset waiting to be born, and inconsistency between two near-identical inline styles is exactly the brand drift the preset library exists to prevent.

## The self-check loop — this is mandatory

The script generates and saves but does **not** judge whether the image matches the brief. You do that. Each call costs money; **a regeneration is not free**, so be deliberate.

After every successful generation:

1. **Open the saved file** with the `Read` tool (it renders images visually). Inspect it.
2. **Verify against the brief.** Check for:
   - Subject and composition match the prompt.
   - **No extra limbs, fused fingers, melted objects, or other obvious artifacts.**
   - **Style preset honoured** — palette, line weight, no rogue gradients/3D where the preset forbids them.
   - **Aspect ratio** matches what you asked for.
   - **Specific garment cuts, props, and poses** — models tend to drift toward generic versions (e.g. harem trousers rendering as plain joggers, peaked librarian glasses as plain rectangles). If a detail is load-bearing for the brief, call it out explicitly in the regenerate prompt with a contrast (e.g. *"trousers must be gathered tightly at the knee, not straight-leg joggers"*).
3. **If the brief involves any words or labels in the image**, do the text sub-checklist:
   - Read every visible word out loud (mentally). Spelling must be exact.
   - No phantom letters, no doubled characters, no nonsense glyphs.
   - Required words from the brief are all present.
   - **If text matters and image-model text rendering keeps failing, propose to the user that the text be overlaid in HTML/CSS over a text-free image instead** — that's almost always the right call for e-learning.
4. **If it passes**, report the file path and JSON summary to the user. Done.
5. **If it fails**, regenerate with an adjusted prompt that *names the specific problem* — e.g. append `"All text must be spelled correctly: 'Diagnose, Decide, Deploy, Detect'."` or `"Hands held behind back; do not draw fingers."` Use a **maximum of 3 attempts** for the same brief. If it still fails on attempt 3, stop and report what's wrong — don't burn API budget in a loop.

Keep track of attempts mentally; do not exceed three regenerations without user input.

## Generating multiple images — parallel and background

Each invocation is one image. When you need several, do not run them in series — that wastes wall-clock time and burns prompt cache while you sit idle.

**Parallel (preferred when you have all the briefs up front).** Fire one `Bash` call per image in a *single response* — the harness runs them concurrently. Three images that each take ~45s finish in ~45s, not ~135s. The self-check loop still runs per file after they all return; inspect each with `Read`, and only regenerate the ones that fail.

**Background (preferred when you have other work to do while images render).** Kick the generation off with `run_in_background: true` on the `Bash` call, then continue with non-image work (drafting React, editing the manifest, reading the chapter). You'll be notified when the command completes — do not poll or sleep. When it finishes, run the self-check loop.

**Combine both.** Fire N generations in parallel, all with `run_in_background: true`, then proceed to other work. Inspect each as its notification arrives.

Rules that still apply:

- **Plan all briefs before firing.** Decide style preset, aspect, output path, and prompt for every image up front. Mid-batch redesigns waste the parallelism.
- **Distinct output paths.** Two concurrent calls writing the same `--output` will clobber each other.
- **The 3-attempt cap is per image, not per batch.** If one image fails its self-check, that image gets up to 3 attempts; the others are unaffected.
- **Do not parallelise *regenerations* of the same brief.** Inspect the first result, adjust the prompt, then try again. Firing three variants in parallel hoping one sticks is exactly the API-budget burn the self-check loop exists to prevent.

## Path conventions

When saving into the repo:

- E-learning visuals: `app/static/images/elearning/<topic>/<name>.webp`
- Product UI imagery: `app/static/images/<area>/<name>.webp`
- One-off content (blog, marketing): `app/static/images/content/<slug>.webp`
- Documentation imagery: `docs/assets/<name>.webp`
- Throwaway / preview / personal experiments: `tmp/<name>.webp` (gitignored; safe for one-offs the user does not want in the repo)

Use kebab-case filenames. Reference assets through the `static_versioned` filter in templates (per `CLAUDE.md`).

## What this skill deliberately does *not* do

- **Does not strip SynthID** (Google) or attempt to remove pixel-space watermarks. They're harmless and required by usage policy.
- **Does not preserve C2PA Content Credentials** through the re-encode — re-encoding breaks the signature. Standard EXIF/XMP/PNG text chunks (which can include the raw prompt, timestamps, and model identifiers) *are* stripped, which is the intent.
- **Does not auto-commit** generated images. Show the user the result first and let them decide what to keep.
- **Does not generate real charts from real data.** The data-viz preset produces illustrative imagery only. For real charts, use a charting library.
