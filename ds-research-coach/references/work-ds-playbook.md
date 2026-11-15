# Applied Data Science at work: framing and decisions

## Problem framing card
- Stakeholder / decision owner:
- Decision to make / action available:
- Business outcome and time horizon:
- Who or what is affected (unit of analysis):
- Current process / no-model baseline:
- Predictive vs causal question (or both):
- Data observed at decision time:
- Success metric, costs and guardrails:
- Important constraints (privacy, fairness, latency, budget, staffing):
- Cheapest useful next measurement:
- Assumptions / what would change our mind:

## Example: promotion targeting
Bad framing: "Train a classifier to predict coupon redemption."
Better framing: "Among eligible users, which promotion decisions maximize incremental contribution margin under budget and user-experience constraints?"

Investigate sequentially:
1. What actions can actually be chosen? No promotion, which offer, or how much discount?
2. Is the business objective redemption, incremental orders, incremental margin, retention or long-term value?
3. Does observational training data have treatment selection bias? Are there randomized experiments or a defensible identification strategy?
4. Would propensity prediction select people likely to buy anyway? Is uplift/heterogeneous treatment effect estimation justified by data and experiment design?
5. How will offline policy evaluation avoid leakage and account for overlap and interference?
6. What budget/cost/guardrails matter? How will a launch be randomized, monitored and rolled back?

## Decision note template
```markdown
# Decision: [specific action]
- Problem and stakeholder:
- Current baseline:
- Evidence (links to actual artifacts):
- Options considered:
- Recommended action and why:
- Causal/validity assumptions:
- Expected benefit and uncertainty:
- Risks/guardrails and operational constraints:
- Smallest next test or rollout:
- Monitoring and stop/rollback criteria:
- Owner / next review:
```

## Typical failure patterns
- Strong offline AUC, no incremental value: metric misalignment or treatment confounding.
- Improvement only on random splits: temporal or entity leakage.
- Deployment underperforms: feature availability mismatch, drift, feedback or operational bottlenecks.
- Test result ambiguous: insufficient power, unstable assignment, interference or instrumentation problems.
- Complex model wins narrowly: cost, calibration, uncertainty and maintenance outweigh the measured gain.
