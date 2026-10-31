# Worked analysis: a synthetic learning survey

**Author:** John Quinn · **Version:** 0.2.0 · **Updated:** 31 October 2026

## Question and source

Which activities do the eight invented respondents rate as useful? This exercise uses [synthetic-survey.csv](synthetic-survey.csv), not research participants. The [analysis script](analyze_survey.py) validates the dictionary and reproduces the counts below with Python's standard library.

## Cleaning and denominator decisions

All eight identifiers are unique. Activity values match the three allowed categories. Usefulness has eight valid integer ratings; confidence has seven valid ratings and one skipped item (S007). Neither field contains Not applicable in the main sample. The separate [missingness example](missingness-example.csv) demonstrates text NA versus a skipped blank. No imputation or recoding to zero is applied.

| Usefulness rating | Count | Denominator | Percentage |
|---|---|---|---|
| 1 | 0 | 8 | 0% |
| 2 | 1 | 8 | 12.5% |
| 3 | 2 | 8 | 25% |
| 4 | 3 | 8 | 37.5% |
| 5 | 2 | 8 | 25% |

Five of eight valid usefulness ratings are 4-5 (62.5%); the median is 4. Confidence has median 4 among seven valid ratings, one skipped item and no NA responses. Confidence describes self-report and does not measure competence.

| Activity | Valid usefulness ratings | Ratings 4-5 | Percentage |
|---|---|---|---|
| Simulation | 4 | 4 | 100% |
| Case discussion | 2 | 1 | 50% |
| Reading | 2 | 0 | 0% |

## Interpretation and decision

The invented distribution illustrates how an overall summary can conceal differences between small groups. It does not show that simulation causes better learning, that any activity improves clinical outcomes, or that the sample represents a wider population. The groups were invented, are unequal and have no allocation mechanism or baseline comparison. No hypothesis test is justified for this teaching exercise.

For a real pilot, the next decision would be whether the instrument is understandable and the export preserves response categories. Collect pilot feedback, examine missingness and test the cleaning workflow before interpreting activity ratings. Document revisions and obtain the required local governance determination.

## Reproduce

Run: python3 research-methods/analyze_survey.py

The script rejects duplicate identifiers, invalid categories and values outside integer ratings 1-5, NA or blank. Its JSON output separates valid, skipped and not-applicable responses. Run it again after changing the CSV or dictionary convention.
