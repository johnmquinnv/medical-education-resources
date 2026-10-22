# Google Forms and Excel: documented workflow

**Maintainer:** John Quinn, MD, MPH, PhD, EMT-P  
**Version:** 0.1.0 · **Updated:** 22 October 2026  
**Status:** original portfolio demonstration; not a validated instrument or approved operational policy. Synthetic examples only.

This is a workflow specification, not a claim that a live Form or workbook has been deployed.

## Form specification

Use the activity options and rating anchors in [instruments.md](instruments.md). Make “not applicable” explicit and keep comments optional. Confirm email collection, login restrictions and access settings against the approved protocol. Use a separate response destination for testing; remove synthetic tests from a real study dataset before launch.

## Export and clean

1. Preserve a dated raw export in restricted storage; never overwrite it.
2. Make a working copy and record each transformation in a cleaning log.
3. Apply the [data dictionary](data-dictionary.csv): valid categories, numeric bounds and missing values.
4. Resolve duplicates using a prespecified rule, rather than deleting inconvenient observations.
5. Keep a versioned analysis file and record software versions and analyst decisions.

## Excel example

Open [synthetic-survey.csv](synthetic-survey.csv) in Excel. Columns A–D are response_id, activity, usefulness and confidence; rows 2–9 contain the eight invented records.

| Calculation | Formula | Expected result |
|---|---|---|
| Records | =COUNTA(A2:A9) | 8 |
| Valid usefulness ratings | =COUNT(C2:C9) | 8 |
| Ratings 4–5 | =COUNTIF(C2:C9,">=4") | 5 |
| Proportion rating 4–5 | =COUNTIF(C2:C9,">=4")/COUNT(C2:C9) | 62.5% |
| Missing confidence ratings | =COUNTBLANK(D2:D9) | 1 |
| Median usefulness | =MEDIAN(C2:C9) | 4 |

Formula separators vary by locale. The denominator is valid usefulness responses, not automatically everyone invited. For a live growing dataset, convert the data to an Excel Table and update formulas accordingly. Inspect a frequency table for all five rating categories before drawing conclusions. Eight invented records cannot support real-world claims.
