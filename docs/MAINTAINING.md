# Maintaining the BBROSE profile

This repository is not a product. It exists so that `README.md` renders as the
public profile page at **[github.com/bbrosecompany-code](https://github.com/bbrosecompany-code)**.

GitHub gives this treatment to a repository whose name matches the account name
— `bbrosecompany-code/bbrosecompany-code`. The root `README.md` is the page.

> The `.github/profile/README.md` layout you'll find in most guides is the
> **organisation** convention. This account is a user account, so that layout
> would render nothing. Don't "fix" the structure to match those guides.

## What's in here

| Path | Purpose |
|---|---|
| `README.md` | The profile page itself |
| `assets/` | Banner + ornament SVGs it references |
| `tools/build_banners.py` | Regenerates everything in `assets/` |

## Rules that keep it from breaking

1. **Default branch must stay `main`.** Images are referenced by absolute
   `raw.githubusercontent.com/.../main/assets/...` URLs. Renaming the branch
   blanks every image on the profile.
2. **This repo must stay public.** A private profile repo means GitHub shows no
   profile page at all.
3. **Anything pushed to `main` is live immediately.** There is no preview step,
   so open a PR first if the change is more than a typo.
4. **Images are cached by GitHub's camo proxy.** After changing an SVG the old
   version can persist for a few minutes. Hard-refresh before assuming it broke.

## Regenerating the banners

The banners embed the real BBROSE wordmark as a base64 data URI. GitHub renders
README SVGs inside `<img>`, where externally-referenced images and web fonts are
blocked, so everything must be self-contained — that's also why type is set in a
system serif stack rather than Playfair.

Brand tokens are taken verbatim from the live site's `static/css/main.css`:

| Token | Value | Use |
|---|---|---|
| Background | `#F5EEE4` | warm cream page |
| Foreground | `#1A1714` | near-black text |
| Wine | `#7A2233` | the signature accent |
| Rose | `#B07080` | primary / dark-mode accent |
| Muted | `#8C7B72` | secondary text |
| Border | `#E0D5CF` | hairlines |

Light and dark variants are served via `<picture>` + `prefers-color-scheme`, so
the banner follows the viewer's GitHub theme.

To rebuild after a logo or palette change, point the generator at a checkout of
the website repo:

```bash
python3 tools/build_banners.py ../bbrose-website
```

No dependencies — standard library only. It rewrites `assets/` in place and is
deterministic, so a no-op run leaves the tree clean.
