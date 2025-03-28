# adapted from https://developers.zenodo.org/?python#quickstart-upload

import argparse
import json
import logging
import os

import requests
from requests.exceptions import JSONDecodeError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument("--title", "-t")
parser.add_argument("files", nargs="+")

URL = os.environ["ZENODO_URL"]
TOKEN = os.environ["ZENODO_TOKEN"]

HEADERS = {"Authorization": f"Bearer {TOKEN}"}


def check_status(response, expect) -> bool:
    "Helper for checking that ``response.status_code`` matches ``expect``."
    if response.status_code != expect:
        try:
            body = response.json()
        except JSONDecodeError as e:
            body = e
        msg = f"Request failed ({response.status_code}), body: {body}"
        logger.error(msg)
        return False

    return True


def check_api_access(url, headers):
    logger.info("checking API access")
    r = requests.get(f"{url}/api/deposit/depositions", headers=headers)
    return check_status(r, 200)


def create_empty_upload(url, headers):
    logger.info("creating an empty upload")
    r = requests.post(
        f"{url}/api/deposit/depositions",
        json={},
        headers=headers | {"Content-Type": "application/json"},
    )
    if not check_status(r, 201):
        return False
    return r.json()


def upload_file(bucket_url, filename, headers) -> bool:
    "Upload a file and return whether this succeeded or not"

    logger.info(f"uploading file: `{filename}`")

    if not os.path.exists(filename):
        logger.error(f"provided filename `{filename}` does not exist")
        return

    with open(filename, "rb") as f:
        path = os.path.basename(filename)
        r = requests.put(f"{bucket_url}/{path}", data=f, headers=headers)
        return check_status(r, 201)


def add_metadata(deposition_id, url, headers, title):
    logger.info("updating metadata")
    description = (
        "Generated by yammbs-dataset-submission: "
        "https://github.com/openforcefield/yammbs-dataset-submission"
    )
    data = {
        "metadata": {
            "title": title,
            "upload_type": "dataset",
            "description": description,
            "creators": [{"name": "OpenFF, YDS", "affiliation": "OMSF"}],
        }
    }
    r = requests.put(
        f"{URL}/api/deposit/depositions/{deposition_id}",
        headers=headers | {"Content-Type": "application/json"},
        data=json.dumps(data),
    )
    return check_status(r, 200)


def with_retries(fn, retries):
    "Run ``fn`` up to ``retries`` times or until it returns something truthy"
    finished = False
    while not finished and retries > 0:
        finished = fn()
        retries -= 1
    return finished


def main():
    args = parser.parse_args()

    if not with_retries(lambda: check_api_access(URL, HEADERS), 5):
        logger.error("No API access, exiting")
        exit(1)

    if not (res := with_retries(lambda: create_empty_upload(URL, HEADERS), 5)):
        logger.error("Failed to create empty upload, exiting")
        exit(1)

    bucket_url = res["links"]["bucket"]
    deposition_id = res["id"]

    for f in args.files:
        with_retries(lambda: upload_file(bucket_url, f, HEADERS), 5)

    with_retries(
        lambda: add_metadata(deposition_id, URL, HEADERS, title=args.title), 5
    )


if __name__ == "__main__":
    main()
