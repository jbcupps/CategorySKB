import pytest
import json
from src.errors import ValidationError

def test_validate_skb_empty_data(client):
    response = client.post('/skb/validate', 
                         data=json.dumps({}),
                         content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'No data provided'

def test_analyze_skb_empty_data(client):
    response = client.post('/skb/analyze',
                         data=json.dumps({}),
                         content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'No data provided'

def test_integrate_quark_empty_data(client):
    response = client.post('/skb/integrate',
                         data=json.dumps({}),
                         content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == 'No data provided' 