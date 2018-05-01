from flask import  url_for, Response
from plivo import plivoxml
import pandas as pd
from io import StringIO
import requests as req
import numpy as np


def ivr(request):
    r = plivoxml.ResponseElement()
    if request.method == 'GET':
        get_digits_action_url = url_for('ivr', _external=True)
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
             
            call_number = get_number(role = 'sales')
            return get_forward( request, forward_number = call_number, message = message) 


        elif digit == '2':
            r.add_speak(''' Thank you for your interest in partnering with us.

Please use the contact us page on our website: www.aldora . capital.com
            .And someone from our team will contact you as soon as possible..''')
        elif digit == '3':
            r.add_redirect(url_for('call_router', _external = True), method = 'GET')

        elif digit == '0':
            call_number = get_number(role = 'help')
            return get_forward( request, forward_number = call_number, message = 'Calling Help line.')

        else:
            r.add_speak('No input detected, Hanging up.')
        return Response(r.to_string(), mimetype='text/xml')
    

def call_router(request):
    r = plivoxml.ResponseElement()

    if request.method == 'GET':
        call_router_url = url_for('call_router', _external = True)
        getDigits = plivoxml.GetDigitsElement(action = call_router_url, 
                method = 'POST', timeout = 10, digit_timeout = 3, retries = 1)
        r.add(getDigits)
        getDigits.add_speak('Please enter the extension now.')
        return Response(r.to_string(), mimetype='text/xml')

    if request.method == 'POST':
        extension = request.form.get('Digits')
        return get_forward(extension)    
    
    
def get_number(extension = 0, role = False):
    url = '''https://docs.google.com/spreadsheets/d/e/2PACX-1vSQx83iQ3YCY_11sMzBImLUGIDceoZUYhTGz0-2zp2FvInYITBFJqSBq-dQJstkZZYrTzLOOOsaw16-/pub?gid=0&single=true&output=csv'''
    directory = pd.read_csv(StringIO(req.get(url).text))
    directory.set_index('extension', inplace = True)
    directory.index = directory.index.map(int)
    if role != False:
        directory = directory[directory['role'].str.contains(role, case = False)]
        extension = directory.index.min()

    if role == 'sales':
        extension = np.random.choice(directory.index)
    
    if int(extension) not in directory.index:
        return 'Fail'
    number =  directory.loc[int(extension), 'number']
    return number


def get_forward(request, extension = False, forward_number = False, message = 'Forwarding Now'):
    r = plivoxml.ResponseElement()
    if forward_number == False:
        forward_number = get_number(extension)

    if forward_number == 'Fail':
        r.add_speak('No individual found with that extension')
        return Response(r.to_string(), mimetype='text/xml')
    
    from_number = request.form.get('From')
    xml_data = '''<Response>
        <Speak>{}</Speak>
        <Dial callerId="{}">
            <Number>{}</Number>
        </Dial>
    </Response>
    '''.format(message, from_number, forward_number)
    print(xml_data)
    return Response(xml_data, mimetype = 'text/xml')
