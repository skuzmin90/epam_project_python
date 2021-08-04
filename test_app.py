from app import app

def test_index():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_results():
    client = app.test_client()
    request =  client.post('/results', data={"select": "2021-08-01"})
    response = client.get('/results', data={"select": "2021-08-01"})
    assert request.status_code == 200
    assert response.status_code == 200
