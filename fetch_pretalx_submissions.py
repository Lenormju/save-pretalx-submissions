"""
Given the event id (slug), fetches and saves to disk all its submitted talks' data.

Requires an API token, get yours on `https://pretalx[.yourdomain].com/orga/me`.
"""
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "requests",
# ]
# ///

# uv run ruff format fetch_pretalx_submissions.py
# uv run ruff check --select ALL --ignore D203 --ignore D212 fetch_pretalx_submissions.py
# uv tool run --with types-requests mypy fetch_pretalx_submissions.py

import json
import sys
import time
import traceback
from pathlib import Path

import requests


def download_and_save_submissions(
    *,
    event_id: str,
    token: str,
    pretalx_server_domain: str,
    savefile_path: Path,
) -> None:
    """Iterate over all submissions and save them into a file."""
    get_event_submissions_url = (
        f"https://{pretalx_server_domain}/api/events/{event_id}/submissions"
    )
    all_submissions = []
    while True:
        print(f"Fetching submissions {get_event_submissions_url}")  # noqa: T201
        try:
            response = requests.get(
                get_event_submissions_url,
                headers={"Authorization": f"Token {token!s}"},
                timeout=10,
            )
        except requests.RequestException:  # noqa: TRY203
            raise
        else:
            if response.status_code == requests.codes.ok:  # 200
                try:
                    all_submissions.extend(response.json()["results"])
                except (IndexError, ValueError, TypeError):  # noqa: TRY203
                    raise
                else:
                    get_event_submissions_url = response.json()["next"]
                    if get_event_submissions_url is None:
                        break
                    else:  # noqa: RET508
                        time.sleep(5)
            else:
                http_error_msg = f"HTTP Error: {response.status_code} {response.reason}"
                raise RuntimeError(http_error_msg)

    try:
        savefile_path.write_text(json.dumps(all_submissions, indent=2, sort_keys=True))
    except OSError:  # noqa: TRY203
        raise


def main() -> int:
    """
    Run the script as a process main function.

    Handles commandline arguments, configuration, logging and catching exceptions.
    """
    pretalx_server_domain = "pretalx.com"
    token = Path("MY_TOKEN.txt").read_text().strip()
    event_id = "europython-2025"
    savefile_path = Path("europython_talks.json")
    try:
        download_and_save_submissions(
            event_id=event_id,
            token=token,
            pretalx_server_domain=pretalx_server_domain,
            savefile_path=savefile_path,
        )
    except BaseException:  # noqa: BLE001
        traceback.print_exc()
        return 2
    else:
        return 0


if __name__ == "__main__":
    sys.exit(main())
