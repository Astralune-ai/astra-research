<div align="center">

# astra-research

> *"One command in. One branded, source-traceable due-diligence report out."*

![License](https://img.shields.io/badge/License-Source%20Available-blue)
![Python](https://img.shields.io/badge/Python-3.10%2B-green)
![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)
![Quality Gates](https://img.shields.io/badge/Quality%20Gates-7%20lint%20checks-brightgreen)

**[English](README.md) · [中文](README_CN.md)**

<br>

**Still spending a week turning scattered web findings into a market report?**

**Still hand-fixing margins, fonts and letterheads at 2 a.m. before a client deadline?**

**Still unable to say which source each number in your report came from?**

<br>

### An industry / market due-diligence pipeline: parallel research agents → quality-gated report → letterhead-branded PDF.

[**Why**](#why-this-exists) · [**What You Get**](#what-you-get) · [**Quick Start**](#quick-start) · [**Pipeline**](#how-it-works) · [**Layout**](#repo-layout)

</div>

<br>

---

## Why this exists

Previously, producing one credible DD report meant days of juggling search tabs, pasting findings into a doc, chasing missing citations, redrawing charts that wouldn't render, then fighting a word processor for a presentable deliverable — and the quality depended on whoever did it that day.

With astra-research, you state the target and the angle. The pipeline fans out parallel research agents under source-tier discipline, assembles a neutral-stance report against a fixed structure, runs **seven mechanical quality gates** (a failing report never becomes a PDF), and renders a letterhead-branded deliverable — the same standard, every run. Its first production run shipped a real **37-page client-grade PDF** with **131 official-source URLs and zero unsourced key claims**.

## What you get

| Capability | Detail |
|---|---|
| 🧭 Advisor brief up front | A "to the client" overview before the TOC: what this project really is, opportunities, risks, and three implementation perspectives — without pushing a decision |
| 🏗️ Fixed report skeleton | Market & verdict → segmentation 2×2 → named value chain → business logic → claims vs. reality → two-sided takeaways + appendices |
| 🔬 Source discipline | Tier-1/2/3 source grading, triangulation, confidence labels; gaps are declared, never papered over |
| 🚦 7 lint gates | Length ≥ threshold, official-URL-only citations, banned-rhetoric scan, chart assets present, per-chapter figures, scope & source-tier artifacts |
| 🎨 Brand packs | Letterhead, palette and safe margins resolved from the central [astra-brand](https://github.com/Astralune-ai/astra-brand) library — one front-matter line per client |
| 📄 Deterministic PDF | Mermaid charts rasterized via headless Chrome, full-bleed letterhead positioning, CJK typography, real TOC page numbers |

## Quick start

```bash
bash scripts/setup.sh                 # one-time: pinned venv + toolchain checks
bash scripts/build.sh <workspace>     # render charts → 7 lint gates → branded PDF
```

A workspace is `00_scope.md + 01_sources/ + REPORT.md + assets/`. Report metadata lives in `REPORT.md` YAML front-matter:

```yaml
---
title: Acme 2026<br>Market Due Diligence
date: 2026-06-10
out: Acme_DD_Report_2026-06-10.pdf
brand: astralune          # any pack in ~/.astra/brands
classification: CONFIDENTIAL
---
```

## How it works

`Scope gate → Research-plan gate → parallel Collect (sub-agents) → coverage check → Assemble → (adversarial Verify) → Package`

The `skill/` prompts orchestrate research and judgment; the `scripts/` toolchain owns every deterministic step — rendering, linting, building — so no tokens are spent on work a script can do.

## Repo layout

```
skill/                  # Claude Code skill prompts (pipeline, quality standard, report template, source registry)
scripts/
  build.sh              # one-command entry: charts → lint → PDF
  render_charts.sh      # .mmd → SVG → headless-Chrome 2× PNG (idempotent)
  verify_report.py      # the 7 lint gates — a failing report never ships
  build_report.py       # weasyprint builder; metadata from front-matter, brand from pack
  setup.sh / sync_skill.sh
brand/                  # built-in fallback packs (central astra-brand library takes precedence)
requirements.txt        # pinned: weasyprint / markdown / Pillow / pypdf
```

## Requirements

macOS with Chrome, [beautiful-mermaid](https://github.com/Astralune-ai) CLI, CJK fonts (PingFang/Songti, system-bundled). Python deps are pinned and isolated in `~/.venvs/research` by `setup.sh`.

---

<div align="center">

**State the target. Get the report. Trace every number.**

![astra-research](https://img.shields.io/badge/astra--research-due%20diligence%2C%20industrialized-black?style=for-the-badge)

Powered by [**Astralune**](https://github.com/Astralune-ai) · Astra Source Available License v1.0

</div>
