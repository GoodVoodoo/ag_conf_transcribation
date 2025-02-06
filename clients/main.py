import sys

import click
import urllib3
from urllib3.exceptions import InsecureRequestWarning

from clients import asr
from clients.common_utils.config import create_config

# NB (k.zhovnovatiy): Disable warning from unsafe Keycloak connection (--verify-sso false)
urllib3.disable_warnings(InsecureRequestWarning)


@click.group()
def main() -> None:
    pass


@click.group(
    "recognize",
    help="Speech Recognition commands",
)
def asr_group() -> None:
    pass


@click.group(
    "models",
    help="Model info retrieval commands",
)
def models_group() -> None:
    pass


asr_group.add_command(asr.file_recognize, "file")
asr_group.add_command(asr.recognize, "stream")

models_group.add_command(asr.get_models_info, "recognize")

main.add_command(asr_group)
main.add_command(models_group)
main.add_command(create_config, "create-config")


if __name__ == "__main__":
    sys.exit(main())
