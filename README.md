# Three data-mining methodologies, three complete analytical prototypes

CMPE-255 • Data Mining Process Assignment • Prepared November 3, 2026

This repository-ready package contains executed, self-contained notebooks and detailed reports. It is **not yet a completed Canvas submission**: student verification and hosted Colab runs and any literal Claude/GPT-5 transcript requirement remain in the [submission checklist](SUBMISSION_CHECKLIST.md).

| Methodology | Dataset / task | Held-out result | Main caveat |
|---|---|---|---|
| [CRISP-DM](crisp_dm/README.md) | Telco churn / ranking | AP 0.622; top-20% lift 2.319 | No causal retention evidence; group differences need review. |
| [SEMMA](semma/README.md) | Red wine quality / regression | RMSE 0.687; 21.6% lower than baseline | Errors are larger at rare extreme quality scores. |
| [KDD](kdd/README.md) | Card usage / clustering | Silhouette 0.246; median stability ARI 0.987 | Stable but only moderately separated descriptive groups. |

## Open the work

Each folder contains `analysis.ipynb`, `analysis.py`, `report.md`, `article_medium.md`, `walkthrough.md`, `data_dictionary.md`, source CSV/provenance, and `artifacts/` with results and models. The videos are supplied separately in the output folder and can be uploaded to YouTube; avoid committing large video files to GitHub.

- [All 25 assignment links and access notes](LINK_REVIEW.md)
- [Initial design, first critique and revisions](PLANNING_AND_REVIEW.md)
- [Executed-work critique and revisions](FINAL_REVIEW.md)
- [Publication and student verification checklist](SUBMISSION_CHECKLIST.md)

## Reproduce locally

Use Python 3.9–3.12 and a CPU environment. From this repository folder:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_notebooks.py
```

Run a single project by appending `crisp_dm`, `semma`, or `kdd`. The notebooks use bundled data, or retrieve the public Kaggle archive and verify its hash. A changed upstream version fails clearly. Each run writes its own project artifacts. Saved joblib files should only be loaded from trusted sources and with compatible package versions.

## Run the deployment demos

```bash
python predict.py crisp_dm crisp_dm/artifacts/sample_input.csv --output crisp_dm/artifacts/demo_predictions.csv
python predict.py semma semma/artifacts/sample_input.csv --output semma/artifacts/demo_predictions.csv
python predict.py kdd kdd/artifacts/sample_input.csv --output kdd/artifacts/demo_predictions.csv
python verify.py
```

The scorer checks input schemas and creates an adjacent audit JSON. These are local prototypes with proposed monitoring plans; no real business intervention or live cloud service is claimed.

## Run in Colab

Open Google Colab, choose **File → Upload notebook**, and select one project's `analysis.ipynb`. Run cells in order. Without the local CSV, the notebook downloads the public Kaggle dataset and validates its hash. In a fresh runtime, uncomment the optional `%pip install` cell if needed. After a GitHub upload, use Colab's GitHub notebook picker or an Open in Colab link pointing to the real repository; this package does not invent a repository URL.

## Authorship, sources and publication

The implementation, review and drafts were produced with Codex assistance. Actual numerical outputs were obtained by execution. Example repositories were reviewed for structure and were not copied as this project's implementation. Dataset ownership and terms remain with their sources; inspect the linked Kaggle terms before redistribution. The two reviews are labeled Codex and do not impersonate a Claude/GPT-5 run. The student must verify the work and complete the checklist before representing the assignment as finished.

## Video walkthroughs

- [CRISP_DM](https://youtu.be/RpL7WDW_gsY)
- [SEMMA](https://youtu.be/eyYKo6OdzqI)
- [KDD](https://youtu.be/XXwhyxQ5_nw)

Each uploaded video begins with the student’s own recorded voice; the remaining walkthrough uses synthetic narration.

## Published articles and Colab entry points

- CRISP_DM: [Medium article](https://medium.com/@saliheren.yuzbazzozlu/a-churn-model-is-only-useful-when-the-review-queue-is-useful-032d5b7938b4) · [Open notebook in Colab](https://colab.research.google.com/github/saliherenyuzbazzozlu/data-mining-methodologies/blob/main/crisp_dm/analysis.ipynb)
- SEMMA: [Medium article](https://medium.com/@saliheren.yuzbazzozlu/predicting-wine-quality-without-letting-duplicates-inflate-the-result-660980e2ac21) · [Open notebook in Colab](https://colab.research.google.com/github/saliherenyuzbazzozlu/data-mining-methodologies/blob/main/semma/analysis.ipynb)
- KDD: [Medium article](https://medium.com/@saliheren.yuzbazzozlu/when-two-customer-segments-are-more-defensible-than-five-df5bb3d6ca25) · [Open notebook in Colab](https://colab.research.google.com/github/saliherenyuzbazzozlu/data-mining-methodologies/blob/main/kdd/analysis.ipynb)
