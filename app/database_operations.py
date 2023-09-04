from app import db
from app.models import Application
from datetime import datetime
import uuid

def generate_unique_application_id():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_string = str(uuid.uuid4().hex)[:6]
    return f"{timestamp}-{random_string}"

def create_application(business_name, year_established):
    new_application = Application(application_id=generate_unique_application_id(), business_details={"name": business_name, "year_established": year_established})
    db.session.add(new_application)
    db.session.commit()
    return new_application

def get_application_by_id(application_id):
    return Application.query.get(application_id)

def update_application(application_id, new_name, new_year_established):
    application = Application.query.get(application_id)
    if application:

        application.business_details={"name": new_name, "year_established": new_year_established}
        db.session.commit()
        return application
    return None


def delete_application(application_id):
    application = Application.query.get(application_id)
    if application:
        db.session.delete(application)
        db.session.commit()
        return True
    return False
