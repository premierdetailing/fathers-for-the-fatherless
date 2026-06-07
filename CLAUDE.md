# Fathers For The Fatherless — Claude Code Instructions

## Project
Static HTML/CSS/JS site. No build system. Edit files directly.

## Live URL
https://fathers-for-the-fatherless.vercel.app

## Deploy After Every Round of Fixes
This repo is connected to Vercel. Pushing the `main` branch auto-deploys to
production in ~20 seconds. After completing all requested changes, ALWAYS publish
from the repo root:
```
git add -A && git commit -m "<short summary of the change>" && git push
```
Do not ask — just commit and push. Deployment is automatic. Confirm the live URL
is updated before reporting back.

## File Structure
- index.html — main page; about/mission/give/updates/contact + topic pages are sibling .html files
- css/styles.css — global styles
- css/fftf-pages.css — interior page styles
- js/fftf.js — scripts
- images/ — assets

## Collaboration
Source of truth is GitHub: premierdetailing/fathers-for-the-fatherless (private).
Multiple people edit this repo. Always `git pull` before starting a round of
changes so you are working on the latest version.
