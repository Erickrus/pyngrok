import json
import requests
import pgrep
import subprocess
import os
import sys
import time


class Ngrok:

  def __init__(self, serviceCommand=""):
    if serviceCommand == "":
      self.serviceCommand = "./ngrok tcp 22 &"
    else:
      self.serviceCommand = serviceCommand

    self.zipFilename = "ngrok-stable-linux-amd64.zip"
    self.downloadUrl = "https://bin.equinox.io/c/4VmDzA7iaHb/%s" % self.zipFilename

  def install(self):
    if os.path.exists('ngrok'):
      print("skip install")
      time.sleep(2)
      return self

    # install
    os.system( "wget %s" % self.downloadUrl )
    time.sleep(2)
    os.system( "unzip %s" % self.zipFilename )
    time.sleep(2)
    return self


  def is_available(self):
    pids = pgrep.pgrep('ngrok')
    if len(pids)>0 and self.get_service_url() != "":
      return True
    else:
      return False


  def start_service(self):
    print("ngrok.start_service()")
    os.system(self.serviceCommand)
    time.sleep(5)
    return self


  def stop_service(self):
    print("ngrok.stop_service()")
    try:
      pids = pgrep.pgrep('ngrok')
      for pid in pids:
        os.system("kill -9 %d" % pid)
    except:
      pass
    time.sleep(5)
    return self


  def get_service_url(self):
    try:
      url = "http://localhost:4040/api/tunnels/"
      res = requests.get(url)
      res = res.content.decode("utf-8")
      res = json.loads(res)
      for item in res["tunnels"]:
        if item['name'] == "command_line":
          return item['public_url']
    except:
      pass
    return ""


  def message(self, text, msg_func=print):
    msg_func("\nngrok.message('%s')" % text)
    return self


  def authtoken(self, token):
    os.system("./ngrok authtoken %s" % token)
    time.sleep(2)
    return self

  def daemon(self):
    self.message(self.get_service_url())

    while True:
      time.sleep(1)
      if not self.is_available():
        # restart the service
        self.stop_service().start_service().message(self.get_service_url())

    return self
    
if __name__ == "__main__":
  ngrok = Ngrok() 
  ngrok.install()
  # ngrok.authtoken('...')
  ngrok.start_service().daemon()

