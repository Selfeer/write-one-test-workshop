# Bug stories for the workshop

Real issues raised by @Selfeer and found by combinatorial tests in clickhouse-regression. Use them on
slide 13 ("bugs live where features meet") or as a closing story.

## 1. One setting × many generated files = 5 bugs in 2 days (Parquet native reader v3)

**In the deck:** slide 24 animates #87412 and #87509.

**Combinatorics:** generated Parquet files (types × shapes × codecs × encodings) × `input_format_parquet_use_native_reader_v3` = 0 / 1.
**Oracle:** the old reader. Each file must give the same type and the same values with the setting off and on
("another implementation" from the oracles slide).

In September 2025, ClickHouse 25.8 added a new Parquet reader behind one setting. The parquet suite already read
many test files (generated ones and files from other Parquet libraries), so turning the setting on for the same files
found these bugs:

| Issue | What happened | Combination |
|---|---|---|
| [#87412](https://github.com/ClickHouse/ClickHouse/issues/87412) | **A Bool column is sometimes true, sometimes false**: run the same SELECT 5–8 times and the values change | Bool × file with enums × reader v3. Fixed in [#87442](https://github.com/ClickHouse/ClickHouse/pull/87442). The maintainer first thought it was already fixed: "EDIT: It was still broken, fixed." |
| [#87509](https://github.com/ClickHouse/ClickHouse/issues/87509) | **Segmentation fault** (server crash) | Bool × bloom filter × gzip × reader v3 |
| [#87396](https://github.com/ClickHouse/ClickHouse/issues/87396) | `Unexpected uncompressed page size` on a file ClickHouse wrote itself | write with ClickHouse → read back × reader v3 |
| [#87413](https://github.com/ClickHouse/ClickHouse/issues/87413) | `Decimal(4, 2)` becomes `Decimal(9, 2)` | Decimal in INT32 physical type × reader v3 |
| [#87469](https://github.com/ClickHouse/ClickHouse/issues/87469) | `DateTime64(3)` becomes `DateTime64(3, 'UTC')` | Timestamp with `isAdjustedToUTC=false` × reader v3 |

All 5 were filed on 22–23 Sep 2025 against 25.8.4.13. All are closed; most were fixed in
[#87600](https://github.com/ClickHouse/ClickHouse/pull/87600) ("More fixes for parquet reader v3, enable it in stateless tests").

**Why it works for the talk:** nobody wrote a test for "Bool with a bloom filter, gzip-compressed, read with the new
reader". The test was "every file, both readers, compare", using files like the generated ones on slide 35.
An older one from the same family, still open: [#72607](https://github.com/ClickHouse/ClickHouse/issues/72607),
where Bool → String gives `true`/`false` with one reader and `1`/`0` with the other.

## 2. 9 codecs × 2 deployments: one cell is empty (s3Cluster + xz)

**Combinatorics:** [`s3/tests/table_function.py`, scenario `auto`](https://github.com/Altinity/clickhouse-regression/blob/5ef901661d878fcbe8a56a57a2f1fb6ce8ec5543/s3/tests/table_function.py#L291-L315)
runs `product(compression_methods, test_clusters)`: 9 compression methods (gzip, gz, deflate, brotli, br, LZMA, xz, zstd, zst)
× single node or each cluster. Each combination writes the value 427 to S3 with one codec, reads it back with
compression `'auto'`, and expects 427.

**Bug:** [#88699](https://github.com/ClickHouse/ClickHouse/issues/88699), still open. Only **xz × s3Cluster on a
3-shard cluster × `auto`** comes back **empty**: no error, just no data. Every other codec works, and xz works on
a single node. It appeared between 25.8.4.13 and 25.8.10, so it is also a regression across versions, the kind
the weekly scheduled runs (slide 12) catch.

**Why it works for the talk:** it's the grid from slide 16 with one red square. No one would write a test for
"xz, through s3Cluster, with auto-detection, on 3 shards" by hand. And the failure is silent: a wrong answer, not
a crash ("a fast wrong answer is worse than a slow right one", slide 10).

## Also possible

- [Altinity/ClickHouse#1218](https://github.com/Altinity/ClickHouse/issues/1218): parallel `EXPORT PARTITION`s, plus
  ALTERs (ADD COLUMN) on another table at the same time, fail with
  `Cannot read all data in MergeTreeReaderCompact. Rows read: 9. Rows expected: 87`. A concurrency example for slide 22.
  Closed.
