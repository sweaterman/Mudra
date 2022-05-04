# -*- coding: utf-8 -*-
# app.py
from flask import Flask, render_template, request, jsonify
import Algo
import sys
import io

# flask ��ü �ν��Ͻ� ����
app = Flask(__name__)

@app.route('/')   # �����ϴ� url
def index():
    return 'Safety Login'

answers = []


@app.route('/getAnswer', methods = ['POST'])
def getAnswer():
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
    answer = request.get_json()
    print(answer)
    # ���⼭ py ���� ���� ��ȭ �����͸� return ���ָ� �ɵ�
    result = Algo.runningApp(answer)
    print(result)
    return result      # �޾ƿ� ������ ����



@app.route('/userLogin', methods = ['POST'])            # test�� ��Ʈ
def userLogin():
    user = request.get_json()#json �����͸� �޾ƿ�
    print(user)
    return jsonify(user)# �޾ƿ� �����͸� �ٽ� ����



@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(error)
    return render_template('page_not_found.html'), 404


if __name__=="__main__":
    app.run()
    # host ���� ���� �����ϰ� �ʹٸ�
    #app.run(host="173.30.1.22", port="5000", debug=True)