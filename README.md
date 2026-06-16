# MAGAZINE

High-end single-model magazine and runway editorial prompts for the GFE roster.

## Layout

```
{Model Name}/       # 10 supermodel folders at repo root (GFE-matching tree)
  01_casting_shots/     # studio editorial prompt + hero images
  02_reference_views/   # runway editorial prompt + reference images
  SCENES/
  VARIATIONS/
  CLIPS/
  PROMOTIONAL/
  STAGED SHOTS/
scripts/            # generators + folder bootstrap
lib/                # legacy GFE roster data
prompts/            # legacy flat prompts (pre-v1.3)
```

## Bootstrap folders

```bash
cd scripts
python ensure_magazine_folder_structure.py
```

## Regenerate prompts

```bash
cd scripts
python fashion_modeling_prompt_generator.py
```

## Usage

Copy the **Imagine prompt paragraph** from `{Name}/01_casting_shots/` or `02_reference_views/` into Grok Imagine (16:9).
