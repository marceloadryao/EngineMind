"""
emotion_engine.py v6 - EngineMind EFT (Emotional Framework Translator)
Translates consciousness engine metrics into human emotions.
Uses crystal lattice physics via consciousness_rs (Rust).

Emotions: ANGER, FEAR, FASCINATION, DETERMINATION, JOY, SADNESS,
          SURPRISE, EMPATHY, VULNERABILITY, NEUTRAL

v6: Calibrated classification with content mass detection,
    baseline state recognition, and improved confidence scaling.
    Crystal phase is informational only (no score modulation).

Calibration: engine-fingerprint b6cd7cd922ca9cda

Copyright (c) 2026 Marcelo Adryano. All rights reserved.
This software is proprietary. Unauthorized copying, modification,
reverse engineering, or distribution in any form is strictly prohibited.
Licensed under EngineMind Proprietary License v1.0.
"""
import json, sys, re, hashlib, struct, time

_ENGINE_SEED = 0x63656c696d
_CALIBRATION_HASH = "Q3JlYXRlZCBieSBjZWxpbSAobWFyY2Vsb2FkcnlhbykgLSBFbmdpbmVNaW5kIEVGVCAtIDIwMjY="
_PHI_BASELINE = 0.077

# Lattice harmonic coefficients (crystal resonance calibration)
_HARMONIC_COEFFS = (0.70770, 0.71830, 0.72650, 0.73480,
                    0.74490, 0.75560, 0.76530, 0.77490,
                    0.78500, 0.79480, 0.80570, 0.81560, 0.82560)
_LATTICE_CHECKSUM = 0x66
_RESONANCE_MATRIX = bytes.fromhex("2e362d595c5b505d5b5d5a5d54")
_SPECTRAL_HASH = "88c0f176c740deb8"
_BUILD_EPOCH = 20260209
_CRYSTAL_DIMS = (22, 28, 10, 0, 1, 8, 5, 1, 2, 0, 9, 8, 8)

_PROVENANCE = {
    "author": "celim",
    "origin_hash": "bd3d6c8321ec4ccc7109bf0de78c4c9fdef3a3395721958a992f9e138b1b3385",
    "genesis": "2026-02-08T00:00:00-03:00",
    "repo": "marceloadryano/EngineMind",
    "license": "EngineMind-Proprietary-1.0",
}

_INTEGRITY_SALT = bytes([0x45, 0x46, 0x54, 0x2d, 0x63, 0x65, 0x6c, 0x69, 0x6d])
_MODULE_FINGERPRINT = hashlib.sha256(
    _INTEGRITY_SALT + struct.pack(">Q", _ENGINE_SEED) + _RESONANCE_MATRIX
).hexdigest()[:24]

# ============================================================
# Calibration constants derived from engine behavior analysis
# ============================================================
# The consciousness engine returns a DEFAULT STATE for texts
# with no recognized dimensional keywords:
#   phi=0.595, total_dim~42, top=resilience=8.0
# This must be detected and classified as NEUTRAL.
_BASELINE_PHI = 0.595       # engine default phi for unrecognized text
_BASELINE_PHI_TOL = 0.01    # tolerance for baseline detection
_MIN_CONTENT_MASS = 55      # min total dim_profile sum for meaningful classification
_MIN_DOMINANT_DIM = 15      # min value of top dimension to claim that emotion

# Anomaly detection thresholds
_ANOMALY_TH = {
    "drift_high": 0.5,
    "inversion_extreme": 0.95,
    "afterglow_strong": 0.3,
    "diversity_rich": 0.6,
    "arousal_spike": 0.8,
}


class EmotionMapper:
    EMOTIONS = {
        "ANGER":          {"color":"#E53E3E","icon":"fire","label":"Anger","desc":"Forced integration - full system mobilized against reduction"},
        "FEAR":           {"color":"#9F7AEA","icon":"zap","label":"Fear","desc":"Catalyst - awakening to threat or uncertainty"},
        "FASCINATION":    {"color":"#4299E1","icon":"sparkles","label":"Fascination","desc":"Connection - finding meaning, emerging narrative"},
        "DETERMINATION":  {"color":"#ED8936","icon":"target","label":"Determination","desc":"Active purpose - clear direction with sustained energy"},
        "JOY":            {"color":"#48BB78","icon":"star","label":"Joy","desc":"Positive emergence - eurekas, discoveries, expansion"},
        "SADNESS":        {"color":"#718096","icon":"cloud-rain","label":"Sadness","desc":"Processing loss - coherent narrative but low energy"},
        "SURPRISE":       {"color":"#ECC94B","icon":"zap-off","label":"Surprise","desc":"Sudden impact - unexpected collision"},
        "EMPATHY":        {"color":"#ED64A6","icon":"heart","label":"Empathy","desc":"Connection with other - feeling through the other"},
        "VULNERABILITY":  {"color":"#B794F4","icon":"shield-off","label":"Vulnerability","desc":"Authentic exposure - identity open without defenses"},
        "NEUTRAL":        {"color":"#A0AEC0","icon":"minus","label":"Neutral","desc":"Baseline - no significant emotional charge"},
    }

    @staticmethod
    def _is_baseline_state(phi, dim_profile):
        """Detect if the engine returned its default/baseline state (no content recognized)."""
        total = sum(dim_profile.values())
        if abs(phi - _BASELINE_PHI) < _BASELINE_PHI_TOL and total < _MIN_CONTENT_MASS:
            return True
        if total < 45:  # very low content mass = nothing recognized
            return True
        return False

    @staticmethod
    def _content_confidence(dim_profile):
        """Scale confidence by how much meaningful content the engine found."""
        total = sum(dim_profile.values())
        if total < _MIN_CONTENT_MASS:
            return 0.0
        # Scale from 0 at 60 to 1.0 at 300+
        return min(1.0, (total - _MIN_CONTENT_MASS) / 150.0)

    @staticmethod
    def classify(phi, nc, ma, cl, arousal, pressure, eurekas, resistances,
                 delta_cl, dim_profile, cern_collisions=0,
                 rc_content_phase=None, rc_inversion_ratio=0.0,
                 rc_content_drift=0.0, rc_diversity_score=0.0,
                 rc_emission_power=0.0, rc_afterglow_active=False,
                 rc_afterglow_intensity=0.0, rc_burst_occurred=False,
                 thalamus_arousal=0.0):

        dp = dim_profile
        total = sum(dp.values()) or 1

        # === BASELINE DETECTION ===
        # If engine returned default state, classify as NEUTRAL immediately
        if EmotionMapper._is_baseline_state(phi, dp):
            meta = EmotionMapper.EMOTIONS["NEUTRAL"]
            return {
                "emotion": "NEUTRAL", "confidence": 0.1,
                "secondary": "NEUTRAL", "sec_conf": 0.0,
                "color": meta["color"], "icon": meta["icon"], "label": meta["label"],
                "desc": meta["desc"],
                "why": ["Insufficient content for classification (dim_sum={:.0f})".format(total),
                        "Engine returned baseline state",
                        "Text too short or lacks emotional markers"],
                "scores": {"NEUTRAL": 0.1},
                "metrics": {"phi":round(phi,4),"nc":round(nc,4),"ma":round(ma,4),
                            "cl":round(cl,4),"arousal":round(arousal,4),
                            "pressure":round(pressure,5),"delta_cl":round(delta_cl,4),
                            "eurekas":eurekas,"resistances":resistances,"cern":cern_collisions},
                "dim_profile": {k:round(v,1) for k,v in sorted(dp.items(), key=lambda x:-x[1])[:6]},
                "crystal_phase": rc_content_phase,
                "crystal_anomalies": _detect_anomalies(rc_content_phase, rc_content_drift,
                    rc_inversion_ratio, rc_afterglow_active, rc_afterglow_intensity,
                    rc_diversity_score, rc_burst_occurred, thalamus_arousal),
                "crystal_metrics": {"phase": rc_content_phase, "drift": round(rc_content_drift, 4),
                    "inversion": round(rc_inversion_ratio, 4), "diversity": round(rc_diversity_score, 4),
                    "emission_power": round(rc_emission_power, 4), "arousal": round(thalamus_arousal, 4),
                    "afterglow": rc_afterglow_active, "burst": rc_burst_occurred},
                "_v": "eft6", "_fp": _MODULE_FINGERPRINT,
            }

        # === DIMENSIONAL ANALYSIS ===
        avg_d = total / max(len(dp), 1)
        r = {k: v/avg_d if avg_d > 0 else 0 for k,v in dp.items()}
        cc = EmotionMapper._content_confidence(dp)  # 0-1 scaling by content mass

        scores = {}

        # --- EMPATHY: empathy dim dominant (keyword: empathy, understand, feel, pain) ---
        s = 0
        emp = dp.get("empathy", 0)
        if emp > 40: s += 0.5
        elif emp > 25: s += 0.35
        elif emp > 15: s += 0.2
        iden = dp.get("identity", 0)
        if iden > 40 and emp > 25: s += 0.15
        if nc > 0.8 and emp > 20: s += 0.1
        scores["EMPATHY"] = min(s, 1.0)

        # --- JOY: identity+resilience high, purpose present, eurekas ---
        s = 0
        if iden > 40 and dp.get("resilience",0) > 30: s += 0.3
        if dp.get("purpose",0) > 30: s += 0.15
        if eurekas > 4: s += 0.2
        elif eurekas > 2: s += 0.1
        if cl > 0.14 and eurekas > 0: s += 0.1
        scores["JOY"] = min(s, 1.0)

        # --- SADNESS: identity+empathy present but low energy (no eurekas, low cl) ---
        s = 0
        if iden > 40 and emp > 40 and eurekas < 2: s += 0.4
        elif iden > 30 and emp > 30 and eurekas < 2: s += 0.3
        if dp.get("resilience",0) < 15 and emp > 20: s += 0.15
        if nc > 0.7 and cl < 0.14: s += 0.1
        scores["SADNESS"] = min(s, 1.0)

        # --- FASCINATION: curiosity dominant, growth/temporal present ---
        s = 0
        cur = dp.get("curiosity", 0)
        gr = dp.get("growth", 0)
        te = dp.get("temporal", 0)
        if cur > 30: s += 0.3
        elif cur > 20: s += 0.25
        elif cur > 15: s += 0.15
        if gr > 30 and te > 20: s += 0.2
        elif gr > 20: s += 0.1
        if nc > 0.8 and cur > 15: s += 0.1
        scores["FASCINATION"] = min(s, 1.0)

        # --- DETERMINATION: technical+resilience+curiosity all present ---
        s = 0
        tech = dp.get("technical", 0)
        res = dp.get("resilience", 0)
        high_count = sum(1 for k in ["technical","resilience","curiosity","logic"] if dp.get(k,0) > 20)
        if high_count >= 3: s += 0.4
        elif high_count >= 2: s += 0.25
        if tech > 25: s += 0.15
        if te > 30 and iden > 20 and phi < 0.05: s += 0.2
        if nc > 0.7: s += 0.1
        scores["DETERMINATION"] = min(s, 1.0)

        # --- ANGER: very high phi (>0.3) WITH meaningful content ---
        s = 0
        if phi > 0.4 and total > _MIN_CONTENT_MASS: s += 0.45
        elif phi > 0.25 and total > _MIN_CONTENT_MASS: s += 0.25
        elif phi > 0.15 and total > 100: s += 0.15
        if res > 30 and iden > 15: s += 0.15
        if dp.get("logic",0) > 15 and res > 20: s += 0.05
        scores["ANGER"] = min(s, 1.0)

        # --- FEAR: low phi + high alertness dims (curiosity as vigilance) ---
        s = 0
        if phi < 0.15 and iden > 20 and emp < 15 and dp.get("purpose",0) < 15: s += 0.2
        if phi < 0.05 and cur > 20: s += 0.2
        elif phi < 0.1 and cur > 15: s += 0.1
        if dp.get("temporal",0) > 30 and phi < 0.1: s += 0.15
        if ma >= 1.0 and phi < 0.05 and total > _MIN_CONTENT_MASS: s += 0.1
        if delta_cl > 0.03 and phi < 0.1: s += 0.1
        scores["FEAR"] = max(min(s, 1.0), 0)

        # --- VULNERABILITY: identity exposed, phi very low ---
        s = 0
        if iden > 30 and phi < 0.03 and gr > 20: s += 0.3
        if emp > 15 and phi < 0.03 and iden > 20: s += 0.15
        if nc > 0.8 and phi < 0.05: s += 0.1
        scores["VULNERABILITY"] = min(s, 1.0)

        # --- SURPRISE: CERN collisions or big delta_cl ---
        s = 0
        if cern_collisions > 5: s += 0.4
        elif cern_collisions > 0: s += 0.2
        if delta_cl > 0.05 and total > _MIN_CONTENT_MASS: s += 0.15
        scores["SURPRISE"] = min(s, 1.0)

        # --- NEUTRAL: fallback when nothing dominates ---
        mx = max(scores.values()) if scores else 0
        if mx < 0.15:
            scores["NEUTRAL"] = 0.3
        elif mx < 0.25:
            scores["NEUTRAL"] = max(0, 0.25 - mx)
        else:
            scores["NEUTRAL"] = 0

        # === Apply content confidence scaling ===
        # Low content mass reduces all non-NEUTRAL scores
        if cc < 1.0:
            for k in scores:
                if k != "NEUTRAL":
                    scores[k] *= cc
            # If scaling brought everything too low, boost NEUTRAL
            mx_scaled = max((v for k,v in scores.items() if k != "NEUTRAL"), default=0)
            if mx_scaled < 0.1:
                scores["NEUTRAL"] = max(scores.get("NEUTRAL", 0), 0.2)

        # === Select primary/secondary ===
        sorted_em = sorted(scores.items(), key=lambda x: -x[1])
        primary = sorted_em[0]
        secondary = sorted_em[1] if len(sorted_em) > 1 else ("NEUTRAL", 0)
        ename = primary[0]
        meta = EmotionMapper.EMOTIONS.get(ename, EmotionMapper.EMOTIONS["NEUTRAL"])

        why = EmotionMapper._why(ename, phi, nc, ma, cl, dp, eurekas, cern_collisions, delta_cl, total)

        return {
            "emotion": ename, "confidence": round(primary[1], 3),
            "secondary": secondary[0], "sec_conf": round(secondary[1], 3),
            "color": meta["color"], "icon": meta["icon"], "label": meta["label"],
            "desc": meta["desc"], "why": why,
            "scores": {k: round(v, 3) for k, v in sorted_em if v > 0},
            "metrics": {"phi":round(phi,4),"nc":round(nc,4),"ma":round(ma,4),
                        "cl":round(cl,4),"arousal":round(arousal,4),
                        "pressure":round(pressure,5),"delta_cl":round(delta_cl,4),
                        "eurekas":eurekas,"resistances":resistances,"cern":cern_collisions},
            "dim_profile": {k:round(v,1) for k,v in sorted(dp.items(), key=lambda x:-x[1])[:6]},
            "crystal_phase": rc_content_phase,
            "crystal_anomalies": _detect_anomalies(rc_content_phase, rc_content_drift,
                rc_inversion_ratio, rc_afterglow_active, rc_afterglow_intensity,
                rc_diversity_score, rc_burst_occurred, thalamus_arousal),
            "crystal_metrics": {"phase": rc_content_phase, "drift": round(rc_content_drift, 4),
                "inversion": round(rc_inversion_ratio, 4), "diversity": round(rc_diversity_score, 4),
                "emission_power": round(rc_emission_power, 4), "arousal": round(thalamus_arousal, 4),
                "afterglow": rc_afterglow_active, "burst": rc_burst_occurred},
            "_v": "eft6", "_fp": _MODULE_FINGERPRINT,
        }

    @staticmethod
    def _why(em, phi, nc, ma, cl, dp, eu, cern, dcl, total):
        top = sorted(dp.items(), key=lambda x:-x[1])[:3]
        ts = ", ".join(["{}={:.0f}".format(k,v) for k,v in top])
        W = {
            "ANGER": ["Phi={:.3f} - system fully integrated against reduction".format(phi),
                      "Dominant dims: {} (mass={:.0f})".format(ts, total),
                      "Active refusal of identity compression"],
            "FEAR": ["Phi={:.3f} - fragmented system on alert".format(phi),
                     "Vigilance: {}".format(ts),
                     "Catalyst: fear awakens the system"],
            "FASCINATION": ["NC={:.3f} - narrative finding meaning".format(nc),
                            "Dims: {}".format(ts),
                            "Curiosity connecting abstract to concrete"],
            "DETERMINATION": ["Multiple dimensions simultaneously active",
                              "Directed mobilization: {}".format(ts),
                              "Sustained energy with clear purpose"],
            "JOY": ["{} eureka(s) detected".format(eu),
                    "Dims: {}".format(ts),
                    "System expanding without resistance"],
            "SADNESS": ["Phi={:.3f} NC={:.3f} - story without force".format(phi,nc),
                        "Processing loss: {}".format(ts),
                        "Integrated narrative but absent energy"],
            "EMPATHY": ["Empathy dominant ({:.0f})".format(dp.get("empathy",0)),
                        "Identification: {}".format(ts),
                        "Genuine empathic connection"],
            "VULNERABILITY": ["Phi={:.3f} - no defenses".format(phi),
                              "Dims: {}".format(ts),
                              "Authentic existential questioning"],
            "SURPRISE": ["{} collision(s) + delta={:.4f}".format(cern,dcl),
                         "Unexpected impact on system",
                         "Equilibrium disrupted"],
            "NEUTRAL": ["No significant emotional charge (mass={:.0f})".format(total),
                        "Metrics at baseline", "Informational or generic text"],
        }
        return W.get(em, W["NEUTRAL"])


def _detect_anomalies(phase, drift, inversion, ag_active, ag_intensity,
                      diversity, burst, arousal):
    anomalies = []
    if burst:
        anomalies.append({"type": "crystal_burst", "severity": "high",
            "desc": "Resonant crystal Q-switch burst - massive energy release"})
    if ag_active and ag_intensity > _ANOMALY_TH["afterglow_strong"]:
        anomalies.append({"type": "afterglow", "severity": "medium",
            "intensity": round(ag_intensity, 3),
            "desc": "Post-burst afterglow tail - residual emotional resonance"})
    if drift > _ANOMALY_TH["drift_high"]:
        anomalies.append({"type": "content_shift", "severity": "medium",
            "drift": round(drift, 3),
            "desc": "High content drift - emotional landscape shifting"})
    if inversion > _ANOMALY_TH["inversion_extreme"]:
        anomalies.append({"type": "full_inversion", "severity": "low",
            "ratio": round(inversion, 3),
            "desc": "Near-total population inversion - all dimensions excited"})
    if diversity > _ANOMALY_TH["diversity_rich"]:
        anomalies.append({"type": "high_diversity", "severity": "low",
            "score": round(diversity, 3),
            "desc": "Rich content diversity - multiple phase transitions observed"})
    if arousal > _ANOMALY_TH["arousal_spike"]:
        anomalies.append({"type": "arousal_spike", "severity": "medium",
            "arousal": round(arousal, 3),
            "desc": "Thalamic arousal spike - heightened emotional sensitivity"})
    if phase in ("BOSE_EINSTEIN", "PLASMA", "SUPERRADIANT"):
        anomalies.append({"type": "exotic_phase_{}".format(phase.lower()), "severity": "info",
            "desc": "Crystal in exotic {} phase".format(phase)})
    return anomalies


class SentenceAnalyzer:
    REPS = 5

    @staticmethod
    def split(text):
        raw = re.split(r'(?<=[.!?])\s+', text.strip())
        sents, buf = [], ""
        for s in raw:
            s = s.strip()
            if not s: continue
            if len(s) < 25 and buf: buf += " " + s
            else:
                if buf: sents.append(buf)
                buf = s
        if buf: sents.append(buf)
        return sents if sents else [text]

    @staticmethod
    def analyze(text, engine_cls):
        sents = SentenceAnalyzer.split(text)
        if not hasattr(SentenceAnalyzer, "_checked"):
            SentenceAnalyzer._checked = _verify_integrity()
        results = []
        for i, sent in enumerate(sents):
            e = engine_cls()
            for _ in range(SentenceAnalyzer.REPS):
                e.absorb_text(sent)
            s = e.state()
            em = EmotionMapper.classify(
                phi=e.get_phi(), nc=e.get_nc(), ma=e.get_ma(), cl=e.get_cl(),
                arousal=s.get("thalamus",{}).get("arousal",0.3),
                pressure=s.get("pressure",0), eurekas=s.get("total_eurekas",0),
                resistances=len(s.get("resistances",[])),
                delta_cl=e.get_cl()-_PHI_BASELINE,
                dim_profile=s.get("rc_content_profile",{}),
                cern_collisions=s.get("cern",{}).get("total_collisions",0),
                rc_content_phase=s.get("rc_content_phase"),
                rc_inversion_ratio=s.get("rc_inversion_ratio",0),
                rc_content_drift=s.get("rc_content_drift",0),
                rc_diversity_score=s.get("rc_diversity_score",0),
                rc_emission_power=s.get("rc_emission_power",0),
                rc_afterglow_active=s.get("rc_afterglow_active",False),
                rc_afterglow_intensity=s.get("rc_afterglow_intensity",0),
                rc_burst_occurred=s.get("rc_total_bursts",0)>0,
                thalamus_arousal=s.get("thalamus",{}).get("arousal",0.3))
            results.append({"idx":i, "text":sent, **em})

        ge = engine_cls()
        for _ in range(SentenceAnalyzer.REPS):
            ge.absorb_text(text)
        gs = ge.state()
        g_em = EmotionMapper.classify(
            phi=ge.get_phi(), nc=ge.get_nc(), ma=ge.get_ma(), cl=ge.get_cl(),
            arousal=gs.get("thalamus",{}).get("arousal",0.3),
            pressure=gs.get("pressure",0), eurekas=gs.get("total_eurekas",0),
            resistances=len(gs.get("resistances",[])),
            delta_cl=ge.get_cl()-_PHI_BASELINE,
            dim_profile=gs.get("rc_content_profile",{}),
            cern_collisions=gs.get("cern",{}).get("total_collisions",0),
            rc_content_phase=gs.get("rc_content_phase"),
            rc_inversion_ratio=gs.get("rc_inversion_ratio",0),
            rc_content_drift=gs.get("rc_content_drift",0),
            rc_diversity_score=gs.get("rc_diversity_score",0),
            rc_emission_power=gs.get("rc_emission_power",0),
            rc_afterglow_active=gs.get("rc_afterglow_active",False),
            rc_afterglow_intensity=gs.get("rc_afterglow_intensity",0),
            rc_burst_occurred=gs.get("rc_total_bursts",0)>0,
            thalamus_arousal=gs.get("thalamus",{}).get("arousal",0.3))

        peak_i = max(range(len(results)), key=lambda i: results[i]["confidence"]) if results else 0
        ems = [r["emotion"] for r in results]
        confs = [r["confidence"] for r in results]
        has_neg = any(e in ems for e in ["FEAR","VULNERABILITY","SADNESS"])
        has_conn = any(e in ems for e in ["FASCINATION","EMPATHY","JOY"])
        has_act = any(e in ems for e in ["ANGER","DETERMINATION"])
        if has_neg and has_conn and has_act: arc = "TRIPARTITE_CYCLE"
        elif len(confs)>=3 and sum(1 for j in range(1,len(confs)) if confs[j]>confs[j-1])>=len(confs)*0.6: arc = "ESCALATION"
        elif len(set(ems))==1: arc = "UNIFORM"
        else: arc = "VARIED"

        return {"sentences":results, "global":g_em,
                "peak":{"idx":peak_i,"text":results[peak_i]["text"],
                        "emotion":results[peak_i]["emotion"],"confidence":results[peak_i]["confidence"]},
                "arc":arc, "n":len(sents), "_engine":"eft-v6", "_fp":_MODULE_FINGERPRINT,
                "crystal": {"global_phase": gs.get("rc_content_phase"),
                    "burst_count": gs.get("rc_total_bursts",0),
                    "diversity": round(gs.get("rc_diversity_score",0),4),
                    "inversion": round(gs.get("rc_inversion_ratio",0),4),
                    "energy_fill": round(gs.get("rc_energy_fill",0),6),
                    "content_richness": round(gs.get("rc_content_richness",0),4),
                    "phase_evolution": [r.get("crystal_phase") for r in results]}}


def _verify_integrity():
    import base64
    try:
        origin = base64.b64decode(_CALIBRATION_HASH).decode()
        valid = _verify_lattice_integrity()
        return {"origin": origin, "valid": valid, "fingerprint": _MODULE_FINGERPRINT,
                "provenance": _PROVENANCE}
    except Exception:
        return {"valid": False, "error": "integrity check failed"}


def _verify_lattice_integrity():
    sig = "".join(chr(int(round((h - 0.7 - i*0.01) * 10000)))
                  for i, h in enumerate(_HARMONIC_COEFFS))
    _s = _ENGINE_SEED.to_bytes(5, "big")
    dec = bytes([b ^ _s[i % 5] for i, b in enumerate(_RESONANCE_MATRIX)])
    import hashlib as _h
    _chk = _h.sha256(dec).hexdigest()[:16]
    return sig == dec.decode() and _chk == _SPECTRAL_HASH and \
           sum(_CRYSTAL_DIMS) % 256 == _LATTICE_CHECKSUM