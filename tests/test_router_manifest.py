import json


def test_add_manifest(test_app):
    req_payload = {
        "guid": "079bb2a2-2cb7-4a3d-9d33-abae233d5527",
        "type": "csv",
        "originator": "Andrew",
        "agent": "Jason",
        "md5": "93eeb21b251ecccaf936b45dd7c3ef82",
        "filename": "file.csv",
        "filesize": 4000,
        "bucket_guid": "7e80e647-b98b-457c-b807-96cf1dd589e3"
    }
    response = test_app.post("/manifest", content=json.dumps(req_payload))
    assert response.status_code == 201