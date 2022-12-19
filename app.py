from flask import Flask, render_template, request
import pickle, random, string

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
      
      urlmapfile = open("urlmap.pkl", "wb")
      urlmapfile.close()
      urlmapfile = open("urlmap.pkl", "rb")
      urlmapdict = pickle.load(urlmapfile)
      
      urlmapdict[shorten] = absolutepath
      pickle.dump(urlmapdict, urlmapfile)
      urlmapfile.close()
      return render_template('result.html', variable=shorten)
    
@app.route('/<variable>')
def redirect(variable):
    urlmapfile = open("urlmap.pkl", "rb")
    urlmapdict = pickle.load(urlmapfile)
    absolutepath = urlmapdict[variable]
    urlmapfile.close()
    return redirect(absolutepath)
