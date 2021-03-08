from __future__ import print_function
import click
from app.cli import pass_context

import os
import sys
import pandas as pd


def print_full(x):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.float_format', '{:20,.2f}'.format)
    pd.set_option('display.max_colwidth', None)
    print(x, file=sys.stderr)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.float_format')
    pd.reset_option('display.max_colwidth')


@click.command('receipts', short_help='Process directories of receipts')
@click.argument('path', required=False, type=click.Path(resolve_path=True))
@click.option('--no-dup-check', is_flag=True, help="skip the duplicate check")
@pass_context
def cli(ctx, path, no_dup_check):
    """Turns a directory listing into a CSV"""
    if path is None:
        path = ctx.home

    files = os.listdir(path)
    df = pd.DataFrame(files, columns=['filename'])
    df['refund'] = df.filename.str.match(r'refund')
    df['_filename_wo_refund'] = df.filename.str.replace('refund_', '')
    df[[
        'business', 'year', 'month', 'day', 'cost', 'paid_by', 'paid_for', 'vendor', 'description'
    ]] = df['_filename_wo_refund'].str.extract(
        r'(\w+?)_(\d{4})(\d{2})(\d{2})_(\d+\.\d{2})(?:_pb#([a-zA-Z0-9]*))?(?:_pf#([a-zA-Z0-9]*))?_(.*?)_(.*)(?:\.\w{3})'
    )
    df['_numerical_date'] = df['year'] + df['month'] + df['day']
    df['date'] = df['month'] + '/' + df['day'] + '/' + df['year']
    df['vendor_description'] = df['vendor'] + '_' + df['description']
    df['cost'] = df.apply(lambda x: 0 - float(x['cost']) if not x['refund'] else float(x['cost']), axis=1)
    df = df.drop('_filename_wo_refund', axis=1)
    df = df.fillna("")  # Fill all NaN with empty string

    df = df.sort_values(by=['business', '_numerical_date', 'vendor_description'])

    # Create Verifications
    h = {}
    ignore_files = []
    for idx, row in df.iterrows():

        if not (row['business'] and row['year'] and row['month'] and row['day'] and row['cost'] and row['vendor']
                and row['description']):
            ignore_files.append(row['filename'])
            continue

        year_month = row['year'] + row['month']
        abs_cost = abs(row['cost'])
        date = row['date']
        dollar = int(abs_cost)

        # possible duplicate if
        #   1) date and dollar (not cents) amount are same
        #   2) month and abs cost are same
        for tup in [(year_month, abs_cost), (date, dollar)]:
            if tup not in h:
                h[tup] = []
            h[tup] += [row['filename']]

    columns_in_order = ['year', 'business', 'date', 'vendor_description', 'cost', 'paid_for', 'paid_by', 'filename']
    print(df.to_csv(path_or_buf=None, index=False, columns=columns_in_order))

    print_full(df)

    # print duplicate checks
    if not no_dup_check:
        print("#####################################################################\nPOSSIBLE DUPLICATES",
              file=sys.stderr)
        for tup in h:
            if len(h[tup]) > 1:
                print("open {}".format(" ".join(h[tup])), file=sys.stderr)

    if True:
        print("#####################################################################\nIGNORING FILES",
              file=sys.stderr)
        print("\n".join(ignore_files), file=sys.stderr)
