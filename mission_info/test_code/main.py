import argparse
import subprocess


def get_git_diff():
    result = subprocess.run(
        ["git", "diff", "--staged"],
        capture_output=True,
        text=True,
        check=True
    )

    return result.stdout


parser = argparse.ArgumentParser()

# 위치 인자, 위치인자 하나만 받고 commit, pr 둘 중 하나여야 합니다.
parser.add_argument(
    "command",
    choices=["commit", "pr"]
)

args = parser.parse_args()

diff = get_git_diff()

if args.command == "commit":
    print("커밋 메시지 생성")
    print(diff)

elif args.command == "pr":
    print("PR 설명 생성")
    print(diff)