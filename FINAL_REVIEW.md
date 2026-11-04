# Second expert critique — executed implementation

Reviewer: the Codex assistant in this chat, using the expert persona recorded in `PLANNING_AND_REVIEW.md`. This is an actual second review after execution; it is not a fabricated GPT-5/Claude transcript or human sign-off.

## CRISP-DM

| Phase | Critique after execution | Revision / disposition |
|---|---|---|
| Business understanding | Lift 2.319 meets the assumed proxy, but no interventions were observed. A statement that churn was reduced would be false. | Reports and article distinguish queue concentration from retention improvement; require randomized pilot for causal benefit. |
| Data understanding | `TotalCharges` blank conversion matters; historical data lack a verifiable pre-outcome snapshot. | Keep all 7,043 records and document missingness, timestamps and inference limits in the report and dictionary. |
| Preparation | Excluding demographics does not remove proxies. | Include group performance and explicit limits rather than call the model fair. |
| Modeling | Logistic and forest validation AP differ by only about 0.0024; this is not evidence of universal superiority. | Describe the winner as selected by the fixed rule in this split, retain all candidate CV evidence. |
| Evaluation | Test AP is lower than validation AP. Senior-group FPR is 0.263 versus 0.099, at the diagnostic 0.5 threshold. | Report the generalization gap and disparity. Do not confuse this threshold with the top-20% operational policy. |
| Deployment | A notebook export alone lacks an input contract; tiny batches can accidentally exceed a strict budget if at least one row is always selected. | Added `predict.py` schema/range/category audit and strict floor(0.2×N) selection, with boundary and malformed-input checks. |

## SEMMA

| Phase | Critique after execution | Revision / disposition |
|---|---|---|
| Sample | Duplicate removal and feature-group separation are correct but do not address unobserved winery/vintage groups. | State the remaining dependence limitation and avoid claims of population representativeness. |
| Explore | Scores 3 and 8 have only 3 and 2 test examples. | Discuss uncertainty and keep subgroup counts beside errors. |
| Modify | The optional 8-feature route did not win. Claiming feature selection improved this model would be false. | Record all 11 retained chemistry variables and disclose selection results. |
| Model | The forest is regularized with leaf size 8 and uses all variables. | Preserve actual chosen settings, baseline and CV table. |
| Assess | RMSE improves 21.6%, but predictions shrink extremes toward the center. | Report extreme-score bias; restrict use to a prototype and require external sensory validation. |
| Delivery extension | Reproducibility requires feature ordering and saved preprocessing; a SAS run is absent. | Added schema-aware scorer and an explicitly unexecuted optional SAS mapping. |

## KDD

| Step | Critique after execution | Revision / disposition |
|---|---|---|
| 1. Domain | Card usage could be misread as risk or wealth. | Restrict interpretation to observed service-usage patterns. |
| 2. Selection | IDs are excluded, but one frequency field has an ambiguous range. | Exclude `CASH_ADVANCE_FREQUENCY` after the data check found eight values above 1. Preserve raw data and the decision record. |
| 3. Preprocessing | Blind clipping would invent corrected data. | Exclude the ambiguous feature; retain amount and count. Rerun before reaching the final test stage. |
| 4. Transformation | The selected log representation changes distance meaning. | Explain relative versus absolute amounts; report 2D PCA variance of 56.2% rather than imply the plot contains all information. |
| 5. Mining task | No ground-truth labels exist. | Report clustering metrics, not accuracy; do not treat group contrasts as independent significance tests. |
| 6. Algorithm choice | Two clusters give the largest eligible validation silhouette, even though more groups may seem attractive. | Keep the declared rule and explain the coarse partition; retain alternative k and GMM results. |
| 7. Mining | Stability requires re-fitting preprocessing, not only changing labels on fixed data. | Five 80% subsample fits refit the whole pipeline; median validation ARI is 0.987. |
| 8. Interpretation | Silhouette 0.246 suggests only moderate separation despite high stability. | Report both; describe purchase-active and cash-advance-oriented profiles without claiming natural customer types. |
| 9. Knowledge use | Cluster numbers do not specify an operational action. | Add a concrete interview hypothesis, batch scorer, monitoring/rollback plan and clear limits. |

## Remaining requirements that cannot be certified by code

- Actual Claude/GPT-5 critique exports if the named model requirement is strict. `critic_prompts.md` provides the exact per-stage workflow; current reviews are labeled Codex.
- The student's manual code verification and a hosted Colab run.
- GitHub publication, three Medium publications, YouTube uploads, and the final Canvas URL submission.
- Full viewing of two linked videos and access to the unavailable UHCL PDF.

These are deliberately not marked complete. See the submission checklist for the concrete handoff.
