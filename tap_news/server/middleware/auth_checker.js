var logger = require('../logger/info_logger');

const jwt = require('jsonwebtoken');
const User = require('mongoose').model('User');
const config = require('../config/config.json');

module.exports = (req, res, next) => {
    logger.info('auth_checker: req: ' + req.headers);

    if (!req.headers.authorization) {
        return res.status(401).end();
    }

    // Get the last part from a authorization header string like "bearer token-value"
    const token = req.headers.authorization.split(' ')[1];

    logger.info('auth_checker: token: ' + token);

    // Decode the token using a secret key-phrase
    return jwt.verify(token, config.jwtSecret, (err, decoded) => {
        if (err) {
            return res.status(401).end();
        }

        const id = decoded.sub;

        // Check if a user exists
        return User.findById(id, (userErr, user) => {
            if (userErr || !user) {
                return res.status(401).end();
            }
            return next();
        });
    });
};