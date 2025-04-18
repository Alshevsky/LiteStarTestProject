import os
import sys
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from alembic.config import CommandLine, Config

def main():
    alembic = CommandLine()
    options = alembic.parser.parse_args()
    if not hasattr(options, "cmd"):
        alembic.parser.error("too few arguments")
    else:
        config = Config(
            file_=options.config,
            ini_section=options.name,
            cmd_opts=options
        )
        alembic.run_cmd(config, options)

if __name__ == "__main__":
    main()
