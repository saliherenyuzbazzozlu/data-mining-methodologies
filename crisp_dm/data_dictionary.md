# Data dictionary

| Column           | Role             | Meaning                                                                 |
|:-----------------|:-----------------|:------------------------------------------------------------------------|
| customerID       | excluded / audit | Customer identifier; excluded from predictors.                          |
| gender           | excluded / audit | Recorded gender category; diagnostic only.                              |
| SeniorCitizen    | excluded / audit | Recorded senior indicator (0/1); diagnostic only.                       |
| Partner          | input            | Whether a partner is recorded.                                          |
| Dependents       | input            | Whether dependents are recorded.                                        |
| tenure           | input            | Customer tenure in months.                                              |
| PhoneService     | input            | Phone-service subscription category.                                    |
| MultipleLines    | input            | Multiple-line subscription category, including no phone service.        |
| InternetService  | input            | Internet-service category.                                              |
| OnlineSecurity   | input            | Online-security subscription category.                                  |
| OnlineBackup     | input            | Online-backup subscription category.                                    |
| DeviceProtection | input            | Device-protection subscription category.                                |
| TechSupport      | input            | Technical-support subscription category.                                |
| StreamingTV      | input            | Streaming-TV subscription category.                                     |
| StreamingMovies  | input            | Streaming-movie subscription category.                                  |
| Contract         | input            | Contract duration/type.                                                 |
| PaperlessBilling | input            | Paperless-billing indicator.                                            |
| PaymentMethod    | input            | Payment-method category.                                                |
| MonthlyCharges   | input            | Monthly charge amount, dataset currency units.                          |
| TotalCharges     | input            | Accumulated charge amount; blank entries become missing numeric values. |
| Churn            | target           | Recorded Yes/No churn outcome; target, excluded from input.             |

This describes the source fields for the teaching analysis. Currency identity and a verified outcome-timing contract are not inferred from column names. Raw file hashes and source URLs are in `data/provenance.json`. Missingness and dtypes are measured in `artifacts/data_quality.csv`.
