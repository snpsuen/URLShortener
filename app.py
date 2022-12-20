from flask import Flask, render_template, request, redirect, url_for
import pickle, random, string
import os.path

def randomstring(length):
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=length
        )
    )

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='favicon.ico'))

@app.route('/shortenurl', methods=['GET', 'POST'])
def shortenurl():
    if request.method == 'POST':
      absolute = request.form['url']
      shorten = randomstring(8)
      
      filename = "urlmap.pkl"
      if os.path.exists(filename):
        urlmapfile = open(filename, "rb")
        urlmapdict = pickle.load(urlmapfile)
        urlmapfile.close()
      else:
        urlmapdict = {}
      
      urlmapdict[shorten] = absolute
      urlmapfile = open(filename, "wb")
      pickle.dump(urlmapdict, urlmapfile)
      urlmapfile.close()
      
      return render_template('result.html', variable=shorten)
    
@app.route('/<variable>')
def redirect(variable):
    filename = "urlmap.pkl"
    if os.path.exists(filename):
        urlmapfile = open(filename, "rb")
        urlmapdict = pickle.load(urlmapfile)
        try:
            fullurl = urlmapdict[variable]
            urlmapfile.close()
            return redirect(fullurl)
        except KeyError as ke:
            return(f"Short URL ({ke}) is not found!\n")
    else:
        return "URL mapping file does not exist!\n"
