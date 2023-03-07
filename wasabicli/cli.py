"""Console script for wasabi S3."""
import sys
import click
from wasabi import ScriptRunner
from formatter import indicators


@click.command()
def main(args=None):
    """Console script for wasabi S3."""
    click.echo(f"{indicators.WARNING}Welcome to the Wasabi S3 CLI Tool{indicators.ENDC}")
    click.echo(f"{indicators.WARNING}--------------------------------------------------------{indicators.ENDC}")
    click.echo(f"{indicators.OKCYAN}@author: M. Salim Dason{indicators.ENDC}")
    click.echo(f"{indicators.OKCYAN}@version: 0.1.4{indicators.ENDC}")
    click.echo(f"{indicators.OKCYAN}@licence: GNU GENERAL PUBLIC LICENSE{indicators.ENDC}")
    click.echo(f"{indicators.FAIL}Note: Tool specifically designed for versioned buckets!{indicators.ENDC}")
    click.echo(f"{indicators.WARNING}---------------------------------------------------------{indicators.ENDC}\n")

    ScriptRunner().start()


if __name__ == "__main__":
    # main()
    sys.exit(main())
