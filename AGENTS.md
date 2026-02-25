# AGENTS.md

## Cursor Cloud specific instructions

### Project overview

AI-Generated Blog — a static blog built with Pelican that uses OpenAI GPT-4o for article generation and DALL-E 3 for cover images. See `README.md` for full architecture and configuration details.

### Key commands

| Task | Command |
|---|---|
| Install deps | `pip install -r requirements.txt` (note: `pelican-readtime>=1.0.0` does not exist; install `pelican-readtime` without version pin) |
| Run tests | `pytest tests/ -v` |
| Lint | `flake8 content_pipeline/` |
| Format check | `black --check content_pipeline/` |
| Type check | `mypy content_pipeline/` |
| Build site | `pelican content -s simple_build.py` (no plugins, best for testing) |
| Build site (full) | `pelican content -s pelicanconf.py` (requires sitemap/seo/neighbors plugins) |
| Dev server | `pelican --listen --port 8000 --bind 0.0.0.0` (after building) |
| Generate content | `python -m content_pipeline.generator` (requires `OPENAI_API_KEY`) |

### Non-obvious caveats

- **`pelican-readtime` version**: `requirements.txt` specifies `>=1.0.0` but the latest PyPI release is `0.2.1`. Install without version constraint: `pip install pelican-readtime`.
- **`tests/__init__.py` encoding**: This file was originally UTF-16LE encoded, causing `SyntaxError: source code string cannot contain null bytes`. It has been fixed to UTF-8.
- **Pelican plugins (sitemap, seo, neighbors)**: These are referenced in `pelicanconf.py` but not installed as pip packages. Use `simple_build.py` (which sets `PLUGINS = []`) for local builds/testing to avoid plugin errors.
- **`PATH` for user-installed tools**: Tools like `pelican`, `flake8`, `black`, `mypy` install to `~/.local/bin`. Ensure `export PATH="$HOME/.local/bin:$PATH"` is set.
- **5 pre-existing test failures**: Some tests have mock setup issues incompatible with newer `openai` library versions (e.g., `Mock` objects not subscriptable for `choices[0]`). These are not environment issues.
- **No OpenAI API key needed for dev/test**: Unit tests mock the OpenAI API. The key is only needed for actual content generation.
- **`TYPOGRIFY = True`** in `pelicanconf.py` will cause build errors unless `typogrify` is installed. `simple_build.py` avoids this.
