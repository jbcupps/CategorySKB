def test_home_page(client):
    """Test that home page loads correctly"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to the Particle Physics Explorer' in response.data

def test_modeler_page(client):
    """Test that modeler page loads"""
    response = client.get('/modeler')
    assert response.status_code == 200

def test_analysis_page(client):
    """Test that analysis page loads"""
    response = client.get('/analysis')
    assert response.status_code == 200

def test_tutorial_parameter(client):
    """Test that tutorial parameter is accepted"""
    response = client.get('/modeler?tutorial=true')
    assert response.status_code == 200