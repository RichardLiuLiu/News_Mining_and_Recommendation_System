var express = require('express');
var path = require('path');

var index = require('./routes/index');
var news = require('./routes/news');
var auth = require('./routes/auth');
var config = require('./config/config.json');

var app = express();

var bodyParser = require('body-parser');
app.use(bodyParser.json());

var cors = require('cors');
app.use(cors());

var logger = require('./logger/info_logger');

// Connect MongoDB
require('./models/main').connect(config.mongodb_uri);

// Use passport strategies
var passport = require('passport');
app.use(passport.initialize());
var localSignupStrategy = require('./passport/signup_passport');
var localLoginStrategy = require('./passport/login_passport');
passport.use('local-signup', localSignupStrategy);
passport.use('local-login', localLoginStrategy);

// User auth_checker
var authCheckerMiddleware = require('./middleware/auth_checker');

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');
app.use('/static', express.static(path.join(__dirname, '../client/build/static/')));

app.use('/', index);
app.use('/news', news);
app.use('/auth', auth);

// catch 404.
app.use(function(req, res, next) {
  res.status(404);
});

module.exports = app;
