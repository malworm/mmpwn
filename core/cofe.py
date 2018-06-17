#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import re
from random import randint
import urllib3


class Cofe:
    
    def __init__(self, url, max_threads, user_agent):
        print("[+] Target {}".format(url))

        self.url = url
        self.agent = user_agent
        self.max_threads = int(max_threads)
        self.CleanUrl()

    def RandomAgent(self):
        with open('database/user-agents.txt', 'r') as f:
            uas = f.read()
            uas = re.sub("#.*","", uas)
            uas = uas.replace("\n\n", "")
            uas = uas.split("\n")
           
        random = randint(0, len(uas)-1)
        self.agent = uas[random]

    """ this method set a backslash at the end  """
    def CleanUrl(self):
        if self.url[-1] != '/':
            self.url = self.url + '/'


    def IsMMPub(self):
        self.index = requests.get(self.url, headers={"User-Agent":self.agent}, verify=False)
        # verificar se existe um mmpublish

    
    def IsUpOrDown(self):
        try:
            r = requests.get(self.url, allow_redirects=False, headers={"User-Agent":self.agent}, verify=False)
            if 'location' in r.headers:
                print("[+] The website try to redirect.. {}".format(r.headers['location']))
                userInput = str(input('[+] Do you want to follow the redirect ? [Y]es or [N]o:   '))
                if userInput.lower() == "y":
                    self.url == r.headers['location']
                else:
                    print("[+] Redirection found and not followed !")
                    exit()
        except Exception as e:
            print(e)
            print("[-] Critical website is down !")
            exit()

    def IsRobots(self):
        r = requests.get(self.url + "robots.txt", headers={"User-Agent":self.agent}, verify=False)
        if "200" in str(r) and not "404" in r.text:
            print("[+] Print robots txt avaliable under {}".format(self.url + "robots.txt"))
            lines = r.text.split('\n')
            for l in lines:
                if "Dissalow" in l:
                    print("[-] \t /interesting entry files in robots.txt !")
    
    def ToString(self):
        print("=== MMPwN ===")
        print("URL : {}".format(self.url))
        print("Agent: {}".format(self.agent))


    def HaveDWR(self):
        r = requests.get(self.url+"dwr/", headers={"User-Agent":self.agent}, verify=False)
        if "200" in str(r) and not "404" in r.text:
            print("[+] Critical! Find DWR PATH ==> {}".format(self.url+"dwr"))
    
    def GetAdminLogin(self):
        r = requests.get(self.url+"admin/admin.login.action", headers={"User-Agent":self.agent}, verify=False)
        if "200" in str(r) and not "404" in r.text:
            print("[+] ADMIN path found ==> {}".format(self.url+"admin/admin.login.action"))

    
            
        