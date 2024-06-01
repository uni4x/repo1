# def test_register_and_login(test_client):
#     # Register a new user
#     response = test_client.post('/auth/register', data={
#         'username': 'testuser',
#         'password': 'password',
#         'password2': 'password'
#     }, follow_redirects=True)
#     assert response.status_code == 200
#     assert b"Congratulations, you are now a registered user!" in response.data

#     # Log in with the new user
#     response = test_client.post('/auth/login', data={
#         'username': 'testuser',
#         'password': 'password'
#     }, follow_redirects=True)
#     assert response.status_code == 200
#     assert b"Welcome, testuser!" in response.data

#     # Log out
#     response = test_client.get('/auth/logout', follow_redirects=True)
#     assert response.status_code == 200
#     assert b"You have been logged out." in response.data