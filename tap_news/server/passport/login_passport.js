const jwt = require('jsonwebtoken');
const User = require('mongoose').model('User');
const PassportLocalStrategy = require('passport-local').Strategy;
const config = require('../config/config.json');

module.exports = new PassportLocalStrategy(
    {
        usernameField: 'email',
        passwordField: 'password',
        session: false,
        passReqToCallback: true
    },
    (req, email, password, done) => {
        const userData = {
            email: email.trim(),
            password: password
        };

  // Find a user by email address
    return User.findOne({ email: userData.email }, (err, user) => {
        if (err) {
            return done(err);
        }

        if (!user) {
            const error = new Error('Incorrect email or password');
            error.name = 'IncorrectCredentialsError';
            return done(error);
        }

        // Check if a hashed user's password is equal to a value saved in the database
        return user.comparePassword(userData.password, (passwordErr, isMatch) => {
            if (err) {
                return done(err);
            }

            if (!isMatch) {
                const error = new Error('Incorrect email or password');
                error.name = 'IncorrectCredentialsError';
                return done(error);
            }
            
            // Create a token string
            const payload = {
                sub: user._id
            };           
            const token = jwt.sign(payload, config.jwtSecret);

            return done(null, token, null);
        });
    });
});