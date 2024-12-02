from flask import Flask, request, render_template
import pandas as pd
from twilio.rest import Client

# Initialize Flask app
app = Flask(__name__)

# Load the dataset
predictions_df = pd.read_csv('clean-loan-test-predictions.csv')

# Twilio credentials (replace with your actual credentials)
TWILIO_ACCOUNT_SID = 'ACd9d940e7f69028b039e47a64c897e35e'
TWILIO_AUTH_TOKEN = 'c3cf21f89b6159eafd71e1422623730a'
TWILIO_PHONE_NUMBER = '+18557970169'

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from form
    loan_id = request.form.get('loan_id')
    phone_number = request.form.get('phone')

    # Search for the Loan ID in the dataset
    result = predictions_df[predictions_df['Loan_ID'] == loan_id]

    if not result.empty:
        loan_status = 'Eligible' if result['Loan_Status'].iloc[0] == 'Y' else 'Not Eligible'
        message_body = f"Loan ID: {loan_id}, Status: {loan_status}"

        # Send SMS
        client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )

        return render_template('result.html', loan_id=loan_id, loan_status=loan_status, sms_sent=True)
    else:
        return render_template('result.html', loan_id=loan_id, loan_status='Loan ID not found', sms_sent=False)

if __name__ == '__main__':
    app.run(debug=True)

  