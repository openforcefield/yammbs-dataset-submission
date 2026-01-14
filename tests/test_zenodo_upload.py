import random
import string
import subprocess
import os

import requests


def test_basic_upload(capsys):
    """Test that zenodo_upload.py can upload a file to a sandbox Zenodo instance and return the record ID."""
    title = "".join([string.ascii_lowercase[random.randint(0, 25)] for _ in range(16)])

    random_file_name = f"{random.randint(0, 100)}.txt"

    with open(random_file_name, "w") as f:
        f.write("BLAH")

    result = subprocess.run(
        ["python", "zenodo_upload.py", "--title", title, random_file_name],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, f"Script failed with stderr: {result.stderr}"

    # rstrip is necessary, otherwise a trailing newline breaks URLs
    deposition_id = result.stdout.rstrip()

    # the record must be "published" to be retrievable, normally we do this manually but
    # an automated tests requires this be done automatically
    post_response = requests.post(
        f"https://sandbox.zenodo.org/api/deposit/depositions/{deposition_id}/actions/publish",
        headers={"Authorization": f"Bearer {os.environ['ZENODO_TOKEN']}"},
    )

    assert post_response.status_code < 400, post_response.json()

    get_response = requests.get(f"https://sandbox.zenodo.org/api/records/{deposition_id}")

    assert get_response.json()["metadata"]["title"] == title

    assert len(get_response.json()["files"]) == 1

    assert get_response.json()["files"][0]["key"] == random_file_name
