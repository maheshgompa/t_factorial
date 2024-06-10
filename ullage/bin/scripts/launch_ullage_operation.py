import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

import click
import datetime

from rich.console import Console
from bin.ullage.ullage_operation import UllageONOFFOperation


def create_date(date_str):
    if date_str == 'yesterday':
        date = datetime.date.today()
        date = date - datetime.timedelta(1)
    else:
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
        except:
            raise click.UsageError('date argument is not valid')

    return date


@click.group()
def subcommands():
    pass


@click.command()
@click.argument('date_str', required=True)
def process(date_str):
    # {{{
    """
    Process data for the selected day to calculate on off conditions

    Ej:
    python launch_ullage_on_off.py process 2023-4-30
    """

    selected_date = create_date(date_str)

    # Instantiate UllageONOFFOperation class with final_df
    ullage_operation = UllageONOFFOperation()
    click.echo()

    ullage_operation.process(selected_date, update_database=True)


@click.command()
@click.argument('date_str', required=True)
def check(date_str):
    # {{{
    """
    Process data for the selected day to calculate on off conditions

    Ej:
    python launch_ullage_on_off.py process 2023-4-30
    """

    selected_date = create_date(date_str)

    ullage_operation = UllageONOFFOperation()
    click.echo()
    ullage_operation.check(selected_date, update_database=False)


subcommands.add_command(process)
subcommands.add_command(check)

if __name__ == '__main__':
    subcommands()
