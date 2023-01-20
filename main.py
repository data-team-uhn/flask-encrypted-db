from __init__ import create_app
from utils import initiate_db, create_admin_user


if __name__ == '__main__':
    initiate_db()
    create_admin_user()

    app = create_app()
    app.run('0.0.0.0', 5005)
