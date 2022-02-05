from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return { column.name : getattr(self, column.name) for column in self.__table__.columns }

class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    map_url = StringField('Location URL', validators=[DataRequired(), URL()])
    location = StringField('Cafe Location', validators=[DataRequired()])
    img_url = StringField('Image URL', validators=[DataRequired(), URL()])
    seats = SelectField('No. of seats',choices=['0-10','10-20','20-30','30-40','40-50','50+'],  validators=[DataRequired()])
    has_toilet = BooleanField('Has toilet?', default='checked')
    has_wifi = BooleanField('Has Wifi?', default='checked')
    has_sockets = BooleanField('Has Sockets?', default='checked')
    can_take_calls = BooleanField('Can take calls?', default='checked')
    coffee_price = StringField('Coffee price', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Flask routes
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        cafe = Cafe(name=form.name.data,
            map_url=form.map_url.data,
            location=form.location.data,
            img_url=form.img_url.data,
            seats=form.seats.data,
            has_toilet=form.has_toilet.data,
            has_wifi= form.has_wifi.data,
            has_sockets= form.has_sockets.data,
            can_take_calls= form.can_take_calls.data,
            coffee_price=form.coffee_price.data,
            )
        db.session.add(cafe)
        db.session.commit()
        return redirect(url_for('cafes'))
    return render_template('add_and_update.html', title="Add New Cafe", form=form)

@app.route('/cafes')
def cafes():
    all_cafes = Cafe.query.all()
    list_of_rows = [cafe.to_dict() for cafe in all_cafes]
    return render_template('cafes.html', cafes=list_of_rows)

@app.route('/update/<int:cafe_id>', methods=['GET', 'POST'])
def update_cafe(cafe_id):
    form = CafeForm()
    cafe_details = Cafe.query.filter_by(id=cafe_id).first()
    if request.method == "GET":
        form.name.data=cafe_details.name
        form.map_url.data=cafe_details.map_url
        form.location.data=cafe_details.location
        form.img_url.data=cafe_details.img_url
        form.seats.data=cafe_details.seats
        form.has_toilet.data=cafe_details.has_toilet
        form.has_wifi.data=cafe_details.has_wifi
        form.has_sockets.data=cafe_details.has_sockets
        form.can_take_calls.data=cafe_details.can_take_calls
        form.coffee_price.data=cafe_details.coffee_price

    if form.validate_on_submit():
        cafe_details.name=form.name.data
        cafe_details.map_url=form.map_url.data
        cafe_details.location=form.location.data
        cafe_details.img_url=form.img_url.data
        cafe_details.seats=form.seats.data
        cafe_details.has_toilet=form.has_toilet.data
        cafe_details.has_wifi= form.has_wifi.data
        cafe_details.has_sockets= form.has_sockets.data
        cafe_details.can_take_calls= form.can_take_calls.data
        cafe_details.coffee_price=form.coffee_price.data
        db.session.commit()
        return redirect(url_for('cafes'))
    return render_template('add_and_update.html', title="Update Cafe", form=form)

@app.route('/delete/<int:cafe_id>')
def delete_cafe(cafe_id):
    cafe_info_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_info_to_delete)
    db.session.commit()
    return redirect(url_for('cafes'))

if __name__ == '__main__':
    app.run(debug=True)
