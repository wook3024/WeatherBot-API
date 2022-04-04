import argparse

from alive_progress import alive_bar
from httpx import Client
from rich.console import Console

console = Console()


def run():
    with Client() as client:
        response = client.get(url="http://localhost:8000/livez")
    console.log("Status code: {}".format(response.status_code))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=1)
    args = parser.parse_args()

    with alive_bar(args.count, title="Eval") as bar:
        for _ in range(args.count):
            run()
            bar()
