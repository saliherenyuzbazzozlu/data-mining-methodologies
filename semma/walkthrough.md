# SEMMA — code and artifact walkthrough

The accompanying MP4 is a generated narrated walkthrough of actual executed artifacts. It uses the local Samantha synthetic voice; it is not a live recording of the student. Review it and replace the narration if personal presentation is required.

## 00:00 — SEMMA: predict a sensory score

This generated walkthrough explains the executed SEMMA project using red wine quality data. The narration is synthetic. The five stages are Sample, Explore, Modify, Model and Assess. A hypothetical lab wants a numerical estimate of a sensory quality score from eleven chemistry measurements. The technical goal is at least ten percent lower root mean squared error than a training-mean baseline. This is not a replacement for sensory judges. The implementation uses Python, and a separate document maps the workflow to optional SAS nodes. No SAS execution is claimed.

## 00:35 — Sample: remove duplicate leakage

The Sample stage contains an important correction. The raw file has one thousand five hundred ninety nine rows, including two hundred forty exact duplicates. The code removes exact duplicates, leaving one thousand three hundred fifty nine observations. It then hashes the predictor columns to identify identical chemistry profiles, even if their target scores differ. Group Shuffle Split keeps those profiles together. The resulting counts are eight hundred fifteen training rows, two hundred seventy two validation rows and two hundred seventy two test rows. This protects against a recognizable form of leakage, although unknown producer and vintage dependence remains possible.

## 01:15 — Explore: inspect the chemistry and target

The Explore stage uses training data only to inspect distributions, skewness, the sensory-score balance and correlations. This chart includes the target for exploratory comparison. Relationships are observational: a correlation does not show that changing a chemical concentration would improve taste. Valid extreme measurements are retained rather than automatically trimmed. The target is ordinal, so numerical regression is an approximation that assumes adjacent score differences are reasonably comparable. The accompanying histograms and data dictionary make the feature meanings and distributions inspectable.

## 01:51 — Modify: train-only transformations

The Modify stage builds imputation and scaling into the learning pipeline. This means a cross validation fold cannot learn its median or scale from held-out rows. The model grid also compares an eight-feature selection with all eleven inputs for ridge regression. Selection is fitted within the same pipeline, preventing target leakage. The winning forest uses all eleven features, so the report does not pretend that feature removal improved the final result. The schema records the expected columns and observed training ranges for later scoring audits.

## 02:22 — Model: grouped cross-validation

The Model stage compares ridge regression and a random forest with a mean-only baseline. Three-fold Group K Fold preserves chemistry groups during tuning. Negative root mean squared error is the cross validation scoring convention, so the code reverses its sign when reporting ordinary positive error. Validation error selects the random forest. The chosen forest has one hundred fifty trees and a minimum leaf size of eight. This setting regularizes the model by preventing leaves that depend on just one or two examples. All grid results and the validation comparison are saved.

## 02:56 — Assess: improvement and residuals

The final test root mean squared error is point six eight seven quality points. The mean-only baseline is point eight seven six. That is about a twenty one point six percent reduction, exceeding the assumed ten percent gate. Mean absolute error is point five four zero, and eighty eight point two percent of predictions are within one score point. The plots show both observed versus predicted scores and residuals. The model tends to pull extreme scores toward the middle, an important limitation that a single aggregate metric would hide.

## 03:26 — Assess: look at the tails

The error-by-score artifact makes the tail behavior explicit. The three score-three test wines were overpredicted by about two points on average. The two score-eight wines were underpredicted by about one point five four points. Those counts are very small, so they do not support precise population-level conclusions. They do show why the prototype should not automatically reject low-quality batches or approve premium products. Validation permutation importance ranks alcohol and sulphates highly, but that is dependence of this fitted predictor, not causal evidence about flavor.

## 04:00 — Delivery: reproducible batch scoring

The delivery extension saves the entire fitted pipeline, checks that reloading it preserves predictions, and writes sample input and output files. The shared batch scorer preserves input order, checks required columns and numerical validity, and produces an audit file with missingness and range flags. Run Python predict dot py with the semma project, sample input and output path. The monitoring plan calls for new validation when measurements or tasting procedures change. The full notebook, detailed report, article draft, model comparison, error tables and critique records are ready for review. A hosted Colab run and publication are still separate steps.

## Demonstration command

From the repository root, run:

```bash
python predict.py semma semma/artifacts/sample_input.csv --output semma/artifacts/demo_predictions.csv
python verify.py
```

Open the output CSV and adjacent audit JSON. The video shows code and saved results; it is not a screen recording of an interactive terminal session.
