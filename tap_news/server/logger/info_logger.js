var winston = require('winston');

// Create a logger
var logger = new winston.Logger ({
    transports: [
        new (winston.transports.Console) ({
            timestamp: () => (new Date()).toLocaleTimeString(),
            colorize: true,
        }),
        new (winston.transports.File)({
            name: 'info-log',
            filename: './debug.log',
            level: 'info',
            json: false
        }),
        new (winston.transports.File)({
            name: 'error-log',
            filename: './errors.log',
            level: 'error',
            json: false
        })
    ]
});

module.exports = logger;