from cURL import cURL

class KrakenMaster(object):

    base_url='http://skynet.local:5000/'
    debug=False
    curl=False

    def __init__(self, debug=False):
        self.debug=debug
        self.curl = cURL(debug=debug)
        
    def get_settings(self):
        data = self.curl.make_request(url=self.base_url + 'settings/api/retrieve')
        if self.debug:
            print("Retrieved Settings :: %s " % data)
        return data

    def create_grade(self, args):
        data = self.curl.make_request(url=self.base_url + 'grades/api/create', method='POST',type_json=True, args=args)
        if self.debug:
            print("Created Grade :: %s " % data)
        if data and 'success' in data:
            return data['success']
        else:
            return False
