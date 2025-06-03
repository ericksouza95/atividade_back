from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
app.app_context().push()

user = User(username='admin2', password=generate_password_hash('1234'))
db.session.add(user)
db.session.commit()
