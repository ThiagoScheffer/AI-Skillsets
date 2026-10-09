# Scripts

All included scripts use the Python standard library only.

They are intentionally conservative and perform structural checks. They do not prove software correctness or compliance.

Run from the skill-pack root, pointing to the application repository:

```bash
python scripts/validate_sdlc.py /path/to/app
python scripts/trace_requirements.py /path/to/app
python scripts/detect_drift.py /path/to/app
python scripts/generate_status.py /path/to/app
```
