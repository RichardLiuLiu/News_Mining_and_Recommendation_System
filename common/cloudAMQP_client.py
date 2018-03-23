import json
import pika

class CloudAMQPClient:
    def __init__(self, cloud_amqp_url, queue_name):
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        self.parms = pika.URLParameters(cloud_amqp_url)
        self.parms.socket_timeout = 3
        self.connection = pika.BlockingConnection(self.parms)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)
    
    def send_message(self, message):
        self.channel.basic_publish(exchange='',
                                   routing_key=self.queue_name,
                                   body=json.dumps(message))
        print("[x] Message sent to %s: %s" % (self.queue_name, message))

    def get_message(self):
        method_frame, header_frame, body = self.channel.basic_get(self.queue_name)
        if method_frame:
            print("[x] Message received from %s: %s" % (self.queue_name, body))
            self.channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body.decode('utf-8'))
        else:
            print("No message returned")
            return None
    
    def sleep(self, seconds):
        self.connection.sleep(seconds)
