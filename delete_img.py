def delete_function():
  import os
  import glob
  files = glob.glob('/var/www/app/OS/static/img/*')
  for f in files:
    os.remove(f)
