#!/usr/bin/env python

import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import time

#ACCESS_TOKEN = 'bhCSxrbWx9tRwoycO-Jf1Dh-KDBUQ01c_BbrTsPfaJVtRzvPdOT8JgKcKnuEjQYZLt5MZs1YKxM='
#PROJECT_ID = '45f7b0f416a311e483a622000a9e07fe'

class StormLog(object):

    def __init__(self, access_token, project_id, input_url=None):
        self.url = input_url or 'https://api-3qhk-yq9b.data.splunkstorm.com/1/inputs/http'
        self.project_id = project_id
        self.access_token = access_token
                        
        self.pass_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        self.pass_manager.add_password(None, self.url, 'x', access_token)
        self.auth_handler = urllib.request.HTTPBasicAuthHandler(self.pass_manager)
        self.opener = urllib.request.build_opener(self.auth_handler)
        urllib.request.install_opener(self.opener)
                                                                    
    def send(self, event_text, sourcetype='syslog', host=None, source=None):
        params = {'project': self.project_id,'sourcetype': sourcetype}
        if host:
            params['host'] = host
        if source:
            params['source'] = source
        url = '%s?%s' % (self.url, urllib.parse.urlencode(params))
        try:
            req = urllib.request.Request(url, event_text)
            response = urllib.request.urlopen(req)
            return response.read()
        except (IOError, OSError) as ex:
            raise            

if __name__ == '__main__':
    print("Started at " + time.ctime())
    msg = time.ctime()     
    
                
#log = StormLog(ACCESS_TOKEN, PROJECT_ID)
# Send a log; will pick up the default value for ``source``.
#log.send('Jul 28 2014 10:06:02 host57 action=supply_win amount=5710.3',sourcetype='syslog', host='host57')


# Will pick up the 'default' value for ``host``.
#log.send('Jul 28 2014 10:06:02 host44 action=deliver from=foo@bar.com to=richard.crouch100@gmail.com',sourcetype='syslog')                                                                                                                                                                                                                                        sourcetype='syslog')