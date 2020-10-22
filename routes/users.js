var express = require('express')
var router = express.Router()

// register page
router.get('/register', function (req, res, next) {
  res.render('front/register')
})

// login page
router.get('/login', function (req, res, next) {
  res.render('front/login')
})

module.exports = router
