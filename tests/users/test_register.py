def test_get_all(client):
    response = client.get("/user/all")
    return response

