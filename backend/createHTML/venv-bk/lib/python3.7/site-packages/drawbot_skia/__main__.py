import argparse
import sys
from .drawing import Drawing
from .runner import makeDrawbotNamespace, runScriptSource


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="drawbot",
        description="Command line DrawBot tool.",
    )
    parser.add_argument(
        "drawbot_script",
        type=argparse.FileType("r"),
        help="The Drawbot script to run.",
    )
    parser.add_argument(
        "output_file",
        nargs="*",
        default=[],
        help="A filename for the output graphic.",
    )

    arguments = parser.parse_args(args)
    db = Drawing()
    namespace = makeDrawbotNamespace(db)
    runScriptSource(arguments.drawbot_script.read(), arguments.drawbot_script.name, namespace)
    for path in arguments.output_file:
        db.saveImage(path)


if __name__ == "__main__":
    main()
