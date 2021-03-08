from __future__ import print_function
import click
from app.cli import pass_context

import os
import sys
import pandas as pd
import numpy as np

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


@click.command('schwabcsv', short_help='Order and sort Schwab Acccount CSV')
@click.argument('csvfile', required=True, type=click.Path(resolve_path=True))
@pass_context
def cli(ctx, csvfile):
    """order and sort a Schwab Account CSV"""

    df = pd.read_csv(csvfile, skiprows=[0,2,3])

    df[['month', 'day', 'year']] = df['Date'].str.extract(r'(\d{2})/(\d{2})/(\d{4})')
    df['_numerical_date'] = df['year'] + df['month'] + df['day']
    df['date'] = df['month'] + '/' + df['day'] + '/' + df['year']
    df['cost'] = (df['Deposit (+)'].astype(str).replace(r'[\$,]', '', regex=True).astype(float).fillna(0) -
                      df['Withdrawal (-)'].astype(str).replace(r'[\$,]', '', regex=True).astype(float).fillna(0))
    df = df.sort_values(by=['Description', '_numerical_date'])
    df = df.fillna("")  # Fill all NaN with empty string

    columns_in_order = ['year', 'date', 'Description', 'Type', 'cost']
    print(df.to_csv(path_or_buf=None, index=False, columns=columns_in_order))
    print_full(df)
