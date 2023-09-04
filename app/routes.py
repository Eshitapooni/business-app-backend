import requests
from flask import Flask, request, jsonify
from app import app, db
from app.decision_engine import submit_to_decision_engine
from app.accounting_providers import fetch_balance_sheet
from app.models import Application, BalanceSheet
from app.decision_engine import calculate_pre_assessment
from config import DECISION_ENGINE_URL
from datetime import datetime
import uuid

@app.route('/initiate-application', methods=['POST'])
def initiate_application():
    try:
        data = request.get_json()
        business_details = data['business_details']
        accounting_provider = data['accounting_provider']
        application_id = generate_unique_application_id()

        application = Application(application_id=application_id, business_details=business_details)
        db.session.add(application)
        db.session.commit()


        balance_sheet_data = fetch_balance_sheet(application.application_id,accounting_provider)
        balance_sheet = BalanceSheet(
            application_id=application.application_id,
            year=balance_sheet_data['year'],
            month=balance_sheet_data['month'],
            profit_or_loss=balance_sheet_data['profitOrLoss'],
            assets_value=balance_sheet_data['assetsValue']
        )
        db.session.add(balance_sheet)
        db.session.commit()

        return jsonify({"application_id": application.application_id})
    except Exception as e:
        app.logger.error(str(e))
        return jsonify({"error": "An error occurred: " + str(e)}), 500

def generate_unique_application_id():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_string = str(uuid.uuid4().hex)[:6]
    return f"{timestamp}-{random_string}"

@app.route('/fetch-balance-sheet/<string:application_id>', methods=['GET'])
def fetch_balance_sheet_endpoint(application_id):
    balance_sheet = BalanceSheet.query.filter_by(application_id=application_id).first()
    if balance_sheet:
        balance_sheet_data = {
            "year": balance_sheet.year,
            "month": balance_sheet.month,
            "profitOrLoss": balance_sheet.profit_or_loss,
            "assetsValue": balance_sheet.assets_value
        }
        return jsonify(balance_sheet_data)
    else:
        return jsonify({"error": "Balance sheet not found"}), 404

@app.route('/complete-application', methods=['POST'])
def complete_application():
    try:
        data = request.get_json()
        balance_sheet_data = data['balance_sheet']
        pre_assessment = calculate_pre_assessment(balance_sheet_data)
        
        decision_result = submit_to_decision_engine(data['business_details'], pre_assessment)

        decision = decision_result.get('decision')
        message = decision_result.get('message')
        return jsonify({"decision": decision, "message": message})
    except Exception as e:
        app.logger.error(str(e))
        return jsonify({"error": "An error occurred: " + str(e)}), 500

from app.database_operations import (
    create_application,
    get_application_by_id,
    update_application,
    delete_application
)

@app.route('/submit-application', methods=['POST'])
def submit_application():
    try:
        data = request.get_json()
        name = data.get('name')
        year_established = data.get('year_established')
        
        new_application = create_application(name, year_established)
        
        if new_application:
            return jsonify({'message': 'Application submitted successfully', 'application_id': new_application.id}), 201
        else:
            return jsonify({'message': 'Failed to submit application'}), 400
    except Exception as e:
        app.logger.error(str(e))
        return jsonify({"error": "An error occurred: " + str(e)}), 500

@app.route('/application/<int:application_id>', methods=['GET'])
def get_application(application_id):
    application = get_application_by_id(application_id)
    if application:
        return jsonify(application.serialize()), 200
    else:
        return jsonify({'message': 'Application not found'}), 404
    

@app.route('/application/<int:application_id>', methods=['PUT'])
def update_application_route(application_id):
    try:
        data = request.get_json()
        new_business_details = data.get('business_details', {})  # Ensure you get the data correctly
        new_name = new_business_details.get('name')
        new_year_established = new_business_details.get('year_established')
        
        updated_application = update_application(application_id, new_name, new_year_established)
        
        if updated_application:
            return jsonify({'message': 'Application updated successfully', 'application': updated_application.serialize()}), 200
        else:
            return jsonify({'message': 'Application not found'}), 404
    except Exception as e:
        app.logger.error(str(e))
        return jsonify({"error": "An error occurred: " + str(e)}), 500

@app.route('/application/<int:application_id>', methods=['DELETE'])
def delete_application_route(application_id):
    if delete_application(application_id):
        return jsonify({'message': 'Application deleted successfully'}), 200
    else:
        return jsonify({'message': 'Application not found'}), 404
