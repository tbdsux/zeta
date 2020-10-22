var express = require('express')
var router = express.Router()

// dashboard index
router.get('/', function (req, res, next) {
  res.render('dashboard/index')
})

// collections
router.get('/collections', function (req, res, next) {
  res.render('dashboard/collections')
})

// browse
router.get('/browse', function (req, res, next) {
  res.render('dashboard/browse')
})

module.exports = router
