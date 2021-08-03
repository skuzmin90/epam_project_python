from app import app

def test_index():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_results():
    client = app.test_client()
    response = client.post('/results', select = json.dumps('2021-08-01'))
    assert response.status_code == 200

