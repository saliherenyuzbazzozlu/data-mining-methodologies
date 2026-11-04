# Submission checklist and honest completion status

Canvas asks for a **website URL**, with all artifacts in GitHub. Do not submit a local filesystem path or this ZIP as if it were the required URL.

## Prepared and verified locally

- [x] Three separate projects and three different Kaggle datasets.
- [x] CRISP-DM six phases, SEMMA five phases, and KDD nine-step workflow.
- [x] Executed notebooks with outputs, saved models, plots, comparison tables and split manifests.
- [x] Detailed reports, dictionaries, raw data checksums and source attribution.
- [x] Two genuine Codex critique rounds and documented revisions.
- [x] Three Medium-ready article drafts.
- [x] Three 1080p walkthrough videos with disclosed synthetic narration (4:53, 4:41, 4:58); full decoding and audio checks passed.
- [x] Local batch deployment scripts and input-contract checks.
- [x] Every distinct assignment URL checked or attempted; access limits documented.

## Remaining before the assignment is fully submitted

- [ ] Review all code yourself. Explain at least one preprocessing step, the split logic, one metric and one limitation per project. Record your notes; do not claim a human review you did not do.
- [ ] If the instructor requires the named model literally, run the supplied per-stage prompts in **Claude or GPT-5**, revise twice, and preserve actual transcripts. Codex review is disclosed separately and is not mislabeled as either model.
- [ ] Open each notebook in Google Colab, run all cells and preserve the hosted notebook or GitHub-to-Colab link. Local execution has been verified; hosted execution has not.
- [ ] Create/publish a GitHub repository containing this package. Preserve the three project folders. Check source dataset redistribution terms before public upload; notebooks can download the data even if raw CSVs are omitted.
- [x] Publish the three articles to Medium; actual publication verified.
- [x] Walkthroughs uploaded by the student; titles and durations verified. Each has a personal recorded introduction followed by synthetic narration.
- [ ] Finish viewing the two linked source videos and obtain the unavailable UHCL PDF if required by the instructor.
- [ ] Put the GitHub, Colab, Medium and YouTube links in the repository README and verify that the instructor can open them.
- [ ] Submit the repository URL in Canvas and check the submission confirmation.

## Publication links

| Deliverable | URL/status |
|---|---|
| GitHub repository | https://github.com/saliherenyuzbazzozlu/data-mining-methodologies |
| CRISP-DM Colab | GitHub-to-Colab link in README; hosted execution not verified |
| SEMMA Colab | GitHub-to-Colab link in README; hosted execution not verified |
| KDD Colab | GitHub-to-Colab link in README; hosted execution not verified |
| CRISP-DM Medium | https://medium.com/@saliheren.yuzbazzozlu/a-churn-model-is-only-useful-when-the-review-queue-is-useful-032d5b7938b4 |
| SEMMA Medium | https://medium.com/@saliheren.yuzbazzozlu/predicting-wine-quality-without-letting-duplicates-inflate-the-result-660980e2ac21 |
| KDD Medium | https://medium.com/@saliheren.yuzbazzozlu/when-two-customer-segments-are-more-defensible-than-five-df5bb3d6ca25 |
| CRISP-DM YouTube | https://youtu.be/RpL7WDW_gsY |
| SEMMA YouTube | https://youtu.be/eyYKo6OdzqI |
| KDD YouTube | https://youtu.be/XXwhyxQ5_nw |
| Canvas submission | Not submitted |

## Student verification exercises

1. Open `data/provenance.json` and check the raw file's SHA-256. Find the notebook assertion that enforces it.
2. Explain why imputation happens inside a pipeline and why wine splitting uses feature groups.
3. Recalculate churn precision/lift from `test_predictions.csv`, wine RMSE from observed/predicted columns, and cluster counts from `test_assignments.csv`.
4. Inspect the raw cash-advance-frequency values above 1 and explain why the field was excluded.
5. Run the batch scorer on the provided sample and compare the saved model's output. Try a missing column and a negative input and explain the error.
6. Review the plots and the adverse subgroup/extreme-score findings; customize the articles so you can explain every claim.
