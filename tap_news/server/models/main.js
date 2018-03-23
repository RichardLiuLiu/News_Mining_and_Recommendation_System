var logger = require('../logger/info_logger');

const mongoose = require('mongoose');

module.exports.connect = (uri) => {
    mongoose.connect(uri);
    mongoose.connection.on('error', (err) => {
        logger.error('Mongoose connection error: ${err}');
        process.exit(1);
    });
    
    require('./user');
};