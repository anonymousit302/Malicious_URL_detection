from multiprocessing.sharedctypes import Value
from pickle import GET
import re
from string import digits
from urllib.parse import urlparse
from weakref import finalize
from flask import Flask, render_template, render_template_string, request
from matplotlib.pyplot import text
from requests import post
import numpy as np
import pickle

from tld import get_tld



url = "https://practicaldatascience.co.uk/machine-learning/how-to-save-and-load-machine-learning-models-using-pickle#:~:text=To%20load%20a%20saved%20model,back%20an%20array%20of%20predictions."

url1 =[url]
list = []
app = Flask(__name__)
@app.route("/",methods=['GET','POST'])
def home():
    text = request.form.get('url99')
    if request.method=='GET':
        return render_template("homepage.html")

    elif request.method=='POST':
        print(text)
        return render_template("homepage.html")




def hostname_length():
    list.append(len(urlparse(url).netloc))

def path_length():
    list.append(len(urlparse(url).path))

def fd_length():
    urlpath= urlparse(url).path
    try:
        list.append(len(urlpath.split('/')[1]))
    except:
        list.append(0)

tld = get_tld(url,fail_silently=True)
def tld_length():
    try:
        list.append(len(tld))
    except:
        list.append(-1)

def counts_dash():
    list.append(url.count('-'))

def count_atherate():
    list.append(url.count('@'))

def count_question_mark():
    list.append(url.count('?'))

def count_percent():
    list.append(url.count('%'))

def count_dot():
    list.append(url.count('.'))

def count_equal_to():
    list.append(url.count('='))

def count_http():
    list.append(url.count('http'))

def count_https():
    list.append(url.count('https'))

def count_www():
    list.append(url.count('www'))

def digit_count():
    digits = 0
    for i in url:
        if i.isnumeric():
            digits = digits + 1
    list.append(digits)

def letter_count():
    letters = 0
    for i in url:
        if i.isalpha():
            letters = letters + 1
    list.append(letters)

def no_of_dir():
    urldir = urlparse(url).path
    list.append(urldir.count('/'))

def having_ip_address():
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
    if match:
        list.append(-1)
    else:
        # print 'No matching pattern found'
        list.append(1)

def Tokens(f):
    tkns_BySlash = str(f.encode('utf-8')).split('/')	# make tokens after splitting by slash
    total_Tokens = []
    for i in tkns_BySlash:
        tokens = str(i).split('-')	# make tokens after splitting by dash
        tkns_ByDot = []
        for j in range(0,len(tokens)):
            temp_Tokens = str(tokens[j]).split('.')	# make tokens after splitting by dot
            tkns_ByDot = tkns_ByDot + temp_Tokens
        total_Tokens = total_Tokens + tokens + tkns_ByDot
    total_Tokens = list(set(total_Tokens))	#remove redundant tokens
    if 'com' in total_Tokens:
        total_Tokens.remove('com')	#removing .com since it occurs a lot of times and it should not be included in our features
    return total_Tokens

def final_ans():
    loaded_vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))
    loaded_model = pickle.load(open('model1.pkl', 'rb'))
        # make a prediction
    print(loaded_model.predict(loaded_vectorizer.transform(url1)))



    


def getscores():
    hostname_length()
    path_length()
    fd_length()
    tld_length()
    counts_dash()
    count_atherate()
    count_question_mark()
    count_percent()
    count_dot()
    count_equal_to()
    count_http()
    count_https()
    count_www()
    digit_count()
    letter_count()
    no_of_dir()
    having_ip_address()
    review_array = np.array([list])
    pickled_model = pickle.load(open('model2', 'rb'))
    score1 = pickled_model.predict(review_array)
    var1 = score1[0]
    pickled_model2 = pickle.load(open('model3', 'rb'))
    score2 = pickled_model2.predict(review_array)
    var2 = score2[0]
    final_score = var1 + var2
    final_ans()
    return final_score
    
    


@app.route("/result", methods = ['POST','GET'])
def result():
    if request.method=='GET':
        return render_template("result.html")

    elif request.method=='POST':
        final_score2 = getscores()
        print(final_score2)
        if (final_score2<1):
            img_url = "down.jpeg"
        else:
            img_url = "up.jpeg"
        return render_template("result.html", value = final_score2 , value2 = url, filename = img_url)
    
    return render_template("result.html")

if __name__ == "__main__":
    app.run(debug=True)