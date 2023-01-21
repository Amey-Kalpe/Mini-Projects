from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flaskapp import app

if __name__ == '__main__':
    app.run(debug=True)
