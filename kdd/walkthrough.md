# KDD — code and artifact walkthrough

The accompanying MP4 is a generated narrated walkthrough of actual executed artifacts. It uses the local Samantha synthetic voice; it is not a live recording of the student. Review it and replace the narration if personal presentation is required.

## 00:00 — KDD: turn a partition into a question

This generated walkthrough explains the executed K D D project on historical card usage summaries. The narration is synthetic. The purpose is descriptive service research, not credit scoring. No cluster should determine lending eligibility, a credit limit or a price. The notebook follows nine steps: domain understanding, target data selection, cleaning, transformation, task choice, algorithm choice, mining, interpretation and knowledge use. The common five-stage diagram groups these into selection, preprocessing, transformation, mining and interpretation. The key idea is that fitting a clustering algorithm is only one part of discovering useful knowledge.

## 00:42 — Selection and a real data-quality revision

The target dataset has eight thousand nine hundred fifty rows. Customer identifiers are excluded from distance calculations. A structural check found eight cash-advance-frequency values above one, with a maximum of one point five. Rather than assume a correction or silently clip them, the revised project excludes that ambiguous field and retains cash-advance amount and count. This code records the exclusion decision. It then creates disjoint discovery, validation and test partitions. The quality issue was resolved before the analysis reached final test evaluation.

## 01:16 — Preprocess and transform

The preprocessing stage imputes missing values from discovery rows. Missing minimum payments are not interpreted as zero payments. The transformation code treats monetary amounts and transaction counts separately from frequency and tenure variables. It compares raw standardization with log one plus x followed by standardization. The logarithm handles zero and reduces heavy-tail influence. The selected representation retains sixteen eligible predictors. Principal component analysis is reserved for visualization rather than replacing the space in which the clusters are fitted.

## 01:50 — Choose the task, algorithms and rule

The mining task is unsupervised clustering because no target label is available. Classification accuracy would be meaningless here. The experiment compares fifteen candidates: five K-means choices on raw-standardized inputs, five on log-standardized inputs and five diagonal Gaussian mixtures on log-standardized inputs. The fixed selection rule maximizes validation silhouette while requiring every validation group to contain at least five percent of rows. Davies Bouldin scores are recorded as a complementary measure. This explicit rule prevents choosing a visually attractive number of segments after inspecting the test set.

## 02:27 — Mine and test stability

The rule selected log-transformed K-means with two clusters. This excerpt then tests partition stability. Five alternative pipelines are refitted on eighty percent discovery subsamples. Importantly, each refit learns preprocessing again, rather than changing only the clustering step. Validation predictions from each alternative are compared with the original assignments using adjusted Rand index. This measure does not require numeric cluster labels to match. The median score is point nine eight seven, showing strong repeatability under this particular sampling design. It does not prove that the groups are naturally occurring customer categories.

## 03:05 — Interpret: moderate separation, stable labels

The final test silhouette is point two four six and the Davies Bouldin score is about one point five seven six. The test groups contain one thousand forty eight and seven hundred forty two rows. These findings describe moderate geometric separation together with high resampling stability. The displayed two-dimensional P C A view explains fifty six point two percent of transformed discovery variance. It omits a substantial amount of information. Cluster assignments were made using all sixteen eligible transformed variables, not by drawing a dividing line on this picture.

## 03:39 — Interpret original-unit profiles

The original-unit profile table is essential for understanding the labels. Cluster zero has median purchases of eight hundred sixty two point two two, purchase frequency about point nine zero nine, fourteen purchase transactions and zero cash advance. Cluster one has median purchases of zero and median cash advance about nine hundred fifteen point four eight. Working descriptions are purchase-active and low-purchase slash cash-advance profiles. These are medians, not claims about every customer. The report does not infer wealth, distress, creditworthiness or the causal effect of any marketing action.

## 04:15 — Knowledge use and deployment artifact

The final K D D step consolidates the pattern and proposes a testable use. One defensible follow-up is to interview consenting participants from both usage profiles about which product functions they use and why. The saved pipeline assigns a new batch consistently, and the excerpt verifies that reloading the model preserves assignments. Run the shared predict script with the k d d project and the sample input. Monitor missingness, new numerical ranges and segment-share changes. A new model requires renewed stability checks and reviewed group descriptions, because cluster numbers may change. The deliverable is a reproducible discovery prototype and a bounded follow-up question, not an automated customer decision system.

## Demonstration command

From the repository root, run:

```bash
python predict.py kdd kdd/artifacts/sample_input.csv --output kdd/artifacts/demo_predictions.csv
python verify.py
```

Open the output CSV and adjacent audit JSON. The video shows code and saved results; it is not a screen recording of an interactive terminal session.
