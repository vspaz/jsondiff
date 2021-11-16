import json

from jsondiff import cli
from jsondiff import difference


def main():
    args = cli.get_args()
    file1 = json.loads(args.file1)
    file2 = json.loads(args.file2)
    cfg = json.loads(args.config)

    d = difference.JsonDiff(config=cfg)
    d.find_diff(one=file1, two=file2, diff=d.diff)
    print(d.get_diff())


if __name__ == "__main__":
    main()
