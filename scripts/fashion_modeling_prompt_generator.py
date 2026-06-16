#!/usr/bin/env python3
"""Fashion Magazine Modeling Prompt Generator — MAGAZINE repo."""

from __future__ import annotations

import re
import sys
from datetime import datetime
from pathlib import Path

MAGAZINE_ROOT = Path(__file__).resolve().parent.parent
LIB = MAGAZINE_ROOT / "lib"
sys.path.insert(0, str(LIB))

from gfe_roster_data import GFE_ROSTER_20
OUTPUT_DIR = MAGAZINE_ROOT / "prompts"

MAGAZINE_OUTFITS: dict[str, str] = {
    "Aiko": "asymmetric avant-garde shimmering metallic petal gown in sapphire jewel tones with sculptural draping",
    "Vesper": "gothic haute couture black velvet column gown with deep wine silk panels and architectural shoulder wings",
    "Mika": "deconstructed crimson silk couture dress with exposed seam tailoring and tattoo-revealing sheer mesh insets",
    "Sora": "soft pink organza tiered editorial gown with cloud-like volume and delicate pearl-thread embroidery",
    "Hana": "ivory satin couture slip-gown with black Chantilly lace architecture and Kyoto-minimal train",
    "Rin": "hot pink sculptural latex-neoprene hybrid mini-gown with neon piping and Harajuku runway energy",
    "Yume": "coral sunset ombré silk charmeuse gown with island-wave pleating and open back drape",
    "Kira": "charcoal structured wool-silk fusion coat-dress with razor tailoring and elongated executive silhouette",
    "Luna": "terracotta copper-thread jacquard gown with Oaxaca-inspired geometric bodice and fluid train",
    "Nova": "electric blue iridescent tech-fabric couture dress with LED-thread accents and cyber-editorial cut",
    "Ember": "burnt orange velvet burnout gown with jazz-club fringe panels and smoky ombré hem",
    "Jade": "jade green liquid-satin couture dress with mandala pleat origami bodice and gold filament trim",
    "Scarlet": "scarlet lacquered silk ball-gown bodice with sculpted peplum and high-slit editorial skirt",
    "Violet": "violet ombré carnival tulle couture dress with carnival-to-couture ruffle architecture",
    "Raven": "midnight blue deconstructed lace gown with Portland-goth torn-hem train and matte silk underlay",
    "Willow": "sage green flowing bamboo-silk editorial gown with wellness-luxe drape and bare-shoulder cut",
    "Iris": "champagne Parisian couture column dress with honey balayage-complementing silk and gold chain harness",
    "Sage": "forest green literary-chic wool crepe gown with glasses-chain detail and gold-leaf collar sculpt",
    "Lyra": "seafoam silk chiffon island-pop couture dress with ukulele-strap-inspired asymmetric strapwork",
    "Niko": "gold lamé night-market couture jumpsuit-gown with Thai silk paneling and street-luxe tailoring",
}


def _tattoo_visual(actor) -> str:
    inv = actor.tattoo_inventory
    if inv.startswith("Heavy"):
        return "full irezumi sleeve tattoos and floral choker band"
    if inv.startswith("Moderate"):
        return "botanical half-sleeve and sternum tattoos"
    if inv.startswith("Light"):
        return "subtle fine-line wrist and collarbone tattoos"
    return "no visible tattoos"


def _physical_compact(actor) -> str:
    text = actor.base_physical_description.strip().rstrip(".")
    return re.sub(r"^5'[\d.]+\"\s*,?\s*", "", text)


def visuals_from_actor(actor) -> str:
    hook = actor.signature_looks.split(";")[0].split(",")[0].strip().lower()
    return f"{hook}, {_tattoo_visual(actor)}, {_physical_compact(actor)}"


class MagazineModelingPromptGenerator:
    def __init__(self) -> None:
        self.version = "1.1"
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        print(f"Magazine Assets folder ready: {OUTPUT_DIR}")

    def build_magazine_prompt(
        self,
        name: str,
        age: int,
        ethnicity: str,
        visuals: str,
        outfit: str,
        scene: str = "studio",
    ) -> str:
        base = (
            f"photorealistic high-fidelity 16:9 magazine editorial photograph, single "
            f"{age}-year-old {ethnicity} woman named {name}, {visuals}, wearing {outfit}, "
            f"elegant confident pose with intense gaze to camera, dramatic cinematic lighting "
            f"with soft shadows and high contrast highlights on fabric and skin, ultra-detailed "
            f"textures, sharp focus, Vogue-level professional fashion photography, expensive "
            f"avant-garde haute couture aesthetic, natural physics dress drape and movement, "
            f"commercial-ready high-end magazine cover quality"
        )
        if scene == "runway":
            base += (
                ", dynamic mid-stride runway walk on minimalist catwalk, motion blur on fabric "
                "edges, dramatic spot lighting"
            )
        return base

    def generate(self, model_data: dict, scene: str = "studio") -> str:
        prompt = self.build_magazine_prompt(
            name=model_data["name"],
            age=model_data["age"],
            ethnicity=model_data["ethnicity"],
            visuals=model_data["visuals"],
            outfit=model_data["outfit"],
            scene=scene,
        )
        filename = OUTPUT_DIR / f"{model_data['name']}_Magazine_{scene}.txt"
        lines = [
            prompt,
            "",
            f"# {model_data['name']} — {scene.upper()} Magazine Shot Prompt v{self.version}",
            f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "# Copy the first line into Grok Imagine. Aspect ratio: 16:9",
            "",
        ]
        filename.write_text("\n".join(lines), encoding="utf-8")
        print(f"✅ Saved single-model magazine shot prompt: {filename}")
        return prompt


def main() -> int:
    gen = MagazineModelingPromptGenerator()
    count = 0
    for actor in GFE_ROSTER_20:
        outfit = MAGAZINE_OUTFITS.get(actor.stage_name)
        if not outfit:
            print(f"⚠️  Missing outfit for {actor.stage_name}, skipping")
            continue
        model_data = {
            "name": actor.stage_name,
            "age": actor.age,
            "ethnicity": actor.ethnicity,
            "visuals": visuals_from_actor(actor),
            "outfit": outfit,
        }
        gen.generate(model_data, scene="studio")
        gen.generate(model_data, scene="runway")
        count += 2

    print(f"\nAll single-model high-end magazine shots generated ({count} prompts).")
    print(f"Ready for Grok Imagine or video base plates: {OUTPUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())