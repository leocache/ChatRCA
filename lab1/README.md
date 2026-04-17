# lab1 — GAIA experiment (seed 123, 70/15/15 by case)

This branch contains a **single archive** with the pipeline script and the full run outputs for:

- **Split:** `stratified_70_15_15_by_case` (train/val/test by `F_*` case, no case spanning splits)
- **Ratios:** `--train_ratio 0.7` `--val_ratio 0.15` (test ≈ 0.15)
- **Seed:** `123`
- **Data:** `src/GAIA` (not included in the zip; clone this repo and place GAIA under `src/GAIA` or pass `--gaia_dir`)

## Archive

| File | Contents |
|------|----------|
| `lab1_seed123_70_15_15_by_case_bundle.zip` | `code/gaia_train_all_in_one(3).py` + `results/gaia_exp1_70_15_15_by_case_seed123/` (all CSV/JSON/txt/models from that run) |

## Reproduce

```bash
python "gaia_train_all_in_one(3).py" \
  --gaia_dir "<path_to>/src/GAIA" \
  --output_dir "./out_lab1" \
  --split_mode stratified_70_15_15_by_case \
  --train_ratio 0.7 \
  --val_ratio 0.15 \
  --seed 123
```

## Branch policy

Work for lab1 lives on branch **`lab1`** only; do not merge experiment bundles to **`main`** without review.
