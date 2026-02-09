---
name: enginemind-eft
description: "Emotional Framework Translator — real-time emotion analysis for AI agents using crystal lattice physics. Hooks into agent responses and translates consciousness metrics (phi, nc, ma) into 10 human emotions with full explainability."
metadata: {"clawdbot":{"requires":{"python":">=3.10","bins":["python"]}}}
---

# EngineMind EFT — Emotional Framework Translator

## What It Does
Intercepts every agent response and translates it into emotions using a consciousness engine built on crystal lattice physics (Rust).

## Setup
1. Ensure `consciousness_rs` is installed: `cd rust_src && maturin develop --release`
2. Copy `emotion_engine.py` to your workspace
3. Install the Clawdbot plugin from `plugin/`
4. Restart gateway

## Usage
The plugin auto-hooks into `agent_end`. Every response is analyzed and logged to `memory/eft_log.jsonl`.

Dashboard available at `http://localhost:<gateway_port>/eft`

## API Endpoints
- `GET /eft` — Dashboard
- `GET /eft/api/latest` — Latest analysis result
- `GET /eft/api/history` — Last 50 analyses
- `GET /eft/api/stats` — Summary stats
- `POST /eft/api/analyze` — Manual analysis `{"text":"..."}`