const express = require('express');

const router = express.Router();

const mountRegisterRoutes = require('../features/register/routes');
const mountLoginRoutes = require('../features/login/routes');
const mountLogoutRoutes = require('../features/logout/routes');
const mountResetPasswordRoutes = require('../features/reset-password/routes');
const mountProfileRoutes = require('../features/profile/routes');

function isAuthenticated(req, res, next) {
 
  return res.render('pages/dashboard',{picture_time:'11/23/15:05PM'},{date:[0,1,2,3,4,5,6]});
}

/* GET home page. */
router.get('/', isAuthenticated, (req, res) => {
  res.render('pages/dashboard');
});

router.get('/icons', isAuthenticated, (req, res) => {
  res.render('pages/icons');
});

router.get('/maps', isAuthenticated, (req, res) => {
  res.render('pages/maps');
});

router.get('/tables', isAuthenticated, (req, res) => {
  res.render('pages/tables');
});

mountRegisterRoutes(router);
mountLoginRoutes(router);
mountLogoutRoutes(router, [isAuthenticated]);
mountResetPasswordRoutes(router);
mountProfileRoutes(router, [isAuthenticated]);

module.exports = router;
