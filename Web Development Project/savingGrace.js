var express = require('express');
var app = express();
var handlebars = require('express-handlebars').create({defaultLayout:'main'});

app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars');
app.set('port', 7714);

app.get('/', function(req,res){
  res.render('home');
});

app.get('/meet-gracie', function(req,res){
  res.render('meetGracie');
});

app.get('/healthy-pup', function(req,res){
  res.render('healthy');
});

app.get('/happy-pup', function(req,res){
  res.render('happy');
});

app.use(function(req,res){
  res.status(404);
  res.render('404');
});

app.use(function(err, req, res, next){
  console.error(err.stack);
  res.type('plain/text');
  res.status(500);
  res.render('500');
});

app.listen(app.get('port'), function(){
  console.log('Express started on http://localhost:' + app.get('port') + '; press Ctrl-C to terminate.');
});

