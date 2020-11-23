const express = require('express');
const io = require('socket.io')

const router = express.Router();

const mountRegisterRoutes = require('../features/register/routes');
const mountLoginRoutes = require('../features/login/routes');
const mountLogoutRoutes = require('../features/logout/routes');
const mountResetPasswordRoutes = require('../features/reset-password/routes');
const mountProfileRoutes = require('../features/profile/routes');


function dynamicData(req, res, next) {


  return res.render('pages/dashboard',{pictureDate: 'sent socket message'});
}

/* GET home page. */
router.get('/', dynamicData, (req, res) => {
  res.render('pages/dashboard');
});

router.get('/icons', dynamicData, (req, res) => {
  res.render('pages/icons');
});

router.get('/maps', dynamicData, (req, res) => {
  res.render('pages/maps');
});

router.get('/tables', dynamicData, (req, res) => {
  res.render('pages/tables');
});

mountRegisterRoutes(router);
mountLoginRoutes(router);
mountLogoutRoutes(router, [dynamicData]);
mountResetPasswordRoutes(router);
mountProfileRoutes(router, [dynamicData]);

module.exports = router;
