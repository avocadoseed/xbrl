
import os, shutil, zipfile, re

pat = re.compile(r".+PublicDoc.+xbrl$")

path = ".\\downloaded"
targetpath = os.path.join(os.getcwd(), "xbrl")

os.chdir(path)
for d in os.listdir("."):
  zf = zipfile.ZipFile(d)
  print(d)
  for item in zf.namelist():
    if pat.match(item):
      print(item)
      zf.extract(item, ".\\tmp")
      filename = os.path.basename(item)
      print(filename)
      target_filename = os.path.join(targetpath, filename)
      if not os.path.exists(target_filename):
        shutil.move(".\\tmp\\" + item, targetpath)

  
