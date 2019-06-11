# -*- coding: utf-8 -*-
#__author__ = 'zj'
#__Date__ = 2019/6/11 14:09

from IPy import IP
from datetime import datetime
import subprocess
import re
import paramiko

class Compose(object):
  def __init__(self):
    self.ip_list=[]
    self.config_ip()
    self.passwd=['123123','123456']
    self.port=['22','2222']
    self.user=['root','ops']
    self.user_pass_port=[]
    self.exec_auth()
  
  def config_ip(self):
    file = open("./ip")
    while 1:
      line = file.readline()
      line = line.strip("\n")
      if not line:
        break
      else:
        self.ip_list.append(line)
    file.close()

  def ip_up(self, Msg):
    logs_file = "up.{}.{}".format(datetime.now().strftime("%Y_%m_%d_%H"), "logs")
    f = open(logs_file, 'a+')
    f.write(Msg)
    f.close()
  
  def ip_ssh_failure(self, Msg):
    logs_file = "ssh_filed.{}.{}".format(datetime.now().strftime("%Y_%m_%d_%H"), "logs")
    f = open(logs_file, 'a+')
    f.write(Msg)
    f.close()
  
  def ip_down(self, Msg):
    logs_file = "down.{}.{}".format(datetime.now().strftime("%Y_%m_%d_%H"), "logs")
    f = open(logs_file, 'a+')
    f.write(Msg)
    f.close()
  
  def exec_ssh(self, ip, user, passwd, port):
    try:
      ssh = paramiko.SSHClient()
      ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
      ssh.connect(ip, port=port, username=user, password=passwd, timeout=5)
      stdin, stdout, stderr = ssh.exec_command('whoami')
      if stdout.read().strip("\n"):
        self.ip_up("{} UP user:{} passwd:{} port:{} is ok\n".format(ip, user, passwd, port))
        return True
    except:
      self.ip_ssh_failure("{} up is ok , but user:{} passwd:{} port:{} ssh is failure \n".format(ip, user, passwd, port))
      return False
     
  
  def exec_auth(self):
    for u in range(len(self.user)):
      for pd in range(len(self.passwd)):
        for p in range(len(self.port)):
          self.user_pass_port.append("{},{},{}".format(self.user[u], self.passwd[pd], self.port[p]))
          
          
  def exec_ping(self, ip, count=1, timeout=1):
    cmd = 'ping -c %d -w %d %s' % (count, timeout, ip)
    p = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    result = p.stdout.read()
    regex = re.findall('100% packet loss', result)
    if len(regex) == 0:
      for c in range(len(self.user_pass_port)):
        tmp_list = (self.user_pass_port[c].split(','))
        if self.exec_ssh(str(ip[0]), tmp_list[0], tmp_list[1], tmp_list[2]):
          break
    else:
      print "\033[32m%s DOWN\033[0m" % (ip)
      self.ip_down("{} DOWN\n".format(ip))
  
  
  def exec_ip(self):
    for i in range(len(self.ip_list)):
      ip = IP(self.ip_list[i])
      for x in range(2, ip.len()):
        self.exec_ping(ip[x])
    
    
if __name__ == "__main__":
  test = Compose()
  print (test.exec_ip())