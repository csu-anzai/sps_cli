/*****

Template básico de aplicativo Node.JS com o módulo 'express'.
Autor: @bwb0de
email: danielc@unb.br

*****/

//Importando módulos do a serem usados
const express = require('express'); //http framework
const handlebars = require('express-handlebars').create({defaultLayout:'main'}); //Definindo os padrões dos templates (handlebars)
const body_parser = require('body-parser'); //para obter dados encaminhados via POST.
//const fs = require("fs");
//const db = require("db_json_paths");

/*
const session = require('express-session');
const parseurl = require('parseurl');

const child_process = require('child_process').spawn;
const formidable = require('formidable'); //para aceitar upload de arquivos
const cookie_parser = require('cookie-parser');
*/

const child_process = require('child_process').spawn;

/*
function read_json_file(target_json_file) {
	let rawdata = fs.readFileSync(target_json_file);
	let jsondata = JSON.parse(rawdata);
	return jsondata;
}
*/

let app = express();


app.disable('x-powered-by'); //evitando que informações do servidor sejam exibidas
app.engine('handlebars', handlebars.engine);
app.set('view engine', 'handlebars');
app.use(body_parser.urlencoded({extended: true}));
app.set('port', process.env.PORT || 3000); //definindo a porta do servidor http
app.use(express.static(`${__dirname}/public`)); //definindo caminho de acesso ao conteúdo estático


app.get('/', function(req, res){
  res.render('index', {style_sheet: ['frontpage', 'w3']}); 
});


app.use(function(req, res, next){
  console.log('Looking for URL : ' + req.url); // Imprime tentativas de acesso a locais ou arquivos além da raiz do site e continua...
  next();
});

  
app.use(function(err, req, res, next){
  console.log('Error : ' + err.message); // Apanha o erro, apresenta-o no console e continua...
  next();
});



app.get('/listar_usuarios', function(req, res){
  var process = child_process('lst', ['-j', 'usr', 'id']);
  process.stdout.on('data', function(data) { 
    res.render('listar_usuarios', {style_sheet: ['frontpage', 'w3'], nfo: JSON.parse(data.toString())});
  });
});

app.get('/listar_atendimentos', function(req, res){
  var process = child_process('lst', ['-j', 'atd']);
  process.stdout.on('data', function(data) { 
    res.render('listar_atendimentos', {style_sheet: ['frontpage', 'w3'], nfo: JSON.parse(data.toString())});
  });
});

app.get('/listar_processos', function(req, res){
  var process = child_process('lst', ['-j', 'sei']);
  process.stdout.on('data', function(data) { 
    res.render('listar_processos', {style_sheet: ['frontpage', 'w3'], nfo: JSON.parse(data.toString())});
  });
});

app.get('/listar_processos_pendentes', function(req, res){
  var process = child_process('lst', ['-j', 'pnd']);
  process.stdout.on('data', function(data) { 
    res.render('listar_processos_pnd', {style_sheet: ['frontpage', 'w3'], nfo: JSON.parse(data.toString())});
  });
});



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
