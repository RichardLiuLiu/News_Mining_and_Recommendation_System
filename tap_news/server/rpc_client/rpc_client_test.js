var client = require('./rpc_client');

client.add(1, 2, (res) => {
    console.assert(res = 3);
});

client.getNewsSummariesForUser('test_user', 1, function(res) {
    console.assert(res != null);
});