# MAGAZINE

High-end supermodel magazine and runway editorial prompts for the Girlfriend Experience roster.

## Split architecture

| Layer | Repo / path | Contents |
|-------|-------------|----------|
| **MAGAZINE** (this repo) | `MAGAZINE/` | Prompt generators, roster data, folder bootstrap |
| **STUDIO** | `Studio/Magazine_Assets/` | All model folders, editorial prompts, hero images |

Sibling layout:

```
Grok Projects/
├── MAGAZINE/         ← you are here (scripts)
└── Studio/
    └── Magazine_Assets/   ← {Anya Petrova, …} model asset folders
```

## Scripts

Requires `Studio/` as a sibling folder:

```bash
cd scripts
python ensure_magazine_folder_structure.py
python fashion_modeling_prompt_generator.py
```

All outputs land in `../Studio/Magazine_Assets/{Name}/`.
