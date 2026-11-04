# Optional SAS replication map

This project was executed in Python. SAS software was not available in the connected environment, and no SAS output is represented as executed. The assignment says to use a SAS trial “if possible.”

The SAS paper linked by the instructor demonstrates separating the sample, exploration, variable changes, modeling and assessment. It uses a retail purchase classification task; the present project independently uses regression on wine chemistry.

| SEMMA stage | Python implementation | Suggested SAS Enterprise Miner equivalent |
|---|---|---|
| Sample | Deduplicate and preserve identical-chemistry groups across partitions | Import the prepared dataset with its fixed partition indicator; assign quality as interval target and chemistry as interval inputs. Preserve the supplied partition rather than resampling rows. |
| Explore | Histograms, score distribution, skewness, correlation | StatExplore and MultiPlot nodes; review input roles and score imbalance. |
| Modify | Training-fold median imputation, scaling and optional 8-feature selection | Impute, Transform Variables and Variable Selection nodes. Ensure validation/test rows do not fit the transformations. |
| Model | Ridge and forest, compared with a mean-only baseline | Regression and HP Forest where licensed; settings are not numerically identical to scikit-learn. |
| Assess | Validation selection, final RMSE/MAE/R², residuals and target-level errors | Model Comparison and score output; calculate RMSE on the untouched test partition. |

For an actual SAS demonstration, import the CSV and `artifacts/split_manifest.csv`, joining `source_row` to the original zero-based row position after exact deduplication. Preserve `feature_group` and partition. Check counts against `sample_audit.json`. Record the version, licensed procedures, model settings, run log and screenshots. Do not claim equivalence merely because both tools call a model “random forest.”

Reference: [Soto Fuentes, SAS Global Forum 2013, paper 069-2013](https://support.sas.com/resources/papers/proceedings13/069-2013.pdf).
