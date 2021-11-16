import json

from jsondiff import cli
from jsondiff import difference


def main():
    args = cli.get_args()
    file1 = json.loads(args.file1)
    file2 = json.loads(args.file2)
    cfg = json.loads(args.config)

    jd = difference.JsonDiff(config=cfg)
    jd.find_diff(one=file1, two=file2, diff=jd.diff)
    print(jd.get_diff())


if __name__ == "__main__":
    main()
