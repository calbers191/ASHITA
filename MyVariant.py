import requests

class MyVariant():

    def __init__(self, copath_no, chr, pos, ref, alt, gene, transcript_id, c_dot):
        self.copath_no = copath_no
        self.chr = chr
        self.pos = pos
        self.ref = ref
        self.alt = alt
        self.gene = gene
        self.transcript_id = transcript_id
        self.c_dot = c_dot


    def get_functional_predictions(self):
        params = {'add-all-data': 1, 'format': 'json', "Authorization": "Token aF31n1tErNi#yVp%j5@j2dL7Pws#xTYSZ8&b64@e"}
        r = requests.get('https://api.varsome.com/lookup/' + self.chr + "-" + self.pos + "-" + self.ref + "-" + self.alt, params=params)
        print(r.url)
        return r.json()
