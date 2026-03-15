"""
AI Explanation Engine
====================
Generates human-readable explanations for IP / Domain risk
Used in SOC / SIEM dashboard:
"Why this IP is risky"
"""

import os
from datetime import datetime

# ================= SAFE OPENAI IMPORT =================
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


# ================= RULE-BASED EXPLANATION =================
def rule_based_explanation(target, threat_level, vt, abuse, ports):
    reasons = []

    if threat_level == "High Risk" or threat_level == "Critical Risk":
        reasons.append("The target shows strong indicators of malicious behavior.")

    vt_score = vt.get("malicious", 0) if isinstance(vt, dict) else vt
    if vt_score > 0:
        reasons.append(f"VirusTotal detected {vt_score} malicious reports.")

    ab_score = abuse.get("score", 0) if isinstance(abuse, dict) else abuse
    if ab_score > 50:
        reasons.append(
            f"AbuseIPDB score is high ({ab_score}), indicating repeated abuse."
        )

    if ports:
        reasons.append(
            f"Exposed services detected on ports: {', '.join(map(str, ports))}."
        )
    else:
        reasons.append("No open network services were detected.")

    reasons.append(
        "This assessment is based on open-source intelligence and heuristic scoring."
    )

    return " ".join(reasons)


# ================= AI-POWERED EXPLANATION =================
def ai_explanation(target, threat_level, vt, abuse, ports, god_mode=None):

    # ---- fallback if AI not available ----
    if not OPENAI_AVAILABLE or not os.getenv("OPENAI_API_KEY"):
        return rule_based_explanation(target, threat_level, vt, abuse, ports)

    prompt = f"""
You are a Senior Security Operations Center (SOC) Analyst and Incident Responder.

Your task is to analyze the following threat intelligence for a target IP or domain and generate a highly concise "Mitigation Playbook".

Target: {target}
Threat Level: {threat_level}
VirusTotal detections: {vt.get("malicious", 0) if isinstance(vt, dict) else vt}
AbuseIPDB score: {abuse.get("score", 0) if isinstance(abuse, dict) else abuse}
Open Ports: {ports if ports else "None"}
God-Mode Intel: {god_mode if god_mode else "None"}

Please output your response exactly in this format:
1. Executive Summary: 1-2 sentences explaining why this IP is risky based on the data.
2. Mitigation Playbook: Provide exact, copy-pasteable terminal commands (e.g., iptables, ufw, or aws CLI) to block this threat. Wrap the commands in a markdown code block (```bash).

Do not include any other conversational fluff.
"""

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=400
        )

        message = response.choices[0].message.content

        if not message:
            raise ValueError("Empty AI response")

        return message.strip()

    except Exception as e:
        # Safe fallback
        return rule_based_explanation(target, threat_level, vt, abuse, ports)


# ================= SOC SUMMARY =================
def soc_summary(target, threat_level):
    return {
        "target": target,
        "threat_level": threat_level,
        "generated_at": datetime.utcnow().isoformat()
    }
