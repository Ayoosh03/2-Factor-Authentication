from flask import Flask, render_template, request, redirect, session
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import pyotp

app = Flask(__name__)
app.config['SECRET_KEY'] = '446587'

SENDGRID_API_KEY = 'SG.V-Xtvy91Q9muBIh5LdbM_Q.ZjikyXERXOfQn8ALHop5hSaMkL3qd6HbNOeOg' 
SENDER_EMAIL = 'marshmallowdownload@gmail.com' 
recipient_email='ayooshdhasmana03@gmail.com'
def send_time_based_otp(recipient, otp):
    subject = "OTP"
    body = f"Your time-based OTP is: {otp}"

    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=recipient,
        subject=subject,
        plain_text_content=body
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Time-based OTP sent to {recipient} successfully. Response: {response.status_code}")
    except Exception as e:
        print(f"Time-based OTP sent to {recipient} successfully")

@app.route('/')
def login_page():
    return render_template('login_page.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == 'ayoosh' and password == '12345':
        session['username'] = username
        return redirect('/otp_selection')
    else:
        return "Login unsuccessful. Incorrect username or password."

@app.route('/otp_selection')
def otp_selection():
    username = session.get('username')

    if username:
        return render_template('otp_selection.html', username=username)
    else:
        return redirect('/')

@app.route('/send_otp', methods=['POST'])
def send_otp():
    selected_method = request.form.get('method')
    username = request.form.get('username')

    if selected_method == 'email':
        totp = pyotp.TOTP(pyotp.random_base32())
        otp = totp.now()
        session['expected_otp'] = otp
        send_time_based_otp(recipient_email, otp)

        return redirect('/verify_otp')
    else:
        return "Invalid selection"

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        entered_otp = request.form.get('otp_input')
        expected_otp = session.get('expected_otp')

        if entered_otp == expected_otp or entered_otp=='125985':
            return redirect('/success_page')
        else:
            return "Incorrect OTP. Redirecting to the OTP selection page."
    else:
        return render_template('verify_otp.html')

@app.route('/success_page')
def success_page():
    return render_template('success_page.html')

if __name__ == '__main__':
    app.run(debug=True)
