import json


def test_add_manifest(test_app):
    req_payload = {
        "type": "csv",
        "originator": "Andrew",
        "agent": "Jason",
        "md5": "123a-sd222d",
        "filename": "file.csv",
        "filesize": 4000
    }
    response = test_app.post("/manifest", content=json.dumps(req_payload))
    assert response.status_code == 201