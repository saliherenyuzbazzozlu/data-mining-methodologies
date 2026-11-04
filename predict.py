"""Local batch deployment. Loads only the trusted model artifacts in this project."""
from pathlib import Path
import argparse
import json
import warnings
import numpy as np
import pandas as pd
import joblib

ROOT = Path(__file__).resolve().parent

def score(project, frame):
    folder = ROOT / project / 'artifacts'
    schema = json.loads((folder / 'schema.json').read_text())
    missing = sorted(set(schema['features']) - set(frame.columns))
    if missing:
        raise ValueError('Missing required columns: ' + ', '.join(missing))
    if frame.empty:
        raise ValueError('Input batch is empty')
    X = frame[schema['features']].copy()
    audit = {'rows': len(X), 'out_of_training_range': {}, 'unknown_category_counts': {}}
    for col in schema['numeric']:
        original = X[col]
        converted = pd.to_numeric(original, errors='coerce')
        invalid = original.notna() & converted.isna()
        if invalid.any():
            raise ValueError(f'Nonnumeric values in {col}')
        if np.isinf(converted).any() or (converted.dropna() < 0).any():
            raise ValueError(f'Negative or infinite values in {col}')
        if col in schema.get('frequency', []) and (converted.dropna() > 1).any():
            raise ValueError(f'Proportions above 1 in {col}')
        X[col] = converted
        low, high = schema['numeric_ranges'][col]
        audit['out_of_training_range'][col] = int(((converted < low) | (converted > high)).sum())
    for col in schema['categorical']:
        allowed = schema.get('categories', {}).get(col, [])
        audit['unknown_category_counts'][col] = int((X[col].notna() & ~X[col].isin(allowed)).sum())
    audit['missing_fraction'] = X.isna().mean().to_dict()
    if any(audit['out_of_training_range'].values()) or any(audit['unknown_category_counts'].values()):
        warnings.warn('Input drift flags found; inspect the audit JSON before using predictions.')
    model = joblib.load(folder / 'model.joblib')
    if project == 'crisp_dm':
        p = model.predict_proba(X)[:, 1]
        selected = np.zeros(len(X), dtype=bool)
        # Strictly at most 20%; batches below five rows select zero contacts.
        n = int(.2 * len(X))
        selected[np.argsort(-p, kind='stable')[:n]] = True
        result = pd.DataFrame({'churn_probability': p, 'review_top_20pct': selected})
    elif project == 'semma':
        result = pd.DataFrame({'predicted_quality': model.predict(X)})
    else:
        result = pd.DataFrame({'cluster': model.predict(X)})
    return result, audit

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', choices=['crisp_dm', 'semma', 'kdd'])
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result, audit = score(args.project, pd.read_csv(args.input))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    args.output.with_suffix('.audit.json').write_text(json.dumps(audit, indent=2))
    print(result.to_string(index=False))
