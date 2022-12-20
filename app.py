from flask import Flask, render_template, request
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

@app.route('/shortenurl', methods=['GET', 'POST'])
def shortenurl():
    if request.method == 'POST':
      absolutepath = request.form['url']
      shorten = randomstring(8)
      
      filename = "urlmap.pkl"
      if os.path.exists(filename):
        urlmapfile = open(filename, "rb")
        urlmapdict = pickle.load(urlmapfile)
        urlmapfile.close()
      
      urlmapdict = {}
      urlmapdict[shorten] = absolutepath  
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
            absolutepath = urlmapdict[variable]
            urlmapfile.close()
            return redirect(absolutepath)
        except KeyError as ke:
            return(f"Short URL not found: {ke}")
    else:
        return "URL mapping file does not exist!"
    
