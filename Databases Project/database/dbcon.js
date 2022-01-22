var mysql = require('mysql');
var pool = mysql.createPool({
  connectionLimit : 10,
  host            : 'classmysql.engr.oregonstate.edu',
  user            : 'cs340_[username]',
  password        : '[password]',
  database        : 'cs340_[username]'
});

module.exports.pool = pool;
