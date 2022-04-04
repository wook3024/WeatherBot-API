import time
import random
import argparse
from httpx import Client
from rich.console import Console
from alive_progress import alive_bar


console = Console()
timeout_count = 0
min_value = -90
max_value = 90


def elapsed_time(fn):
    def inner(*args, **kwargs):
        start_time = time.time()
        to_execute = fn(*args, **kwargs)
        end_time = time.time()
        process_time = end_time - start_time
        console.log("{0} process time: {1:.8f}s".format(fn.__name__, process_time))
        return to_execute

    return inner


@elapsed_time
def run():
    with Client() as client:
        response = client.get(
            url="http://localhost:8000/summary", 
            params={
                "lat": random.randrange(min_value,max_value), 
                "lon": random.randrange(min_value,max_value)
            }
        )
    if response.status_code != 200:
        global timeout_count
        timeout_count += 1
    console.log("Status code: {}".format(response.status_code))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=50)
    args = parser.parse_args()

    with alive_bar(args.count, title="Eval") as bar:
        for _ in range(args.count):
            run()
            bar()
    console.log("Count: {}, Timeout ratio: {}".format(args.count, timeout_count / args.count))
