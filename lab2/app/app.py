from flask import Flask, render_template, request
from flask import make_response

app = Flask(__name__)


@app.route('/')
def index():
    # url = request.url
    return render_template('index.html')


@app.route('/headers')
def headers():
    return render_template('headers.html')


@app.route('/args')
def args():
    return render_template('args.html')


@app.route('/cookies')
def cookies():
    resp = make_response(render_template('cookies.html'))
    if 'name' in request.cookies:
        resp.delete_cookie('name')
    else:
        resp.set_cookie('name', 'value')
    return resp


@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template('form.html')


@app.route('/calc', methods=['GET', 'POST'])
def calc():
    result = ''
    error_text = ''
    if request.method == 'POST':
        try:
            first_num = int(request.form['first'])
            second_num = int(request.form['second'])
        except ValueError:
            error_text = 'Введите корректное число'
            return render_template('calc.html', result = result, error_text = error_text)

        operation = request.form['operation']
        if operation == '+':
            result = first_num + second_num
        elif operation == '-':
            result = first_num - second_num
        elif operation == '*':
            result = first_num * second_num
        elif operation == '/':
            try:
                result = first_num / second_num
            except ZeroDivisionError:
                error_text = 'На ноль делить нельзя'
    return render_template('calc.html', result = result, error_text = error_text)

def template_telephone(tel):
    if tel.startswith('8'):
        temp_tel = tel[1:]
    elif tel.startswith('+7'):
        temp_tel = tel[2:]
    else:
        temp_tel = tel[0:]
    temp_tel = temp_tel.replace(' ', '').replace('(', '').replace(')', '').replace('-', '').replace('.', '')
    operator = temp_tel[:3]
    operator = ''.join(operator)
    first_code = temp_tel[3:6]
    first_code = ''.join(first_code)
    second_code = temp_tel[6:8]
    second_code = ''.join(second_code)
    third_code = temp_tel[8:]
    return ("8-{}-{}-{}-{}".format(operator, first_code, second_code, third_code))

@app.route('/form_telephone', methods=['GET', 'POST'])
def form_telephone():
    k = 0
    error_text = ''
    temptel = ''
    # allowed_symbols = [' ', '.', '(', ')', '-', '+', '0', '1', '2', '3', '4', '5', '6', '7', '8' , '9']
    if request.method == 'POST':
        telephone = str(request.form['telephone'])
        telephone_after = list(telephone.strip(' .()-+0123456789'))
        if telephone_after != []:
                error_text = 'Недопустимый ввод. В номере телефона встречаются недопустимые символы.'
                # return render_template('form_telephone.html', error_text = error_text) 
        else:
            for i in list(telephone):
                if i.isdigit():
                    k += 1
            if telephone[0] == '8' or (telephone[0] == '+' and telephone[1] == '7'):
                if k != 11:
                    error_text = 'Недопустимый ввод. Неверное количество цифр.'
                    # return render_template('form_telephone.html', error_text = error_text) 
                else:
                    error_text = ''
                    temptel = str(template_telephone(telephone))
                    # return render_template('form_telephone.html', error_text = error_text, temptel = temptel) 
            elif k != 10:
                        error_text = 'Недопустимый ввод. Неверное количество цифр.'
                        # return render_template('form_telephone.html', error_text = error_text) 
            else:
                error_text = ''
                temptel = str(template_telephone(telephone))
                # return render_template('form_telephone.html', error_text = error_text, temptel = temptel) 
    return render_template('form_telephone.html', error_text = error_text, temptel = temptel)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
