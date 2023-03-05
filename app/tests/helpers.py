

def login(app, email, password):
    return app.post(
        '/login',
        data=dict(email=email, password=password),
        follow_redirects=True
    )


def logout(app):
    return app.get(
        '/logout',
        follow_redirects=True
    )
