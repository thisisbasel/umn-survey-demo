from flask import Flask, request, render_template, jsonify, make_response
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


app = Flask(__name__)
ma = Marshmallow(app)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost/survey'

else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ewbjrbhnrnactd:885dc2586da7c86e604a3fb5b4fc54c05865832ccaf69a435cf2c51fa986d111@ec2-34-198-31-223.compute-1.amazonaws.com:5432/dda9fvqaitrpad'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Survey(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    state = db.Column(db.Text)
    campus = db.Column(db.String(200))
    work = db.Column(db.String(200))
    checked = db.Column(db.String(200))
    signed = db.Column(db.Text)

    def __init__(self, state, campus, work, checked, signed):
        self.state = state
        self.campus = campus
        self.work = work
        self.checked = checked
        self.signed = signed

class SurveySchema(ma.Schema):
    class Meta:
        fields = ('id', 'timestamp', 'state', 'campus', 'work', 'checked', 'signed')
    
survey_schema = SurveySchema
surveys_schema = SurveySchema(many=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/survey")
def survey():
    return render_template("survey.html")

@app.route("/decline")
def decline():
    return render_template("decline.html") 

# @app.route("/thanks")
# def thanks():
#     return render_template("thanks.html")

@app.route('/thanks', methods=['POST'])
def thanks():
    if request.method == 'POST':
        state = request.form['state']
        campus = request.form['campus']
        work = request.form['work'] 
        checked = request.form['checked']  
        signed = request.form['signed'] 
    data = Survey(state, campus, work, checked, signed)
    db.session.add(data)
    db.session.commit()
    return render_template("thanks.html")

@app.route('/api/results', methods=['GET'])
def api():
    queryString = request.args.get('reverse')
    all_surveys = Survey.query.all()
    result = surveys_schema.dump(all_surveys)

    if queryString:
        result.reverse(); 
   
    return jsonify(result)


# ?reverse=True


if __name__ == '__main__':
    app.run()
