import pandas as pd
from io import StringIO
import requests as req
import numpy as np
from plivo import plivoxml
    
    
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
