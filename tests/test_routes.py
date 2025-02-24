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

def test_test_skb_route(client):
    """Test that the /test_skb route works correctly"""
    data = {
        'particle_name': 'proton',
        'twist_numbers': [2, 2, -1],
        'linking_pairs': [(0, 1, 1), (1, 2, 1), (0, 2, 1)]
    }
    response = client.post('/test_skb', json=data)
    assert response.status_code == 200
    assert 'predicted_charge' in response.json
    assert 'predicted_mass' in response.json
