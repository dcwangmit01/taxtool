from __future__ import print_function
import click
from taxtool.cli import pass_context
from taxtool.utils import Utils
import os
import re
import sys

@click.command('receipts', short_help='Process directories of receipts')
@click.argument('path', required=False, type=click.Path(resolve_path=True))
@pass_context
def cli(ctx, path):
    """Turns a directory listing into a CSV"""
    if path is None:
        path = ctx.home
    #ctx.log('Reading directory in %s', click.format_filename(path))

    h = {}
    
    files = os.listdir(path)
    for f in files:

        # yyyy, mm, dd, dollar, cents, business, who, description
        m = re.match('^(return)?_?(\d{4})(\d{2})(\d{2})_(\d+)_(\d+)_(\S+?)_(\S+?)_(.*)\.(\S+?)$', f)

        if m is None:
            print("WARNING: Ignoring file {}", f, file=sys.stderr)
            continue

        filename = f
        refund = True if m.group(1) == "return" else False
        date = m.group(3) + "/" +  m.group(4) + "/" + m.group(2)
        cost = ("" if refund else "-") + m.group(5) + "." + m.group(6)
        business = m.group(7)
        who = m.group(8)
        description = m.group(9)
        extension = m.group(10)

        # stdout csv output
        if True:
            print("{}, {}, {}, {}, {}".format(
                business,
                date,
                f,
                cost,
                who,
            ))
                
        # check
        year_month = m.group(2) + m.group(3)
        dollar = m.group(5)
        cents = m.group(6)
        abs_cost = m.group(5) + "." + m.group(6)
        
        for tup in [(date, dollar), (year_month, abs_cost)]:
            if tup not in h:
                h[tup] = []
            h[tup] += [filename]

    if False:
        print("possible dups")
        for tup in h:
            if len(h[tup]) > 1:
                print("open {}".format(" ".join(h[tup])))


