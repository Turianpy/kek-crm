def check_pagination(response, limit=None):
    for field in ['count', 'next', 'previous', 'results']:
        assert field in response.data

    assert len(response.data['results']) <= 10 if not limit else limit
