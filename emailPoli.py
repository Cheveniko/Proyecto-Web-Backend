from __main__ import app
from flask import request, jsonify, render_template
from app import app as ap
from flask_mail import Mail, Message
from decouple import config 
from flask import current_app


# Credenciales del MAIL

ap.config['SECRET_KEY'] = "tsfyguaistyatuis589566875623568956"

ap.config['MAIL_SERVER'] = "smtp.googlemail.com"

ap.config['MAIL_PORT'] = 587

ap.config['MAIL_USE_TLS'] = True

ap.config['MAIL_USERNAME'] = "poliflights@gmail.com"

ap.config['MAIL_PASSWORD'] = "bhhcoksaufstncdn"

mail = Mail(ap)

@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.form  
    recipient = data['recipient']   
    print(recipient)
    msg_title = "Gracias por su compra"

    sender = "noreply@app.com"
    msg = Message(msg_title,sender= sender, recipients=[recipient])
    msg_body = "Aqui va el body"
    msg.body = ""
    
    # En caso de hacer algo mas elaborado
    # msg.html = render_template("email.html",data=data)

    data = {
		'app_name': "POLI FLIGHTS",
		'title': msg_title,
		'body': msg_body,
	}

    msg.html = render_template("email.html",data=data)

    
    try:
        mail.send(msg)
        return jsonify({'message': 'Email sent successfully'}), 200
    except Exception as e:
        print(e)
        return f"the email was not sent {e}"
