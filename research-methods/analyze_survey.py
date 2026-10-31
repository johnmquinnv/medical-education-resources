#!/usr/bin/env python3
"""Validate the published synthetic survey and report transparent denominators.

SPDX-License-Identifier: MIT
"""
import argparse
import csv
import io
import json
from pathlib import Path
from statistics import median

ACTIVITIES = {'simulation', 'case_discussion', 'reading'}
RATINGS = {'1', '2', '3', '4', '5'}
FIELDS = ['response_id', 'activity', 'usefulness', 'confidence']


def analyze(stream):
    reader = csv.DictReader(stream)
    if reader.fieldnames != FIELDS:
        raise ValueError('Expected columns: ' + ', '.join(FIELDS))
    rows = list(reader)
    ids = set()
    for line, row in enumerate(rows, 2):
        if None in row or any(v is None for v in row.values()):
            raise ValueError(f'Line {line}: inconsistent number of columns')
        if not row['response_id'] or row['response_id'] in ids:
            raise ValueError(f'Line {line}: missing or duplicate identifier')
        ids.add(row['response_id'])
        if row['activity'] not in ACTIVITIES:
            raise ValueError(f'Line {line}: invalid activity')
        for field in ['usefulness', 'confidence']:
            if row[field] not in RATINGS | {'NA', ''}:
                raise ValueError(f'Line {line}: invalid {field}; use 1-5, NA or blank')

    def summarize(values):
        valid = [int(v) for v in values if v in RATINGS]
        high = sum(v >= 4 for v in valid)
        return {
            'valid': len(valid), 'skipped': values.count(''),
            'not_applicable': values.count('NA'),
            'distribution': {str(v): valid.count(v) for v in range(1, 6)},
            'median': median(valid) if valid else None,
            'ratings_4_5': high,
            'proportion_4_5': high / len(valid) if valid else None,
        }

    return {
        'records': len(rows),
        'usefulness': summarize([r['usefulness'] for r in rows]),
        'confidence': summarize([r['confidence'] for r in rows]),
        'by_activity': {a: summarize([r['usefulness'] for r in rows if r['activity'] == a])
                        for a in sorted(ACTIVITIES)},
    }


def self_test():
    header = ','.join(FIELDS) + '\n'
    summary = analyze(io.StringIO(header + 'E001,simulation,5,4\nE002,reading,NA,\n'))
    assert summary['usefulness']['valid'] == 1
    assert summary['usefulness']['not_applicable'] == 1
    assert summary['confidence']['skipped'] == 1
    empty = analyze(io.StringIO(header + 'E001,reading,NA,\n'))
    assert empty['usefulness']['proportion_4_5'] is None
    for bad in ['0', '6', '2.5', 'N/A', 'unknown']:
        try:
            analyze(io.StringIO(header + f'E001,reading,{bad},4\n'))
        except ValueError:
            pass
        else:
            raise AssertionError(f'Accepted invalid value: {bad}')
    for badrows in ['E001,reading,3,4\nE001,reading,4,4\n',
                    'E001,unknown,3,4\n', ',reading,3,4\n']:
        try:
            analyze(io.StringIO(header + badrows))
        except ValueError:
            pass
        else:
            raise AssertionError('Accepted invalid identifiers or activity')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file', nargs='?', type=Path, default=Path(__file__).with_name('synthetic-survey.csv'))
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    if args.self_test:
        self_test()
    with args.file.open(newline='', encoding='utf-8') as stream:
        print(json.dumps(analyze(stream), indent=2))
