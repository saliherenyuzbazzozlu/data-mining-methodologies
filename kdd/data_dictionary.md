# Data dictionary

| Column                           | Role             | Meaning                                                               |
|:---------------------------------|:-----------------|:----------------------------------------------------------------------|
| CUST_ID                          | excluded / audit | Anonymized customer ID; excluded from modeling.                       |
| BALANCE                          | input            | Balance amount in source currency units.                              |
| BALANCE_FREQUENCY                | input            | Frequency of balance updates, encoded fraction.                       |
| PURCHASES                        | input            | Total purchase amount.                                                |
| ONEOFF_PURCHASES                 | input            | One-off purchase amount.                                              |
| INSTALLMENTS_PURCHASES           | input            | Installment purchase amount.                                          |
| CASH_ADVANCE                     | input            | Cash-advance amount.                                                  |
| PURCHASES_FREQUENCY              | input            | Purchase frequency, encoded fraction.                                 |
| ONEOFF_PURCHASES_FREQUENCY       | input            | One-off purchase frequency, encoded fraction.                         |
| PURCHASES_INSTALLMENTS_FREQUENCY | input            | Installment purchase frequency, encoded fraction.                     |
| CASH_ADVANCE_FREQUENCY           | excluded / audit | Ambiguous frequency: 8 values exceed 1; excluded rather than clipped. |
| CASH_ADVANCE_TRX                 | input            | Cash-advance transaction count.                                       |
| PURCHASES_TRX                    | input            | Purchase transaction count.                                           |
| CREDIT_LIMIT                     | input            | Recorded credit-limit amount; 1 missing value.                        |
| PAYMENTS                         | input            | Payment amount.                                                       |
| MINIMUM_PAYMENTS                 | input            | Minimum-payment amount; 313 missing values.                           |
| PRC_FULL_PAYMENT                 | input            | Full-payment proportion.                                              |
| TENURE                           | input            | Tenure field in months.                                               |

This describes the source fields for the teaching analysis. Currency identity and a verified outcome-timing contract are not inferred from column names. Raw file hashes and source URLs are in `data/provenance.json`. Missingness and dtypes are measured in `artifacts/data_quality.csv`.
