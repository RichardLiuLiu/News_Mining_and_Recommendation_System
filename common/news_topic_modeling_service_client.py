import jsonrpclib

URL = "http://localhost:6060"
print("1")
client = jsonrpclib.ServerProxy(URL)
print("2")

def classify(text):
    topic = client.classify(text)
    print("Topic: %s" % str(topic))
    
    return topic