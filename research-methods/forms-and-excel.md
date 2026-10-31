# Google Forms and Excel: documented workflow

**Maintainer:** John Quinn, MD, MPH, PhD, EMT-P  
**Version:** 0.2.0 · **Updated:** 31 October 2026  
**Status:** original portfolio demonstration; synthetic records only.

## Form and export specification

Use the activity options and rating anchors in [instruments.md](instruments.md). Make Not applicable explicit and keep comments optional. Map that response to text NA; leave a skipped item blank; retain ratings as integers 1-5. The [dictionary](data-dictionary.csv) and [missingness example](missingness-example.csv) use this same convention. NA is not the spreadsheet error #N/A.

Confirm email collection, login restrictions and access settings against the approved protocol. Keep a dated raw export in restricted storage, use a separate testing destination and document every transformation in a cleaning log. Check identifiers, duplicates, activity categories, integer bounds and missingness before analysis. Unexpected values require resolution rather than silent deletion.

## Excel example

Open [synthetic-survey.csv](synthetic-survey.csv). Columns A-D are response_id, activity, usefulness and confidence; rows 2-9 contain eight invented records. Run the [reproducible checker](analyze_survey.py) first; the formulas below assume its validation has passed.

| Calculation | Formula | Expected result |
|---|---|---|
| Records | =COUNTA(A2:A9) | 8 |
| Valid usefulness ratings | =COUNTIFS(C2:C9,">=1",C2:C9,"<=5") | 8 |
| Ratings 4-5 | =COUNTIFS(C2:C9,">=4",C2:C9,"<=5") | 5 |
| Proportion rating 4-5 | =IFERROR(COUNTIFS(C2:C9,">=4",C2:C9,"<=5")/COUNTIFS(C2:C9,">=1",C2:C9,"<=5"),"Not applicable") | 62.5% |
| Skipped confidence ratings | =COUNTBLANK(D2:D9) | 1 |
| Not-applicable confidence ratings | =COUNTIF(D2:D9,"NA") | 0 |
| Median usefulness | =MEDIAN(C2:C9) | 4 |

In the separate three-record missingness example, usefulness has one valid rating, one NA and one skipped value. Confidence has two valid ratings, one NA and no skipped values. Neither NA nor blanks enter a valid-rating denominator. Formula separators vary by locale. For a growing dataset, use an Excel Table and update references.

The [worked analysis](worked-analysis.md) reports all five rating categories, subgroup denominators and limitations. Eight invented records cannot support real-world claims. A live research dataset belongs in approved private storage.
