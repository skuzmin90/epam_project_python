from app import app

def test_index():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200

def test_results():
    client = app.test_client()
    response = client.get('/results')
    assert response.status_code == 200

def test_remove():
    client = app.test_client()
    response = client.get('/remove')
    assert response.status_code == 200

def test_update():
    client = app.test_client()
    response = client.get('/update')
    assert response.status_code == 200