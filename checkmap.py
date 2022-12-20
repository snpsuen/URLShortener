import pickle, os.path

filename = "urlmap.pkl"
if os.path.exists(filename):
  urlmapfile = open(filename, "rb")
  urlmapdict = pickle.load(urlmapfile)
  urlmapfile.close()
  print(urlmapdict)
else:
  print(f"File {filename} does not exist!\n")
