#!/usr/bin/python

from cURL import cURL

class Skynet(object):

    debug = False
    base_url='http://skynet.local:3737/'
    device_name = 'KrakenAlarm'
    device={}
    uuid=False 
    token=False
    curl=False

    def __init__(self, debug=False):
        " Constructor "
        self.debug = debug
        self.curl = cURL(debug=debug)
        if not self.get_skynet_info():
            self.register()
            if self.debug:
                print("Skynet info not saved yet")
        self.update_my_device({'online' : 'true'})
    
    def no_error(self, data):
        if data:
            if 'errors' in data:
                if self.debug:
                    print("Error Response %s " % data)
                print("Error for skynet request %s" % data['error'])
            else:
                return True
        return False

    def get_skynet_status(self):
        data = self.curl.make_request(url=self.base_url + 'status')
        if self.no_error(data) and data['skynet'] == 'online':
            return True
        else:
            return False
    
    def get_skynet_info(self):
        if not self.uuid or not self.token:
            return False
        return {'uuid' : self.uuid, 'token' : self.token}

    def save_skynet_info(self, new_uuid, new_token):
        self.uuid = new_uuid
        self.token = new_token

    def register(self):
        if not self.get_skynet_status():
            if self.debug:
                print("Skynet offline")
            return False
        #Delete All Devices with same shit
        args = {'name':self.device_name, 'group' : 'Kraken'}
        devices = self.search_devices()
        for device in devices:
            self.delete_device(device)
        data = self.curl.make_request(url=self.base_url + 'devices', method='POST', args=args)
        if self.debug and data:
            print("Register Data %s" % data)
        if self.no_error(data):
            if self.debug:
                print("Skynet Registered %s" % data['uuid'])
            self.save_skynet_info(data['uuid'], data['token'])
            return True
        return False
    
    def update_my_device(self, params):
        return self.update_device(self.uuid, params)

    def update_device(self, uuid, params):
        default = {'token':self.token}
        args = dict(default.items() + params.items())
        if self.debug:
            print("Update Device args %s " % args);
        data = self.curl.make_request(url=self.base_url + 'devices/'+ uuid, method='PUT', args=args)
        if self.no_error(data):
            if self.debug:
                print("Skynet Device Updated %s" % data['uuid'])
            return True
        return False

    def get_device(self, uuid):
        data = self.curl.make_request(url=self.base_url + 'devices/' + uuid, method='GET')
        if self.no_error(data):
            if self.debug:
                print("Retrieved Device %s" % data)
            return data
        return False

    def send_message(self, devices="*", message={}):
        args = {"devices" : devices, "message" : message}
        data = self.curl.make_request(url=self.base_url + 'messages', method='POST', args=args, type_json=True)
        if self.no_error(data):
            if self.debug:
                print("Sent Message to Device(s) %s" % data)
            return data
        return False

    def search_devices(self, params={}):
        data = self.curl.make_request(url=self.base_url + 'devices', method='GET', args=params)
        if self.no_error(data):
            if self.debug:
                print("Search Devices %s" % data)
            return data
        return False

    def get_my_events(self):
        return self.get_events(self.uuid)
    
    def get_events(self, uuid):
        params = {'token' : self.token}
        data = self.curl.make_request(url=self.base_url + 'events/' + uuid, method='GET', args=params)
        if self.no_error(data):
            if self.debug:
                print("Retrieving Events %s" % data)
            return data
        return False
    
    def mysubscribe(self):
        return self.subscribe(self.uuid)
    
    def subscribe(self, uuid):
        params = {'token' : self.token}
        self.curl.make_request(url=self.base_url + 'subscribe/' + uuid, method='GET', args=params, streaming=True, callback=True)
        return True
    
    def delete_device(self, uuid):
        data = self.curl.make_request(url=self.base_url + 'devices/' + uuid, method='DELETE', args={'token' : self.token})
        if self.no_error(data):
            if self.debug:
                print("Delete Device %s" % data)
            return data
        return False
