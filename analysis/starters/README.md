# Analysis Practice Starters

Practice notebooks develop the first Project 1 spatial analysis incrementally:

1. frame a decision and spatial question
2. inspect units, CRS, scale, and measurement
3. perform and reconcile a point-in-polygon aggregation
4. normalize, validate, and communicate results

These canonical notebooks are clean, version-controlled originals. Create ignored working copies with:

```bash
python scripts/reset_notebook.py <module> --analysis
```

After completing and reviewing a working notebook, preserve it with:

```bash
python scripts/save_attempt.py <module> --analysis
```