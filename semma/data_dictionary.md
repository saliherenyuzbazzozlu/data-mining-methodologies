# Data dictionary

| Column               | Role   | Meaning                                                                   |
|:---------------------|:-------|:--------------------------------------------------------------------------|
| fixed acidity        | input  | Fixed acidity measurement (conventionally g/dm³ as tartaric acid).        |
| volatile acidity     | input  | Volatile acidity measurement (conventionally g/dm³ as acetic acid).       |
| citric acid          | input  | Citric acid concentration (g/dm³).                                        |
| residual sugar       | input  | Residual sugar concentration (g/dm³).                                     |
| chlorides            | input  | Chloride concentration (g/dm³ as sodium chloride).                        |
| free sulfur dioxide  | input  | Free sulfur dioxide concentration (mg/dm³).                               |
| total sulfur dioxide | input  | Total sulfur dioxide concentration (mg/dm³).                              |
| density              | input  | Density (g/cm³).                                                          |
| pH                   | input  | Acidity measure, pH scale.                                                |
| sulphates            | input  | Sulphates concentration (g/dm³ as potassium sulphate).                    |
| alcohol              | input  | Alcohol by volume (%).                                                    |
| quality              | target | Sensory quality score; ordinal target, modeled numerically. Observed 3–8. |

This describes the source fields for the teaching analysis. Currency identity and a verified outcome-timing contract are not inferred from column names. Raw file hashes and source URLs are in `data/provenance.json`. Missingness and dtypes are measured in `artifacts/data_quality.csv`.

Chemical unit conventions should be checked against the source documentation before operational measurement integration; no conversion is performed by this project.
