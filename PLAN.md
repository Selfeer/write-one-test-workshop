# Write one test, break a thousand ways: workshop plan (60 min)

Deck: `workshop/index.html`. Open it in any browser; it works offline (fonts and logo are embedded).
Keys: → / Space / clicker = next step, ← = back, T = light theme
(use it in bright rooms), F = fullscreen. `index.html#15` opens slide 15; `index.html?light` starts in the light theme.

Editing: change `src/deck.html`, then run `python3 workshop/build.py` to regenerate `index.html`.
Branding follows the GeoSTQB brand book: #111111 black, #1E4DFC blue, #839CFE light blue, #1EFCD0 mint,
the Metropolis typeface (SIL Open Font License, in `src/fonts/`), the logo (`src/brand/`), and the dot pattern.

## Running order

| Time | Block | Slides | What the audience does |
|---|---|---|---|
| 0:00–0:02 | Opening + agenda | 1–2 | Show of hands: tests? SQL? ClickHouse? |
| 0:02–0:10 | **What ClickHouse is, and why it's fast** | 3–7 | Watch: OLTP vs OLAP, row vs column, compression, cores and shards |
| 0:10–0:17 | **What we test, and why** | 8–14 | Typical QA vs describing the whole space (slide 9); see the weekly CI runs (slide 12); name things that could vary in a test (slide 14) |
| 0:17–0:32 | **Combinatorics** | 15–24 | Watch the counts grow; discuss which combinations to choose; two real bugs (slide 24) |
| 0:32–0:47 | **Hands-on: fiddle.clickhouse.com** | 25–31 | Predict each result, then run it |
| 0:47–0:57 | **Real suite demo** | 32–35 | Watch `plus.py` run; suggest a value to add |
| 0:57–1:00 | Recipe + Q&A | 36–37 | |

## Hands-on exercises (all checked on ClickHouse 26.3)

Each one teaches one idea. Predicting before running is the point.

Slide 27 explains `values()` before anyone types: it builds A and B as small tables, then pairs every row
of A with every row of B, one result row at a time.

1. `toUInt8(200) + toUInt8(100)`: the answer is **300 (UInt16)**, because adding widens the type. *One test, one fact.*
2. Cross join of two `values()` lists: **4 × 4 = 16 rows**. Adding `200` to both gives 25; adding a third
   table `values('c UInt8', 1, 2)` gives **50 rows, and `a + b + c` becomes UInt32**. *A cross join is `itertools.product`.*
3. UInt64 plus a UInt256 oracle column: **3 of 9 rows fail**, because max + 1 wraps to 0. *The oracle was wrong, not ClickHouse; the spec decides.*
4. Float specials: `inf + -inf = nan`, `0.1 + 0.2 = 0.30000000000000004`, `nan = nan` is false. *The oracle needs its own definition of "same".*
5. `intDiv(minInt64, -1)` throws, and the whole query returns nothing. *That's why each combination runs as its own test.*

Gotcha found while building these: `SELECT arrayJoin(v) AS a, arrayJoin(v) AS b` gives a **zip, not a product**.
ClickHouse merges the identical expressions. That's why the exercises use `values(...) AS A, values(...) AS B`.

## Demo prep (the day before)

- `docker pull altinity/clickhouse-server:25.8.14.20001.altinityantalya` and the images in `functions/functions_env`.
- Do one full run of `cd functions && ./regression.py --local --clickhouse docker://… --only "/functions/plus/*"`.
- Record a terminal run as a backup in case the Wi-Fi or Docker fails.
- Live moment: add `"18446744073709551615"` (the largest UInt64) to `value` in `plus.py`. The count goes from
  1,089 to 1,296 (36 × 36) and **4 tests fail**: max + max stays UInt64 in ClickHouse and wraps to
  18446744073709551614, while the Python float oracle expects 3.7e19 (checked with clickhouse-local 26.3).
  Don't use a negative value such as `"-0.0"`: the `-` sign would make it `--0.0`, which SQL reads as a comment.

## Suites the deck refers to (numbers checked against the code)

- `functions/tests/plus.py`: 3 signs × 11 values per operand = 33² = **1,089** scenarios.
- `rbac/tests/multiple_auth_methods/simple_combinatorics`: 15 create ways × 31³ alter ways = **446,865** sequences.
  Each run samples 3,000 with `random.seed(42)`, 10 in parallel. All of them run with `--stress`. `model.py` is the oracle.
- `alter/stress/tests/stress_alter.py`: `combinations(actions, 3, with_replacement=True)`, shuffled, run in parallel,
  with `tc_netem` network faults. The check is that all replicas agree.
- `parquet/data/test_file_generators.py`: types × nesting × 6 compression codecs → Parquet files.
- 44 suites, about 2,100 Python files, about 600k lines.
- Scheduled CI (slide 12, from the README and `.github/workflows/scheduled-*.yml`): 13 versions. head runs Tue + Thu 00:00 UTC
  in 4 setups (x86/arm64 × ZooKeeper/Keeper); the other 12 run Saturday 22:00 UTC as 15 jobs. That's 23 full regressions a week.
  The pass/fail badges on the slide are a snapshot of the README on 2026-11-26; update them before the workshop.

## Open items to decide together

- [ ] One or two **real bug stories** for slide 13 ("bugs live where features meet"). This matters most.
- [ ] Is 15 minutes of hands-on right if most people have no laptop? Plan B: you type, they guess.
- [ ] A pairwise or covering-array exercise? (`testflows.combinatorics.CoveringArray` could run live.)
- [ ] A concurrency demo you can run live, or keep it to the animation on slide 22?
- [ ] QR code for fiddle.clickhouse.com and the repo (needs generating; the deck has no external dependencies).
