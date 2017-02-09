from __future__ import print_function
import click
from taxtool.cli import pass_context
from taxtool.utils import Utils
import os
import re
import sys


@click.command('receipts', short_help='Process directories of receipts')
@click.argument('path', required=False, type=click.Path(resolve_path=True))
@click.option('--no-dup-check', is_flag=True, help="skip the duplicate check")
@pass_context
def cli(ctx, path, no_dup_check):
    """Turns a directory listing into a CSV"""
    if path is None:
        path = ctx.home
    #ctx.log('Reading directory in %s', click.format_filename(path))

    h = {}
    entries = []

    files = os.listdir(path)
    for f in files:

        # optional_return, yyyy, mm, dd, dollar, cents, business, description
        m1 = re.match(
            '^(return)?_?(\d{4})(\d{2})(\d{2})_(\d+)_(\d+)_(\S+?)_(.*)\.(\S+?)$',
            f)

        if m1 is None:
            print("WARNING: Ignoring file {}", f, file=sys.stderr)
            continue

        filename = f
        refund = True if m1.group(1) == "return" else False
        date = m1.group(3) + "/" + m1.group(4) + "/" + m1.group(2)
        cost = ("" if refund else "-") + m1.group(5) + "." + m1.group(6)
        business = m1.group(7)
        extension = m1.group(9)
        description = m1.group(8)
        who_paid = ''
        for_whom = ''

        if business == '41st':
            m2 = re.match('^(\S+?)_(.*)$', description)

            if m2 is None:
                print("WARNING: Ignoring file {}", f, file=sys.stderr)
                continue

            who_paid = m2.group(1)
            for_whom = 'jt'
            description = m2.group(2)

        if business == '537divis':
            m2 = re.match('^(\S+?)_(\S+?)_(.*)$', description)

            if m2 is None:
                print("WARNING: Ignoring file {}", f, file=sys.stderr)
                continue

            who_paid = m2.group(1)
            for_whom = m2.group(2)
            description = m2.group(3)

        # stdout csv output
        if len(entries) == 0:
            entries.append("{}, {}, {}, {}, {}, {}".format(
                'Business',
                'Date',
                'Filename',
                'Cost',
                'Who_Paid',
                'For_Whom', ))

        entries.append("{}, {}, {}, {}, {}, {}".format(
            business,
            date,
            f,
            cost,
            who_paid,
            for_whom, ))

        # save duplicate indentification info for later
        year_month = m1.group(2) + m1.group(3)
        dollar = m1.group(5)
        cents = m1.group(6)
        abs_cost = m1.group(5) + "." + m1.group(6)

        # possible duplicate if
        #   1) date and dollar (not cents) amount are same
        #   2) month and abs cost are same
        for tup in [(date, dollar), (year_month, abs_cost)]:
            if tup not in h:
                h[tup] = []
            h[tup] += [filename]

    # print sorted entries
    for e in sorted(entries):
        print(e)

    # print duplicate checks
    if not no_dup_check:
        print("possible dups")
        for tup in h:
            if len(h[tup]) > 1:
                print("open {}".format(" ".join(h[tup])))
