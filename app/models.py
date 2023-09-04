from app import db

class Application(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.String(100), unique=True, nullable=False)
    business_details = db.Column(db.JSON, nullable=False)
    balance_sheets = db.relationship('BalanceSheet', backref='application', lazy=True)
    
    def serialize(self):
        return {
            'id': self.id,
            'application_id': self.application_id,
            'business_details': self.business_details,
         
        }

class BalanceSheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.String(100), db.ForeignKey('application.application_id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    profit_or_loss = db.Column(db.Float, nullable=False)
    assets_value = db.Column(db.Float, nullable=False)
