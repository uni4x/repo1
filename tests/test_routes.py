def test_home_page(test_client):
    response = test_client.get("/main", follow_redirects=True)
    assert response.status_code == 200
    assert b"search.html" in response.data
