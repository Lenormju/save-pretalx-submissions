# Fetch Pretalx talks submissions to an event

Given the event id (slug), fetches and saves to disk all the data from the talks submitted to this event.
Requires an API token, get yours on [`pretalx[.yourdomain].com/orga/me`](https://pretalx.com/orga/me) (notice no leading slash).

Run with [`uv`](https://docs.astral.sh/uv/) : `uv run fetch_pretalx_submissions.py`
