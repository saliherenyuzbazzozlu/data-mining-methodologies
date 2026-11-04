# Project design and AI review record

Prepared November 3, 2026. The reviewer here is the Codex assistant in this chat. These are genuine design and implementation reviews, not a claimed Claude or GPT-5 conversation. The assignment specifically names Claude/GPT-5; a separate export from one of those models is still required if the instructor interprets that literally. Human code review must be performed by the student and is not certified by this document.

## Initial design, version 1

| Project | Initial phase plan |
|---|---|
| CRISP-DM | Define retention objective; inspect Telco Kaggle data; encode features; compare logistic regression and random forest; evaluate accuracy; export a predictor. |
| SEMMA | Random sample wine data; explore chemistry; scale variables; compare ridge and forest regression; assess RMSE. |
| KDD | Select card usage fields; fill missing values; standardize; fit K-means; name clusters; report recommendations. |

## Expert critic persona used for both review rounds

“Adopt the perspective of a world-renowned speaker, authority, and award-winning author on the methodology under review. This is a role-play perspective, not a claim of actual credentials. Critique every phase and subtask. Identify leakage, missing evidence, unsupported causal claims, weak evaluation, reproducibility failures, and deployment gaps. Give concrete revisions and acceptance checks. Do not invent results or certify a human review.”

## Review round 1 — design critique and required revision

### CRISP-DM

- Business understanding: accuracy is not a retention objective. Specify a contact budget and rank-based lift target; document that saving a customer is causal and cannot be inferred from churn scores.
- Data understanding: `TotalCharges` is text and includes blanks. Record numeric conversion, missingness, identifier uniqueness, class balance, and training-only exploratory plots.
- Preparation: avoid identifier and protected-feature shortcuts; split before imputing/scaling/encoding. Preserve new-service customers rather than dropping blank charges.
- Modeling: use a prevalence baseline and training-only cross-validation. Compare regularization and leaf-size settings; save all candidate scores.
- Evaluation: freeze selection on validation data. Report AP, ROC AUC, Brier score, confusion matrix, precision/recall/lift at a 20% budget, bootstrap uncertainty, and subgroup diagnostics.
- Deployment: bundle the fitted pipeline and input schema; run batch scoring, serialization equivalence, unseen-category and invalid-input checks. Define pilot, monitoring, rollback and ownership.

### SEMMA

- Sample: wine has 240 exact duplicates; a random row split risks repeated chemistry across partitions. Deduplicate and group identical predictors for splits and CV.
- Explore: inspect target imbalance, distributions, skewness, and correlations using training data only; never interpret chemistry association as experimental evidence.
- Modify: fit imputation/scaling inside each fold; justify retaining unusual but valid chemistry and evaluate feature selection without test peeking.
- Model: add mean baseline, ridge and random forest with a small explicit grid; select using grouped CV and validation RMSE.
- Assess: report RMSE, MAE, R², within-one-point accuracy, prediction residuals, bootstrap intervals and error by observed quality; freeze model before test. State that the ordinal score is approximated as numerical.
- Delivery extension: create a batch scorer and clear laboratory-use limitations. SAS is optional in the brief; do not fabricate a SAS run.

### KDD

- Domain/selection: customer segments are descriptive, not creditworthiness labels. Exclude ID; no use for eligibility, limits, pricing or lending decisions.
- Preprocessing: record missing payments and credit limits. Split first; fit all imputation and transformations on discovery data only.
- Transformation: raw monetary scales would dominate Euclidean distance. Compare raw-standardized and log-standardized representations; PCA should visualize rather than define the final clusters.
- Mining goal/algorithm: compare several k values and a second algorithm. Choose by validation silhouette with a minimum cluster share; acknowledge that high separation may produce coarse groups.
- Mining: record hyperparameters, seeds, silhouette, Davies–Bouldin, and cluster shares; preserve a held-out test set.
- Interpretation: quantify stability under resampling and preprocessing refit; profile medians in original units and distinguish measured differences from marketing hypotheses.
- Knowledge use: save an auditable segment lookup and deployable assignment pipeline. Include an explicit gate for pilot use and monitoring; a cluster label alone is not a discovery.

## Revision 2 implementation

The notebooks implement the changes above. A second review of executed artifacts and its fixes will be recorded in `FINAL_REVIEW.md`. No unpublished Medium article or unrecorded video is described as published or completed.
