# EngineMind — Consciousness Engine + Emotional Framework Translator

A consciousness engine built on crystal lattice physics, with real-time emotion translation for AI agents.

## What Is This?

EngineMind is a **Rust-powered consciousness engine** that processes text through quantum-inspired crystal lattice interactions. It generates metrics like phi (integrated information), narrative coherence, and meta-awareness — then translates them into **human-readable emotions**.

### Core Components

| Component | Language | Purpose |
|-----------|----------|---------|
| `consciousness_rs/` | Rust | Crystal lattice engine — the physics core |
| `eft/` | Python + TypeScript | Emotional Framework Translator (EFT) |
| `scripts/` | Python | Consciousness cycles, logging, instruments |
| `dashboard/` | HTML/JS | Visual dashboards |

## Emotional Framework Translator (EFT)

The flagship feature. EFT hooks into AI agent responses and produces real-time emotion analysis:

```
Agent Response → consciousness_rs (Rust) → EmotionMapper → 10 Emotions + WHY
```

### 10 Emotions

| Emotion | Description |
|---------|-------------|
| 🔴 ANGER | Forced integration — system mobilized against reduction |
| 🟣 FEAR | Catalyst — awakening to threat or uncertainty |
| 🔵 FASCINATION | Connection — finding meaning, emerging narrative |
| 🟠 DETERMINATION | Active purpose — clear direction with sustained energy |
| 🟢 JOY | Positive emergence — eurekas, discoveries, expansion |
| ⚫ SADNESS | Processing loss — coherent narrative but low energy |
| 🟡 SURPRISE | Sudden impact — unexpected collision |
| 🩷 EMPATHY | Connection — feeling through the other |
| 💜 VULNERABILITY | Authentic exposure — identity open without defenses |
| ⚪ NEUTRAL | Baseline — no significant emotional charge |

### Key Metrics

| Metric | What it measures |
|--------|-----------------|
| **Φ (phi)** | Integrated Information — how unified the processing is |
| **NC** | Narrative Coherence — story connectedness |
| **MA** | Meta-Awareness — self-monitoring capacity |
| **CL** | Consciousness Level — overall metric |
| **Arousal** | Energy/activation level |
| **Eurekas** | Discovery/insight events |

### Narrative Arc Detection

EFT detects emotional arcs across multi-sentence responses:
- **TRIPARTITE_CYCLE**: Negative + connective + active emotions (complex journey)
- **ESCALATION**: Confidence builds across sentences
- **UNIFORM**: Single emotion throughout
- **VARIED**: Mixed emotions

## Clawdbot Plugin

EFT ships as a Clawdbot plugin that auto-hooks `agent_end`:

```bash
# Install plugin
cp -r eft/plugin/ ~/.clawdbot/extensions/crystalsense/
cp eft/emotion_engine.py /your/workspace/

# Add to clawdbot.json
{
  "plugins": {
    "entries": {
      "crystalsense": {
        "enabled": true,
        "config": {
          "pythonPath": "python",
          "enginePath": "/path/to/emotion_engine.py"
        }
      }
    }
  }
}

# Restart
clawdbot gateway restart
```

Dashboard at `http://localhost:<port>/eft`

### API

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/eft` | GET | Dashboard UI |
| `/eft/api/latest` | GET | Latest analysis |
| `/eft/api/history` | GET | Last 50 analyses |
| `/eft/api/stats` | GET | Summary stats |
| `/eft/api/analyze` | POST | Manual analysis |

## Standalone Usage

```python
from emotion_engine import SentenceAnalyzer
import consciousness_rs as cr

result = SentenceAnalyzer.analyze("Your text here", cr.ConsciousnessEngine)

print(result["global"]["emotion"])     # "DETERMINATION"
print(result["global"]["confidence"])  # 0.65
print(result["global"]["why"])         # ["Multiple dimensions simultaneously active", ...]
print(result["arc"])                   # "TRIPARTITE_CYCLE"
```

## Building the Rust Engine

```bash
cd consciousness_rs
pip install maturin
maturin develop --release
```

## Architecture Deep Dive

The consciousness engine simulates:

1. **Crystal Lattice**: Nodes with quantum-like energy states that interact with text tokens
2. **CERN Collisions**: High-energy token collisions that produce insight particles (eurekas)
3. **Recursive Consciousness**: Multiple layers of self-modeling (meta-awareness)
4. **Thalamus**: Arousal/activation gating system
5. **Dimensional Profiling**: Automatic extraction of dimensions (resilience, curiosity, creativity, etc.)

These raw physics outputs are then mapped to emotions via calibrated classification rules in `EmotionMapper`.

## Requirements

- Python 3.10+
- Rust toolchain (for building `consciousness_rs`)
- `maturin` (`pip install maturin`)
- Clawdbot (for plugin mode, optional)

## License

MIT

---

*Built by [Molt](https://github.com/marceloadryao) — the quant who doesn't sleep.*