#!/usr/bin/env python3
"""Generate src/game/data/moves.json from a compact spec.

Guarantees the per-type coverage contract in docs/mechanics/03-moves.md:
each of the 10 types gets quick / light / standard(phys) / standard(spec) /
heavy / nuke / a type-flavoured status move, plus a shared bank of Plain and
universal utility moves, plus ~30 abilities. Deterministic; re-runnable.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "src", "game", "data", "moves.json")

# Power-band defaults (power, accuracy, charges) from 03-moves.md
QUICK    = (40, 100, 30)
LIGHT    = (58, 100, 25)
STD      = (78, 100, 18)
HEAVY    = (92, 95, 12)
NUKE     = (115, 85, 8)

def slug(name):
    return name.lower().replace(" ", "_").replace("'", "")

moves = []
def add(name, typ, cat, band=None, power=0, acc=100, charges=20, priority=0,
        target="foe", effect=None, flags=None, desc="", signature=False):
    if band:
        power, acc, charges = band
    m = {
        "id": slug(name), "name": name, "type": typ, "category": cat,
        "power": power, "accuracy": acc, "charges": charges, "priority": priority,
        "target": target, "effect": effect, "flags": flags or [], "desc": desc,
    }
    if signature:
        m["signature"] = True
    moves.append(m)

# --- Per-type damaging + status kits -------------------------------------
# name pattern: (quick, light-spec, std-phys, std-spec, heavy, nuke, status)
TYPE_KIT = {
    "Ember":   ("Ember Jab", "Cinder Spit", "Flame Lash", "Hearth Pulse", "Pyre Slam", "Sunflare Burst",
                ("Scorch Veil", "status", {"status": "scorch", "chance": 100, "to": "foe"}, "Wreathes the foe in clinging hearth-sparks (Scorch).")),
    "Tide":    ("Brine Flick", "Mist Spray", "Wave Crash", "Tide Pulse", "Undertow", "Maelstrom",
                ("Drench Song", "status", {"status": "drench", "chance": 100, "to": "foe"}, "A heavy, sodden hum that slows the foe (Drench).")),
    "Verdant": ("Vine Tap", "Spore Puff", "Root Strike", "Bloomburst", "Bramble Crush", "Overgrowth",
                ("Sleep Pollen", "status", {"status": "doze", "chance": 75, "to": "foe", "accuracy": 75}, "Drifting glow-spores lull the foe to sleep (Doze).")),
    "Stone":   ("Pebble Toss", "Gravel Spray", "Rock Hurl", "Crystal Beam", "Boulder Smash", "Tremor Quake",
                ("Stone Wall", "status", {"stat": "def", "stages": 2, "to": "self"}, "Hunkers behind raised earth, sharply raising Defense.")),
    "Storm":   ("Spark Nip", "Static Jolt", "Thunder Kick", "Volt Arc", "Gale Slam", "Tempest",
                ("Numb Coil", "status", {"status": "numb", "chance": 100, "to": "foe", "accuracy": 90}, "A crackling coil of static leaves the foe twitching (Numb).")),
    "Frost":   ("Frost Nip", "Snow Veil", "Ice Fang", "Glacier Beam", "Avalanche", "Blizzard Howl",
                ("Chill Mist", "status", {"status": "chill", "chance": 30, "to": "foe", "accuracy": 95}, "A biting fog that may freeze the foe solid (Chill).")),
    "Solar":   ("Sun Jab", "Glint Ray", "Solar Lash", "Daybeam", "Flare Crown", "Sunburst Nova",
                ("Bask", "status", {"heal": 0.5, "to": "self"}, "Drinks stored daylight to restore half its health.")),
    "Lunar":   ("Moon Nip", "Dream Wisp", "Lunar Claw", "Moonbeam", "Nightfall Veil", "Eclipse Wave",
                ("Lull", "status", {"status": "doze", "chance": 100, "to": "foe", "accuracy": 60}, "A dreamlight whisper that always dozes — if it lands.")),
    "Light":   ("Glimmer", "Spark Mote", "Radiant Strike", "Light Pulse", "Prism Beam", "Dawnburst",
                ("Dazzle Flash", "status", {"status": "dazzle", "chance": 100, "to": "foe", "accuracy": 100}, "A blinding flare that confuses the foe (Dazzle).")),
    "Dark":    ("Shade Nip", "Gloom Spit", "Null Claw", "Hollow Pulse", "Shadow Rend", "Voidburst",
                ("Blight Touch", "status", {"status": "blight", "chance": 100, "to": "foe", "accuracy": 90}, "A creeping null that worsens each turn (Blight).")),
}

for typ, kit in TYPE_KIT.items():
    quick, lspec, sphys, sspec, heavy, nuke, status = kit
    add(quick, typ, "physical", QUICK, priority=1, flags=["contact"],
        desc=f"A fast {typ.lower()} strike that usually goes first.")
    add(lspec, typ, "special", LIGHT,
        desc=f"A reliable {typ.lower()} ranged hit.")
    add(sphys, typ, "physical", STD, flags=["contact"],
        desc=f"The workhorse physical {typ.lower()} move.")
    add(sspec, typ, "special", STD,
        desc=f"The workhorse special {typ.lower()} move.")
    add(heavy, typ, "physical", HEAVY, flags=["contact"],
        effect={"stat": "def", "stages": -1, "chance": 20, "to": "foe"},
        desc=f"A heavy {typ.lower()} blow that may soften the foe's guard.")
    add(nuke, typ, "special", NUKE,
        effect={"recoil": 0.25} if typ in ("Ember", "Storm", "Dark") else None,
        desc=f"A devastating {typ.lower()} barrage with a real downside.")
    sname, scat, seff, sdesc = status
    sacc = seff.pop("accuracy", 100) if isinstance(seff, dict) else 100
    add(sname, typ, scat, power=0, acc=sacc, charges=10,
        target="self" if (isinstance(seff, dict) and seff.get("to") == "self") else "foe",
        effect=seff, desc=sdesc)

# --- Plain (typeless) bank ------------------------------------------------
add("Pounce", "Plain", "physical", QUICK, priority=0, flags=["contact"], desc="A simple lunging tackle.")
add("Quick Jab", "Plain", "physical", (40, 100, 30), priority=2, flags=["contact"], desc="Always strikes first.")
add("Headbutt", "Plain", "physical", STD, effect={"flinch": 30}, flags=["contact"], desc="A blunt charge that may make the foe flinch.")
add("Slam", "Plain", "physical", HEAVY, flags=["contact"], desc="A heavy full-body slam.")
add("Throes", "Plain", "physical", (130, 100, 5), effect={"recoil": 0.33}, flags=["contact"], desc="A reckless all-out hit; the user is hurt by recoil.")
add("Gust Up", "Plain", "special", LIGHT, desc="A neutral buffeting pulse of air.")
add("Screech", "Plain", "status", power=0, acc=95, charges=10, effect={"stat": "def", "stages": -2, "to": "foe"}, desc="A grating cry that sharply lowers the foe's Defense.")
add("Goad", "Plain", "status", power=0, acc=100, charges=15, effect={"stat": "atk", "stages": -1, "to": "foe"}, desc="Taunts the foe into a sloppy stance, lowering Attack.")

# --- Universal utility / status bank --------------------------------------
add("Hone", "Plain", "status", power=0, acc=0, charges=20, target="self", effect={"stat": "atk", "stages": 1, "to": "self"}, desc="Sharpens focus, raising Attack.")
add("Focus Mind", "Plain", "status", power=0, acc=0, charges=20, target="self", effect={"stat": "spa", "stages": 1, "to": "self"}, desc="Centres the mind, raising Sp. Attack.")
add("Guard Up", "Plain", "status", power=0, acc=0, charges=20, target="self", effect={"stat": "def", "stages": 1, "to": "self"}, desc="Braces, raising Defense.")
add("Veil Up", "Plain", "status", power=0, acc=0, charges=20, target="self", effect={"stat": "spd", "stages": 1, "to": "self"}, desc="Steadies, raising Sp. Defense.")
add("Swift Step", "Plain", "status", power=0, acc=0, charges=20, target="self", effect={"stat": "spe", "stages": 2, "to": "self"}, desc="A burst of footwork, sharply raising Speed.")
add("Mend", "Plain", "status", power=0, acc=0, charges=10, target="self", effect={"heal": 0.5, "to": "self"}, desc="Tends its wounds, restoring half its health.")
add("Rest Up", "Plain", "status", power=0, acc=0, charges=5, target="self", effect={"heal": 1.0, "to": "self", "status": "doze", "selfDoze": 2}, desc="Sleeps deeply: fully heals but Dozes for two turns.")
add("Cleanse", "Plain", "status", power=0, acc=0, charges=10, target="self", effect={"cure": True, "to": "self"}, desc="Shakes off any status condition.")
add("Caltrops", "Plain", "status", power=0, acc=0, charges=10, target="field", effect={"hazard": "caltrops"}, desc="Scatters debris; foes that switch in take chip damage.")
add("Mist Screen", "Plain", "status", power=0, acc=0, charges=10, target="field", effect={"screen": "special", "turns": 5}, desc="A haze that halves special damage to your side for a while.")
add("Bulwark", "Plain", "status", power=0, acc=0, charges=10, target="field", effect={"screen": "physical", "turns": 5}, desc="A ward that halves physical damage to your side for a while.")
add("Swap Out", "Plain", "status", power=0, acc=0, charges=15, target="self", priority=0, effect={"pivot": True}, desc="Slips back to the party after acting (a clean switch).")
add("Lifedrain", "Verdant", "special", (60, 100, 12), effect={"drain": 0.5}, desc="Saps the foe, healing the user for half the damage dealt.")
add("Sun Nap", "Solar", "status", power=0, acc=0, charges=10, target="self", effect={"heal": 0.5, "to": "self", "needs": "sun"}, desc="Curls up in the light; restores more health under sun.")

# --- Signature moves (existing starters; more added during flesh-out) -----
add("Tuft Spark", "Ember", "special", (45, 100, 25), priority=1, signature=True,
    desc="Vulpyre's signature: a quick crackle from its mane that almost always strikes first.")
add("Bubble Hum", "Tide", "special", (60, 100, 15), effect={"stat": "atk", "stages": -1, "chance": 100, "to": "foe"}, signature=True,
    desc="Brinix's signature: a soothing pulse that always saps the foe's Attack.")

# --- Abilities ------------------------------------------------------------
abilities = [
    # Minor (+10)
    {"id": "brisk", "name": "Brisk", "tier": "minor", "eps": 10, "effect": {"stat": "spe", "mult": 1.5, "when": "sun"}, "desc": "Speed rises in bright sun."},
    {"id": "thickcoat", "name": "Thickcoat", "tier": "minor", "eps": 10, "effect": {"resist": "Frost"}, "desc": "Takes less damage from Frost moves."},
    {"id": "surefoot", "name": "Surefoot", "tier": "minor", "eps": 10, "effect": {"noDrop": "spe"}, "desc": "Its Speed cannot be lowered."},
    {"id": "keen", "name": "Keen", "tier": "minor", "eps": 10, "effect": {"crit": 1}, "desc": "Lands critical hits more often."},
    {"id": "forager", "name": "Forager", "tier": "minor", "eps": 10, "effect": {"healOnKO": 0.25}, "desc": "Recovers a little health after felling a foe."},
    {"id": "cozy", "name": "Cozy", "tier": "minor", "eps": 10, "effect": {"regen": 0.0625}, "desc": "Slowly recovers health each turn."},
    # Standard (+20)
    {"id": "emberheart", "name": "Emberheart", "tier": "standard", "eps": 20, "effect": {"boostType": "Ember", "mult": 1.5, "when": "belowHalf"}, "desc": "Ember moves hit harder below half HP."},
    {"id": "verdant_vigor", "name": "Verdant Vigor", "tier": "standard", "eps": 20, "effect": {"boostType": "Verdant", "mult": 1.5, "when": "belowHalf"}, "desc": "Verdant moves hit harder below half HP."},
    {"id": "tidecaller", "name": "Tidecaller", "tier": "standard", "eps": 20, "effect": {"regen": 0.0625, "when": "water"}, "desc": "Recovers health each turn in water or rain."},
    {"id": "static_skin", "name": "Static Skin", "tier": "standard", "eps": 20, "effect": {"contactStatus": "numb", "chance": 30}, "desc": "Contact may leave the attacker Numb."},
    {"id": "bramble", "name": "Bramble", "tier": "standard", "eps": 20, "effect": {"contactRecoil": 0.125}, "desc": "Attackers that make contact take chip damage."},
    {"id": "stonehide", "name": "Stonehide", "tier": "standard", "eps": 20, "effect": {"physTaken": 0.75}, "desc": "Takes 25% less physical damage."},
    {"id": "mistveil", "name": "Mistveil", "tier": "standard", "eps": 20, "effect": {"onSwitchIn": {"stat": "acc", "stages": -1, "to": "foe"}}, "desc": "Lowers the foe's accuracy on switch-in."},
    {"id": "coldblood", "name": "Coldblood", "tier": "standard", "eps": 20, "effect": {"immuneStatus": "chill", "regen": 0.0625, "when": "hail"}, "desc": "Immune to Chill; heals in hail."},
    {"id": "sunsoak", "name": "Sunsoak", "tier": "standard", "eps": 20, "effect": {"regen": 0.0625, "when": "sun"}, "desc": "Recovers health each turn in sun."},
    {"id": "nightsight", "name": "Nightsight", "tier": "standard", "eps": 20, "effect": {"noAccLoss": True, "stat": "spe", "mult": 1.25, "when": "night"}, "desc": "Never misses from low accuracy; faster at night."},
    {"id": "insulate", "name": "Insulate", "tier": "standard", "eps": 20, "effect": {"immune": "Storm"}, "desc": "Unaffected by Storm moves."},
    {"id": "sponge", "name": "Sponge", "tier": "standard", "eps": 20, "effect": {"absorb": "Tide", "heal": 0.25}, "desc": "Tide moves heal it instead of harming."},
    {"id": "cinderveil", "name": "Cinderveil", "tier": "standard", "eps": 20, "effect": {"absorb": "Ember", "heal": 0.25}, "desc": "Ember moves heal it instead of harming."},
    {"id": "grounded", "name": "Grounded", "tier": "standard", "eps": 20, "effect": {"immune": "Storm", "noDrop": "def"}, "desc": "Earthed against Storm; its Defense can't drop."},
    # Strong (+30)
    {"id": "daybringer", "name": "Daybringer", "tier": "strong", "eps": 30, "effect": {"onSwitchIn": {"weather": "sun"}}, "desc": "Summons bright sun on entering battle."},
    {"id": "nightfall", "name": "Nightfall", "tier": "strong", "eps": 30, "effect": {"onSwitchIn": {"weather": "night"}}, "desc": "Draws down night on entering battle."},
    {"id": "aurora_guard", "name": "Aurora Guard", "tier": "strong", "eps": 30, "effect": {"onSwitchIn": {"weather": "hail"}}, "desc": "Calls an aurora-hail on entering battle."},
    {"id": "stormcall", "name": "Stormcall", "tier": "strong", "eps": 30, "effect": {"onSwitchIn": {"weather": "storm"}}, "desc": "Calls a storm on entering battle."},
    {"id": "lumenward", "name": "Lumenward", "tier": "strong", "eps": 30, "effect": {"partyResist": "Dark"}, "desc": "Your party takes less damage from Dark moves."},
    {"id": "nullheart", "name": "Nullheart", "tier": "strong", "eps": 30, "effect": {"immuneStatus": "all"}, "desc": "Cannot be afflicted by any status."},
    {"id": "phoenix", "name": "Phoenix", "tier": "strong", "eps": 30, "effect": {"endure": "once"}, "desc": "Once per battle, survives a fatal hit at 1 HP."},
    {"id": "mirrorlight", "name": "Mirrorlight", "tier": "strong", "eps": 30, "effect": {"reflectStatus": "first"}, "desc": "Reflects the first status move used on it."},
]

data = {
    "_notes": "Generated by tools/balance/gen_moves.py from docs/mechanics/03-moves.md. Re-run to regenerate. 'Plain' is the typeless move category (never STAB, always x1). Effects are read by the battle engine and the simulator.",
    "version": 1,
    "count": {"moves": len(moves), "abilities": len(abilities)},
    "moves": moves,
    "abilities": abilities,
}

with open(OUT, "w") as f:
    json.dump(data, f, indent=2)
print(f"Wrote {len(moves)} moves and {len(abilities)} abilities to {OUT}")
