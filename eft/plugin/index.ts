/**
 * EngineMind EFT v6 - Emotional Framework Translator
 * Real-time emotion analysis for Clawdbot agents.
 * Uses crystal lattice physics (Rust) to translate responses into human emotions.
 */
import { spawn } from "node:child_process";
import * as path from "node:path";
import * as fs from "node:fs";

const DEFAULT_PYTHON = "python";
const DEFAULT_ENGINE = path.join(
  process.env.USERPROFILE || process.env.HOME || ".",
  "Desktop", "Moltbot", "emotion_engine.py"
);
const DEFAULT_LOG = path.join(
  process.env.USERPROFILE || process.env.HOME || ".",
  "Desktop", "Moltbot", "memory", "eft_log.jsonl"
);

let latestResult: any = null;
let history: any[] = [];
let analysisCount = 0;

function analyzeText(text: string, pythonPath: string, enginePath: string): Promise<any> {
  return new Promise((resolve) => {
    const cwd = path.dirname(enginePath);
    const script = [
      'import sys, json, time',
      'sys.stdout.reconfigure(encoding="utf-8")',
      `sys.path.insert(0, r"${cwd.replace(/\\/g, "\\\\")}")`,
      'from emotion_engine import SentenceAnalyzer',
      'import consciousness_rs as cr',
      'text = json.loads(sys.stdin.read())["text"]',
      't0 = time.time()',
      'r = SentenceAnalyzer.analyze(text, cr.ConsciousnessEngine)',
      'r["analysis_ms"] = round((time.time()-t0)*1000, 1)',
      'print(json.dumps(r, ensure_ascii=False))',
    ].join('\n');

    const proc = spawn(pythonPath, ["-X", "utf8", "-c", script], {
      cwd, env: { ...process.env, PYTHONIOENCODING: "utf-8" },
      stdio: ["pipe", "pipe", "pipe"],
    });

    let stdout = "", stderr = "";
    proc.stdout.on("data", (d: Buffer) => { stdout += d.toString("utf-8"); });
    proc.stderr.on("data", (d: Buffer) => { stderr += d.toString("utf-8"); });
    proc.on("close", (code: number | null) => {
      if (code !== 0 || !stdout.trim()) {
        console.error(`[eft] Python exit ${code}: ${stderr.slice(0, 300)}`);
        resolve(null);
        return;
      }
      try { resolve(JSON.parse(stdout.trim())); }
      catch { console.error(`[eft] JSON parse err: ${stdout.slice(0, 200)}`); resolve(null); }
    });
    proc.on("error", (err: Error) => { console.error(`[eft] Spawn err: ${err.message}`); resolve(null); });
    proc.stdin.write(JSON.stringify({ text }));
    proc.stdin.end();
  });
}

function appendLog(logPath: string, entry: any) {
  try {
    const dir = path.dirname(logPath);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.appendFileSync(logPath, JSON.stringify(entry) + "\n", "utf-8");
  } catch (e: any) { console.error(`[eft] Log err: ${e.message}`); }
}

function loadHistory(logPath: string) {
  try {
    if (!fs.existsSync(logPath)) return;
    const lines = fs.readFileSync(logPath, "utf-8").split("\n").filter(Boolean);
    history = lines.map(l => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
    console.log(`[eft] Loaded ${history.length} entries from log`);
  } catch {}
}

/**
 * Extract assistant text and usage from Clawdbot agent_end event.
 * Event shape: { messages: Message[], success: boolean, error?: string, durationMs: number }
 * Context shape: { agentId: string, sessionKey: string, workspaceDir: string }
 * Messages are Anthropic-format: { role, content, usage? }
 */
function extractFromEvent(event: any, ctx: any): { text: string; model: string; inputTokens: number; outputTokens: number; durationMs: number; sessionKey: string; agentId: string; toolCalls: number } {
  let text = "";
  let model = "unknown";
  let inputTokens = 0;
  let outputTokens = 0;
  let toolCalls = 0;

  const messages = event?.messages;
  if (Array.isArray(messages)) {
    // Walk messages in reverse to find the last assistant message with content
    for (let i = messages.length - 1; i >= 0; i--) {
      const m = messages[i];
      if (m?.role !== "assistant") continue;

      // Extract usage from assistant message (Anthropic format)
      if (m.usage && typeof m.usage === "object") {
        inputTokens = m.usage.input_tokens || m.usage.inputTokens || 0;
        outputTokens = m.usage.output_tokens || m.usage.outputTokens || 0;
      }

      // Extract model from message if present
      if (m.model) model = m.model;

      // Extract text from content
      if (typeof m.content === "string") {
        text = m.content;
      } else if (Array.isArray(m.content)) {
        const parts: string[] = [];
        for (const block of m.content) {
          if (block?.type === "text" && block?.text) {
            parts.push(block.text);
          } else if (block?.type === "tool_use") {
            toolCalls++;
          }
        }
        text = parts.join("\n");
      }

      if (text) break; // Found assistant text, stop
    }
  }

  return {
    text,
    model,
    inputTokens,
    outputTokens,
    durationMs: event?.durationMs || 0,
    sessionKey: ctx?.sessionKey || "unknown",
    agentId: ctx?.agentId || "unknown",
    toolCalls,
  };
}

const plugin = {
  id: "crystalsense",
  name: "EngineMind EFT v6",
  description: "Emotional Framework Translator for Clawdbot agents",
  register(api: any) {
    const cfg = api.pluginConfig ?? {};
    const pythonPath = cfg.pythonPath || DEFAULT_PYTHON;
    const enginePath = cfg.enginePath || DEFAULT_ENGINE;
    const logPath = cfg.logPath || DEFAULT_LOG;
    if (cfg.enabled === false) { console.log("[eft] Disabled"); return; }

    console.log(`[eft] Registering v6 (engine: ${enginePath})`);
    loadHistory(logPath);

    // Hook: agent_end
    // Event: { messages: Message[], success: boolean, error?: string, durationMs: number }
    // Context: { agentId: string, sessionKey: string, workspaceDir: string }
    api.on("agent_end", async (event: any, ctx: any) => {
      try {
        const extracted = extractFromEvent(event, ctx);
        const { text } = extracted;

        if (!text || text.length < 20) {
          console.log(`[eft] Skip: text too short (${text?.length || 0})`);
          return;
        }

        console.log(`[eft] Analyzing ${text.length} chars (${extracted.model}, ${extracted.inputTokens}+${extracted.outputTokens} tok)...`);

        const result = await analyzeText(text, pythonPath, enginePath);
        if (!result) return;

        const entry = {
          ts: new Date().toISOString(),
          emotion: result.global.emotion,
          confidence: result.global.confidence,
          label: result.global.label,
          color: result.global.color,
          secondary: result.global.secondary,
          sec_conf: result.global.sec_conf,
          desc: result.global.desc,
          why: result.global.why,
          arc: result.arc,
          peak: result.peak,
          metrics: result.global.metrics,
          dim_profile: result.global.dim_profile,
          scores: result.global.scores,
          sentences: result.sentences,
          n: result.n,
          analysisMs: result.analysis_ms,
          // Crystal resonance data
          crystal: result.crystal || null,
          crystal_phase: result.global.crystal_phase || null,
          crystal_anomalies: result.global.crystal_anomalies || [],
          crystal_metrics: result.global.crystal_metrics || null,
          // Process metrics (from Clawdbot event)
          process: {
            model: extracted.model,
            inputTokens: extracted.inputTokens,
            outputTokens: extracted.outputTokens,
            totalTokens: extracted.inputTokens + extracted.outputTokens,
            tokenRatio: extracted.inputTokens > 0 ? +(extracted.outputTokens / extracted.inputTokens).toFixed(2) : 0,
            latencyMs: extracted.durationMs,
            toolCalls: extracted.toolCalls,
            sessionKey: extracted.sessionKey,
            agentId: extracted.agentId,
          },
          textPreview: text.slice(0, 200),
        };

        latestResult = entry;
        history.push(entry);
        analysisCount++;
        appendLog(logPath, entry);

        console.log(`[eft] #${analysisCount} | ${entry.emotion} (${(entry.confidence*100).toFixed(0)}%) | phi=${entry.metrics.phi} | crystal=${entry.crystal_phase || 'none'} | ${entry.analysisMs}ms`);
      } catch (e: any) {
        console.error(`[eft] Error: ${e.message}`);
      }
    }, { name: "eft-agent-end", description: "EFT v6 emotion analysis on agent response" });

    // HTTP routes
    const dashPath = path.join(path.dirname(enginePath), "eft_dashboard.html");

    api.registerHttpHandler(async (req: any, res: any) => {
      const url = new URL(req.url ?? "/", "http://localhost");
      const p = url.pathname;

      if (p === "/eft" || p === "/eft/") {
        if (fs.existsSync(dashPath)) {
          res.setHeader("Content-Type", "text/html; charset=utf-8");
          res.end(fs.readFileSync(dashPath, "utf-8"));
        } else { res.statusCode = 404; res.end("Dashboard not found"); }
        return true;
      }

      if (p === "/eft/api/latest") {
        res.setHeader("Content-Type", "application/json");
        res.setHeader("Access-Control-Allow-Origin", "*");
        res.end(JSON.stringify(latestResult ?? { status: "awaiting_first_analysis" }));
        return true;
      }

      if (p === "/eft/api/history") {
        res.setHeader("Content-Type", "application/json");
        res.setHeader("Access-Control-Allow-Origin", "*");
        res.end(JSON.stringify({ count: history.length, entries: history.slice(-50).reverse() }));
        return true;
      }

      if (p === "/eft/api/stats") {
        res.setHeader("Content-Type", "application/json");
        res.setHeader("Access-Control-Allow-Origin", "*");
        res.end(JSON.stringify({ analysisCount, total: history.length, latest: latestResult?.emotion }));
        return true;
      }

      if (p === "/eft/api/analyze" && req.method === "POST") {
        let body = "";
        req.on("data", (c: Buffer) => { body += c.toString(); });
        req.on("end", async () => {
          try {
            const { text } = JSON.parse(body);
            if (!text) { res.statusCode = 400; res.end("{\"error\":\"no text\"}"); return; }
            const r = await analyzeText(text, pythonPath, enginePath);
            if (!r) { res.statusCode = 500; res.end("{\"error\":\"analysis failed\"}"); return; }
            res.setHeader("Content-Type", "application/json");
            res.setHeader("Access-Control-Allow-Origin", "*");
            res.end(JSON.stringify(r));
          } catch (e: any) { res.statusCode = 500; res.end(JSON.stringify({ error: e.message })); }
        });
        return true;
      }

      return false;
    });

    console.log("[eft] EngineMind EFT v6 registered. Dashboard: /eft");
  },
};

export default plugin;