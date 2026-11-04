"""Independent checks of saved predictions, partitions, and batch deployment contracts."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import nbformat
from predict import score

ROOT = Path(__file__).resolve().parent
checks = []
for project in ['crisp_dm', 'semma', 'kdd']:
    p = ROOT / project
    nb = nbformat.read(p / 'analysis.ipynb', as_version=4)
    nbformat.validate(nb)
    code = [c for c in nb.cells if c.cell_type == 'code']
    assert all(c.execution_count is not None for c in code)
    assert not [o for c in code for o in c.outputs if o.output_type == 'error']
    split = pd.read_csv(p / 'artifacts/split_manifest.csv')
    key = 'source_row' if project == 'semma' else 'row_id'
    assert split[key].is_unique
    assert set(split.partition) == {'train', 'validation', 'test'}
    if project == 'semma':
        assert split.groupby('feature_group').partition.nunique().max() == 1
    sample = pd.read_csv(p / 'artifacts/sample_input.csv')
    actual, audit = score(project, sample)
    expected = pd.read_csv(p / 'artifacts/sample_output.csv')
    np.testing.assert_allclose(actual[expected.columns].to_numpy(), expected.to_numpy(), rtol=1e-9, atol=1e-9)
    try:
        score(project, sample.drop(columns=sample.columns[0]))
        raise AssertionError('Missing column was accepted')
    except ValueError as e:
        assert 'Missing required columns' in str(e)
    numeric = json.loads((p / 'artifacts/schema.json').read_text())['numeric'][0]
    bad = sample.copy(); bad.loc[0, numeric] = -1
    try:
        score(project, bad)
        raise AssertionError('Negative value was accepted')
    except ValueError as e:
        assert 'Negative or infinite' in str(e)
    bad = sample.copy(); bad[numeric] = bad[numeric].astype(object); bad.loc[0, numeric] = 'broken'
    try:
        score(project, bad)
        raise AssertionError('Nonnumeric value was accepted')
    except ValueError as e:
        assert 'Nonnumeric' in str(e)
    actual.to_csv(p / 'artifacts/demo_predictions.csv', index=False)
    (p / 'artifacts/demo_predictions.audit.json').write_text(json.dumps(audit, indent=2))
    checks.append(project + ': notebook, partition, scorer equivalence and invalid-input checks passed')

p = ROOT / 'crisp_dm/artifacts'
d = pd.read_csv(p / 'test_predictions.csv'); m = json.loads((p / 'metrics.json').read_text())
top = d.sort_values('probability', ascending=False, kind='stable').head(int(.2 * len(d)))
lift = top.observed.mean() / d.observed.mean()
assert np.isclose(lift, m['test']['lift_at_20pct'])
sample = pd.read_csv(p / 'sample_input.csv')
tiny, _ = score('crisp_dm', sample.iloc[:1]); assert tiny.review_top_20pct.sum() == 0
assert score('crisp_dm', sample)[0].review_top_20pct.sum() == 1
checks.append('Churn: independent lift calculation and strict 20% capacity boundaries passed')
p = ROOT / 'semma/artifacts'
d = pd.read_csv(p / 'test_predictions.csv'); m = json.loads((p / 'metrics.json').read_text())
assert np.isclose(np.sqrt(np.mean((d.observed-d.predicted)**2)), m['test']['RMSE'])
checks.append('Wine: independent RMSE calculation passed')
p = ROOT / 'kdd/artifacts'
d = pd.read_csv(p / 'test_assignments.csv'); m = json.loads((p / 'metrics.json').read_text())
np.testing.assert_allclose(d.cluster.value_counts(normalize=True).sort_index(), m['test_cluster_shares'])
checks.append('KDD: independent cluster share calculation passed')
result = {'status': 'passed', 'checks': checks, 'human_review_completed': False}
(ROOT / 'verification_summary.json').write_text(json.dumps(result, indent=2))
print('\n'.join(checks))
