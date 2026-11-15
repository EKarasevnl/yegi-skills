# Experiment playbook

## Turning weak ideas into research questions
Weak: "Try bigger GRU / add CatBoost / ensemble more."
Strong: "Error rises with horizon only in high-volatility sequences; is state estimation drifting, or is the target signal itself less predictable?"

Ask:
1. What empirical pattern are we explaining?
2. What mechanism could cause it?
3. What *different* observable behavior would another mechanism predict?
4. Which cheap diagnostic could distinguish them without a retrain?
5. What controlled change could isolate the mechanism?

## Idea ranking rubric
For user-requested brainstorming, score each candidate qualitatively (high/medium/low):
- **Evidence:** supported by existing observations?
- **Information gain:** would either outcome teach us something?
- **Expected upside:** reasonable path to better held-out performance?
- **Cost:** engineering/compute/inference?
- **Confounding risk:** can it be evaluated cleanly?

Lead with the most informative cheap investigation, not the fanciest architecture. Include both an optimistic prediction and what would falsify it.

## Experiment card
```markdown
### [date] [short name]
- Observation (link to run/artifact):
- Hypotheses (and alternative):
- Prediction before run:
- Controlled variable / invariant baseline:
- Split and metric / diagnostic slices:
- Cheap preflight check:
- Cost ceiling:
- Result with uncertainty:
- Interpretation / competing explanations:
- Decision and next experiment:
```

## Example: additive fraud model and weak stacking gains
Observation: GAM/GLM-boost competes with more flexible classifiers, while OOF stacking barely moves AUC. These observations alone do **not** prove the target is additive.

Hypotheses:
- H1: Most discriminative structure is captured by main effects.
- H2: Interactions help but are not learned or validated reliably.
- H3: Models differ in probability estimates but not in discriminative rankings/errors.

Cheap diagnostics:
- Compare paired OOF predictions: rank correlation, disagreement, errors by subgroup, paired AUC difference by fold/bootstrap appropriate to split.
- Measure additive model residuals by plausible feature intersections using out-of-fold predictions, avoiding post-hoc slice overfitting.
- Add just a few pre-specified pairwise interactions under the same folds, then assess stability.

Interpretation: weak stacking benefit alone cannot distinguish H1/H2/H3; first determine whether the predictors have complementary errors.

## Example: forecasting errors increase at later horizons
Potential causes: recursive error propagation, less informative inputs farther into future, nonstationarity, horizon-specific label noise.
Discriminator: compare direct-vs-recursive forecasts if relevant, errors against horizon and regime, residual autocorrelation, and oracle/teacher-forced inputs where valid.
Avoid simply increasing late-horizon loss weights without knowing whether error is reducible.

## Example: trading strategy seems profitable in a simulator
Competing possibilities: real alpha, optimistic fills, lookahead, regime-specific luck, omitted spread/fees or adverse selection.
First audit event timestamps and execution assumptions, then compare net PnL by regime, inventory exposure and max drawdown under plausible fees/slippage.
