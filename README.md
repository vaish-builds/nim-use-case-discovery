# 🔍 NIM Use Case Discovery Engine

> An enterprise AI adoption tool that uses NVIDIA NIM to identify and prioritize the highest-impact AI use cases for any organization — and generates a C-suite ready implementation roadmap in under 60 seconds.

**Built by Vaishnavi Awasthi** · MEM @ Duke University · [LinkedIn](https://linkedin.com/in/yourhandle)

---

## The Problem This Solves

Every enterprise wants to adopt AI. Most don't know where to start.

When an IT director or Chief Digital Officer walks into a strategy meeting, they face three questions they can't easily answer:
1. Which of our workflows would benefit most from AI?
2. Which should we tackle first given our budget and timeline?
3. How do we explain the ROI to our CFO?

NVIDIA NIM has the model quality to answer these questions — but no tool existed to turn that capability into an enterprise adoption roadmap. This tool builds that bridge.

---

## What It Does

Enter your organization's context — industry, size, technical maturity, top challenges, budget, and timeline. NVIDIA NIM analyzes your inputs and generates:

- **5 prioritized AI use cases** tailored to your specific enterprise context
- **Business impact score** (1–10) for each use case
- **Implementation effort** rating (Low / Medium / High)
- **Time to value** (Quick Win / Short Term / Medium Term)
- **KPI improvement estimate** with specific metric (e.g. "30% ↑ Claims Processing Time")
- **NIM model recommendation** — which model (Llama 3.1 70B, Mistral 7B, or Phi-3 Mini) is best suited and why
- **Executive summary** ready to share with C-suite leadership
- **Downloadable report** for stakeholder presentations

---

## Sample Output (Insurance Industry)

![Discovery Process](screenshot-process.png)
![Results Page](screenshot-result.png)

| # | Use Case | Impact | Effort | Timeline | KPI |
|---|---|---|---|---|---|
| 1 | Automated Claims Processing with Document Analysis | 8/10 | Medium | Quick Win (0–3 mo) | 30% ↑ Claims Processing Time |
| 2 | Predictive Risk Assessment for Cybersecurity Threats | 9/10 | High | Short Term (3–6 mo) | 25% ↓ Successful Attacks |
| 3 | Personalized Customer Service Chatbots | 7/10 | Low | Quick Win (0–3 mo) | 20% ↑ Customer Satisfaction |
| 4 | Automated Policy Underwriting with Predictive Analytics | 8/10 | Medium | Short Term (3–6 mo) | 25% ↑ Policy Issuance Time |
| 5 | Employee Productivity Enhancement with Task Automation | 6/10 | Low | Quick Win (0–3 mo) | 15% ↑ Employee Productivity |

**Average impact score: 7.6/10 · 3 quick wins identified · Model: meta/llama-3.1-70b-instruct**

---

## Why I Built This

While working on my NIM Enterprise Readiness Scorecard (see: [nim-enterprise-readiness-scorecard](https://github.com/vaish-builds/nim-enterprise-readiness-scorecard)), I noticed a gap:

NIM is powerful — but enterprise adoption is blocked not just by technical readiness, but by a lack of clarity on *where* to apply AI in the first place. Sales teams, solution architects, and TPMs spend hours in discovery workshops helping enterprises figure out their highest-impact use cases. This tool automates that process.

It's also a demonstration of NIM's own capabilities — the tool uses NIM to sell NIM adoption. That's the kind of novel use case the Enterprise Product Group exists to develop.

---

## How It Works

```
User inputs enterprise context
(industry, size, maturity, challenges, budget, timeline)
        ↓
Tool sends structured prompt to NVIDIA NIM
(integrate.api.nvidia.com/v1)
        ↓
NIM generates 5 tailored use cases as structured JSON
        ↓
App parses and renders use cases with impact scores,
KPI estimates, effort ratings, and model recommendations
        ↓
Executive summary generated and formatted
for leadership presentation
        ↓
Full report downloadable as .txt
```

---

## Industries Supported

Financial Services, Healthcare & Life Sciences, Retail & E-commerce, Manufacturing & Supply Chain, Government & Defense, Energy & Utilities, Telecommunications, Media & Entertainment, Education & Research, Insurance

---

## NIM Models Used

| Model | Best For |
|---|---|
| meta/llama-3.1-70b-instruct | Complex reasoning, multi-step analysis, detailed use case generation |
| mistralai/mistral-7b-instruct-v0.3 | Fast response, cost-sensitive deployments |
| microsoft/phi-3-mini-128k-instruct | Lightweight tasks, quick wins, high-volume inference |

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| API | NVIDIA NIM — `integrate.api.nvidia.com/v1` |
| Output format | Structured JSON parsed from NIM response |
| Language | Python 3.11+ |
| Key libraries | openai, streamlit, json |

---

## Setup & Run

```bash
# 1. Clone the repo
git clone https://github.com/vaish-builds/nim-use-case-discovery
cd nim-use-case-discovery

# 2. Install dependencies
pip install openai streamlit

# 3. Run
streamlit run app.py
```

Get your free NVIDIA NIM API key at [build.nvidia.com](https://build.nvidia.com). No credit card required.

---

## Related Project

**NIM Enterprise Readiness Scorecard** — a live API audit tool that evaluates NVIDIA NIM against 5 enterprise procurement dimensions and surfaces product gaps with PM recommendations.

→ [github.com/vaish-builds/nim-enterprise-readiness-scorecard](https://github.com/vaish-builds/nim-enterprise-readiness-scorecard)

Together, these two tools represent a full enterprise AI adoption lifecycle:
- **Scorecard** = Is NIM ready for enterprise? (infrastructure audit)
- **Discovery Engine** = Where should my enterprise use NIM? (adoption strategy)

---

*Built by Vaishnavi Awasthi · MEM @ Duke University · April 2026*
