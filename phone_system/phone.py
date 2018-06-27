from phone_system import phone_tools
import flask as f
from flask import request,url_for, Response
from plivo import plivoxml

app = f.Blueprint('phone', __name__)


#------------------------------PHONE SYSTEM----------------------#
@app.route('/ivr', methods = ['GET', 'POST'])
def ivr():
    r = plivoxml.ResponseElement()
    if request.method == 'GET':
        get_digits_action_url = url_for('phone.ivr', _external=True)
        getDigits = plivoxml.GetDigitsElement(action = get_digits_action_url, 
                method = 'POST', timeout = 7, retries =1)
        getDigits.add_speak(''' Thank you for calling Aldora Capital Partners incorporated.
        if you would like to get information about our lending products. Please press one.
        If you are a broker. And would like to partner with us, to help your clients better. Please press two.
        If you know your parties extension, please press three. 
        For all other inquiries please press zero.  
        ''')
        
        r.add(getDigits)
        r.add_speak('No input recieved. Thank you for contacting Aldora Capital.')
        return Response(r.to_string(), mimetype='text/xml')
    
    if request.method == 'POST':
        digit = request.form.get('Digits')
        if digit == '1':
            message = ' We are routing your call to a nearest in house specialist, if they do not pick up the phone, leave them a message and they will get back to you.'
             
            call_number = phone_tools.get_number(role = 'sales')
            return phone_tools.get_forward( request, forward_number = call_number, message = message) 


        elif digit == '2':
            r.add_speak(''' Thank you for your interest in partnering with us.

Please use the contact us page on our website: www.aldora . capital.com
            .And someone from our team will contact you as soon as possible..''')
        elif digit == '3':
            r.add_redirect(url_for('phone.call_router', _external = True), method = 'GET')

        elif digit == '0':
            call_number = phone_tools.get_number(role = 'help')
            return phone_tools.get_forward( request, forward_number = call_number, message = 'Calling Help line.')

        elif len(str(digit)) > 0:
            return phone_tools.get_forward(request, extension=digit, message='Getting Forward to extension')

        else:
            r.add_speak('No input detected, Hanging up.')
        return Response(r.to_string(), mimetype='text/xml')
    
    

@app.route('/call_router/', methods = ['GET', 'POST'])
def call_router():
    r = plivoxml.ResponseElement()

    if request.method == 'GET':
        call_router_url = url_for('phone.call_router', _external = True)
        getDigits = plivoxml.GetDigitsElement(action = call_router_url, 
                method = 'POST', timeout = 10, digit_timeout = 3, retries = 1)
        r.add(getDigits)
        getDigits.add_speak('Please enter the extension now.')
        return Response(r.to_string(), mimetype='text/xml')

    if request.method == 'POST':
        extension = request.form.get('Digits')
        return phone_tools.get_forward(request, extension)