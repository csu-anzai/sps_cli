/*****

Template básico de aplicativo Node.JS com o módulo 'express'.
Autor: @bwb0de
email: danielc@unb.br

*****/

//Importando módulos do a serem usados
const express = require('express'); //http framework
const formidable = require('formidable'); //para aceitar upload de arquivos
const handlebars = require('express-handlebars').create({defaultLayout:'main'}); //Definindo os padrões dos templates (handlebars)
const cookie_parser = require('cookie-parser');
const body_parser = require('body-parser'); //para obter dados encaminhados via POST.
const session = require('express-session');
const parseurl = require('parseurl');
const fs = require("fs");
const child_process = require('child_process').spawn;

let app = express();

app.disable('x-powered-by'); //evitando que informações do servidor sejam exibidas
app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars');
app.use(body_parser.urlencoded({extended: true}));
app.set('port', process.env.PORT || 3000); //definindo a porta do servidor http
app.use(express.static(`${__dirname}/public`)); //definindo caminho de acesso ao conteúdo estático


app.get('/', function(req, res){
  //var process = child_process('lst', ['-j', 'usr', 'id']);
  //process.stdout.on('data', function(data) { 
  //  res.render('listar', {style_sheet: ['frontpage', 'w3'], nfo: JSON.parse(data.toString())});
  //});
  res.render('index'); 
});


app.use(function(req, res, next){
  console.log('Looking for URL : ' + req.url); // Imprime tentativas de acesso a locais ou arquivos além da raiz do site e continua...
  next();
});

  
app.use(function(err, req, res, next){
  console.log('Error : ' + err.message); // Apanha o erro, apresenta-o no console e continua...
  next();
});


//Definir rotas daqui para baixo...
//*******************************/
app.get('/rotas_sps', function(req, res) {
  
  console.log('')
});




//*******************************/

//Define página padrão de erro 404.
app.use(function(req, res) {
  res.type('text/html');
  res.status(404);
  res.render('404', { style_sheet: ['frontpage', 'w3'] });
});


//Define página padrão de erro 500.
app.use(function(err, req, res, next) {
  console.error(err.stack);
  res.status(500);
  res.render('500', { style_sheet: ['frontpage', 'w3'] });
});

let port = app.get('port');

app.listen(port, function(){
  console.log(`Node.JS App iniciado em http://localhost:${port}/ aperte Ctrl-C para fechar.`);
});
