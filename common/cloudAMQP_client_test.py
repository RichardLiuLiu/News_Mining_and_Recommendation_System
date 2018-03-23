from cloudAMQP_client import CloudAMQPClient

TEST_CLOUDAMQP_URL = "amqp://evdlvwsm:3sDqS4rgHn8kZIo7eFTBZgWhYHr0hvda@skunk.rmq.cloudamqp.com/evdlvwsm"
TEST_QUEUE_NAME = "test"

def test_basic():
    client = CloudAMQPClient(TEST_CLOUDAMQP_URL, TEST_QUEUE_NAME)

    sentMsg = {'test': 'test'}
    client.send_message(sentMsg)
    receivedMsg = client.get_message()
    assert sentMsg == receivedMsg
    print('test_basic passed.')

if __name__ == "__main__":
    test_basic()
