from flask import Flask, render_template, request
import requests
import os
import openai
import pickle
#import slack
#import twilio
import re
from time import time, sleep

app = Flask(__name__)

owm_api = 'df2896aab5e0e903ee90fadda5aaf0d7'
# model = pickle.loasd(open('model.sav', 'wb'))
@app.route('/')
def index():
  return render_template('index.html')


@app.route('/chatbot')
def chatbot():
  return render_template('chatbot.html')


@app.route('/recyclehelper')
def recyclehelper():
  return render_template('recyclehelper.html')

# @app.route("/api")
# def api():
#   print(request)

@app.route('/weather', methods=['GET', 'POST'])
def weather():
   return render_template('weather.html')
  
# @app.route('/uploader', methods = ['GET', 'POST'])
# def upload_file():
#    if request.method == 'POST':
#       f = request.files['upload']
#       f.save(secure_filename(f.filename))
#       return model.predict()
#       
     
#CHAT BOT BY TEJAS#
def open_file(filepath):
  with open(filepath, 'r', encoding='utf-8') as infile:
    return infile.read()


openai.api_key = "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"



def is_valid_input(input_text):
    # Remove any non-alphanumeric characters from the input
    cleaned_input = re.sub(r'\W+', '', input_text)

    # Check if the cleaned input is at least 5 characters long
    if len(cleaned_input) < 5:
        return False
    else:
        return True

def bot(prompt,
        engine='text-davinci-002',
        temp=0.9,
        top_p=1.0,
        tokens=1000,
        freq_pen=0.0,
        pres_pen=0.5,
        stop=['<<END>>']):
  max_retry = 1
  retry = 0
  while True:
    try:
      response = openai.Completion.create(engine=engine,
                                          prompt=prompt,
                                          temperature=temp,
                                          max_tokens=tokens,
                                          top_p=top_p,
                                          frequency_penalty=freq_pen,
                                          presence_penalty=pres_pen,
                                          stop=[" User:", " AI:"])
      text = response['choices'][0]['text'].strip()
      print(text)
      filename = '%s_gpt3.txt' % time()
      with open('gpt3_logs/%s' % filename, 'w') as outfile:
        outfile.write('PROMPT:\n\n' + prompt +
                      '\n\n==========\n\nRESPONSE:\n\n' + text)
      return text
    except Exception as oops:
      retry += 1
      if retry >= max_retry:
        return "GPT3 error: %s" % oops
      print('Error communicating with OpenAI:', oops)
      sleep(1)


@app.route("/get")
def get_bot_response():
  userText = request.args.get('msg')
  if is_valid_input(userText):
    botresponse = bot(prompt=userText)
  else:
    botresponse = "Sorry, I didn't catch that - try again."
  return str(botresponse)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
