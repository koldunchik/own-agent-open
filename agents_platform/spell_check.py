import http.client, urllib, json, requests, json, string
from pprint import pprint

input = 'Hllo wrld! Wlcome tt owr exibition. Just gimme som bad dada'

def addhints( input ):

    text = {'text' : input}
    key = 'c8453bb975854d9a9b7ed362a3369a1b'
    host = 'https://api.cognitive.microsoft.com'
    path = '/bing/v7.0/spellcheck'
    params = '?mkt=en-us&mode=proof&text=' + urllib.parse.urlencode(text)

    headers = {'Ocp-Apim-Subscription-Key': key,
    'Content-Type': 'application/x-www-form-urlencoded'}

    r = requests.get(host + path + params, headers=headers);
    jsont = json.loads(r.text)
    out = text['text']
    words = out.split()

    s = {}
    for token in jsont['flaggedTokens']:
        hint = '['
        hint += "/".join(map(lambda x: x['suggestion'], token['suggestions']))
        hint += ']'
        s[token['token']] = hint

    output = ""
    translator = str.maketrans('', '', string.punctuation)
    for word in words:
        output += word
        trimmed_word = word.translate(translator)
        if s.get(trimmed_word) != None:
            output += s.get(trimmed_word)
        output += " "

    return output


print ("in:" + input)
print ("out:" + addhints(input))