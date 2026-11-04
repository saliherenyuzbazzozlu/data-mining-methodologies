# CRISP_DM — code and artifact walkthrough

The accompanying MP4 is a generated narrated walkthrough of actual executed artifacts. It uses the local Samantha synthetic voice; it is not a live recording of the student. Review it and replace the narration if personal presentation is required.

## 00:00 — The decision before the model

This is a generated walkthrough of the executed CRISP D M project. The narration is synthetic. The project asks whether a telecom retention team can concentrate observed churn cases in a review queue covering no more than twenty percent of a customer batch. The first phase defines the objective and the limits. The assumed technical target is a lift of at least two. The data contain historical churn labels, not campaign responses, so this is a ranking prototype, not evidence that a phone call prevents cancellation. The notebook, report, raw data provenance and all measured outputs are included in the project folder.

## 00:36 — Data understanding: reveal blank charges

The second phase begins with data understanding. The displayed code converts Total Charges from text to numeric values. Blank strings become missing values, revealing eleven missing entries that a simple raw CSV missing-value count would overlook. The checks require unique customer identifiers, the expected Yes and No labels, and nonnegative numerical fields. The raw dataset hash is verified before this code runs. The quality table is saved as an artifact, so these decisions can be inspected later. Missing accumulated charges do not justify silently removing a new customer.

## 01:12 — Lock the partitions before fitting

This excerpt creates a stratified sixty, twenty, twenty split. Training rows support exploration and cross validation. Validation rows choose between tuned model families. Test rows are reserved for the final evaluation. The assertion checks that the partitions do not overlap, and the manifest saves every row assignment. Stratification keeps churn prevalence similar across partitions. This is still a random split of a historical teaching dataset. Because reliable feature timestamps and a future outcome window are absent, it does not prove that the same scores would forecast next month.

## 01:47 — Data preparation stays inside the pipeline

The third phase selects the predictor columns and constructs the preprocessing pipeline. Customer I D and the target are excluded. Gender and senior status are reserved for diagnostics rather than direct prediction. Numerical columns receive training-median imputation and standard scaling. Categorical columns receive mode imputation and one hot encoding, with unknown categories allowed at scoring time. Keeping preprocessing inside the pipeline ensures that each cross validation fold learns its own transformation parameters. Removing demographic inputs does not guarantee fairness, since other features can carry correlated information.

## 02:25 — Modeling: compare and freeze

The modeling phase compares logistic regression and a random forest, with a separate prevalence-only baseline. Three-fold stratified cross validation tunes regularization and minimum leaf size using average precision. The full grid results are saved, not only the winning settings. Validation average precision selects logistic regression with C equal to one. The difference from the forest is small, about two thousandths, so the report does not claim universal superiority. Once selected, this training fit remains frozen for the final test and the saved deployment artifact.

## 02:59 — Evaluation: ranking performance

The held-out test set contains one thousand four hundred nine customers. Average precision is point six two two, and area under the R O C curve is point eight three two. The top twenty percent queue contains two hundred eighty one customers. About sixty one point six percent of that queue has observed churn, capturing forty six point three percent of all test churn cases. The resulting lift is two point three two. Five hundred bootstrap resamples give a lift interval of about two point one five to two point five six. This interval holds the fitted model fixed and does not represent future market uncertainty.

## 03:35 — Evaluation also exposes limitations

The calibration plot asks a different question: do predicted probabilities correspond to observed event frequencies? The notebook also saves Brier score, a confusion matrix and subgroup diagnostics. At the diagnostic threshold of point five, the senior group has a false positive rate of about twenty six point three percent, compared with nine point nine percent for the other group. These differences require review. The diagnostic threshold is not the top twenty percent ranking rule, so this table cannot certify the deployed queue as fair. The report also notes that test average precision is below validation performance.

## 04:12 — Deployment: inspect the actual handoff

The final phase exports the complete fitted pipeline, input schema, policy, sample input and sample output. The displayed check reloads the saved model and verifies prediction equivalence. It also tests an unseen contract category and a missing numeric value. From the repository root, run Python predict dot py, then crisp underscore d m, the sample input path, and the output flag. The scorer applies a strict floor of twenty percent times the batch size, rejects malformed inputs and writes an audit J son. Monitoring and rollback are documented. The next real step is a current-data pilot and randomized evidence before claiming retention benefit.

## Demonstration command

From the repository root, run:

```bash
python predict.py crisp_dm crisp_dm/artifacts/sample_input.csv --output crisp_dm/artifacts/demo_predictions.csv
python verify.py
```

Open the output CSV and adjacent audit JSON. The video shows code and saved results; it is not a screen recording of an interactive terminal session.
