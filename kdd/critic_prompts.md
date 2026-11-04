# Required model critique workflow — KDD

Status: ready to run in Claude or GPT-5; no transcript from those models has been fabricated. Current Codex critiques are in the root review documents.

Attach `analysis.ipynb`, `report.md`, `data_dictionary.md` and `artifacts/metrics.json`. Use the following prompt separately for every stage listed below. Save the exact model name shown in the interface, date, prompt, response and resulting changes.

> Adopt the perspective of a world-renowned speaker, leading authority and author of award-winning books on KDD. This is a role-play lens, not a claim of real credentials. Critique the attached project’s [STAGE] in depth. Check each subtask, assumptions, source attribution, leakage, code correctness, evaluation, uncertainty, interpretation and reproducibility. Identify concrete defects and prioritize corrections. Cite the exact cell or report passage. Do not invent executions, results, deployments or publications. Return a revised section and a checklist of evidence needed.

## Stages

- Domain understanding
- Target data selection
- Cleaning/preprocessing
- Transformation/projection
- Mining task
- Algorithm selection
- Mining
- Interpretation/evaluation
- Knowledge use

## Revision sequence

1. Round 1: collect a critique for every stage. Save the unedited response.
2. Apply justified changes. Record the before/after text and code. Re-execute affected analysis before updating numeric claims.
3. Round 2: provide the revised artifacts to the same or another permitted model. Ask it to verify the previous fixes and identify remaining gaps in every stage.
4. Apply and validate any further changes. If a change follows test inspection, label it exploratory or reserve genuinely new test data; do not claim the old test is untouched.
5. Keep original responses, changes, acceptance checks and student review notes together in a `critic_transcripts/` directory when publishing.

The expert persona does not replace evidence. Repeating a model's approval is not manual verification.
