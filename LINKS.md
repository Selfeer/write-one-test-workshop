# Links to the suite examples in the deck

Every link points at clickhouse-regression `main` as of commit `5ef9016` (2026-11-24),
so the line numbers stay correct even after the code changes.

## Slides 17 and 33: one test, 1,089 runs

[`functions/tests/plus.py`](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/functions/tests/plus.py#L6-L31)

- [`@TestSketch`](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/functions/tests/plus.py#L6): one test body, run for every combination.
- [`either()` variables](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/functions/tests/plus.py#L27-L28).
- [The Python oracle and the string comparison](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/functions/tests/plus.py#L29-L31).
- Entry point for the demo command: [`functions/regression.py`](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/functions/regression.py).

## Slide 19: four ways to choose combinations

1. **Edge values:** [the value list in `plus.py`](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/functions/tests/plus.py#L12-L25), with `inf`, `nan`, the largest and smallest floats, and 1/3.
2. **Pairs:** [`s3/tests/combinatoric_table.py`](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/s3/tests/combinatoric_table.py#L204-L213).
3. **Random sample with a fixed seed:** [`random.seed(42)`](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/rbac/tests/multiple_auth_methods/simple_combinatorics/simple_combinatorics.py#L15) and [`random.sample(combinations, 3000)`](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/rbac/tests/multiple_auth_methods/simple_combinatorics/simple_combinatorics.py#L156-L160).
4. **`--stress` runs everything:** [rbac skips the sampling](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/rbac/tests/multiple_auth_methods/simple_combinatorics/simple_combinatorics.py#L159-L160), and [s3 switches from pairs to every combination](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/s3/tests/combinatoric_table.py#L204).

## Slide 20: pairwise

- **Main example:** [`s3/tests/combinatoric_table.py`](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/s3/tests/combinatoric_table.py#L204-L213).
  [The variables](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/s3/tests/combinatoric_table.py#L15) are table configurations.
  Normal runs cover every pair (`strength=2`). With `--stress` the strength becomes the number of variables, which means every combination.
- **Stronger coverage (`strength=3`, every combination of 3 values):** [`alter/table/move_partition/partition_key.py`](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/alter/table/move_partition/partition_key.py#L406).
- **Strongest (`strength=5`):** [`rbac/tests/sql_security/cascading_views.py`](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/rbac/tests/sql_security/cascading_views.py#L1418).

## Slide 21: order matters

In `rbac/tests/multiple_auth_methods/simple_combinatorics/simple_combinatorics.py`:

- [The 446,865 sequences: create × alter × alter × alter](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/rbac/tests/multiple_auth_methods/simple_combinatorics/simple_combinatorics.py#L135-L170).
- [Running one sequence and trying to log in after each step](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/rbac/tests/multiple_auth_methods/simple_combinatorics/simple_combinatorics.py#L113-L131).

## Slide 22: concurrency, parallel runs, faults

- **Parallel runs, 10 at a time:** [rbac's `Pool(10)` and `parallel=True`](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/rbac/tests/multiple_auth_methods/simple_combinatorics/simple_combinatorics.py#L162-L170).
- **Random groups of 3 actions:** [`build_action_groups`](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/alter/stress/tests/stress_alter.py#L103-L123) in `alter/stress`, using `combinations(…, 3, with_replacement=True)` and then a shuffle.
- **Groups run at the same time:** [`parallel=run_groups_in_parallel`](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/alter/stress/tests/stress_alter.py#L255-L290).
- **A random network fault for each group:** [the code](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/alter/stress/tests/stress_alter.py#L260-L268), using [`tc_netem.py`](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/alter/stress/tests/tc_netem.py).
- **A replica deleted while the actions run:** [`delete_one_replica`](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/alter/stress/tests/stress_alter.py#L403).
- **Pairs of action types:** [the `pairs` scenario](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/alter/stress/tests/stress_alter.py#L445).
- **Network faults:** [the `network_faults` scenario](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/alter/stress/tests/stress_alter.py#L575).

## Slide 23: oracles

- **Compute it another way:** [`plus.py`](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/functions/tests/plus.py#L29-L31).
- **A model:** [rbac `model.py`](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/rbac/tests/multiple_auth_methods/simple_combinatorics/model.py#L19).
- **Invariants:** [the "replicas agree" check](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/alter/stress/tests/stress_alter.py#L346-L361), which uses [`check_consistency`](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/alter/stress/tests/actions.py#L1056).
- **Another implementation:** [`parquet/tests/fastparquet.py`](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/parquet/tests/fastparquet.py#L22-L55). ClickHouse imports and exports the files from another Parquet library's own test suite.
- **Snapshots:** [`functions/tests/snapshots`](https://github.com/Altinity/clickhouse-regression/tree/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/functions/tests/snapshots) and [`parquet/tests/snapshots`](https://github.com/Altinity/clickhouse-regression/tree/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/parquet/tests/snapshots).

## Slide 35: generated data files

- [`generate_parquet_test_files`](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/parquet/data/test_file_generators.py#L63) builds every type with its list, struct and map variants.
- [The loop over 6 compression codecs](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/parquet/data/test_file_generators.py#L205).
