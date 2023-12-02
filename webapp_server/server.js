//..............Include Express..................................//
const express = require('express');
const fs = require('fs');
const ejs = require('ejs');
const fetch = require('node-fetch');

//..............Create an Express server object..................//
const app = express();

//..............Apply Express middleware to the server object....//
app.use(express.json()); //Used to parse JSON bodies (needed for POST requests)
app.use(express.urlencoded());
app.use(express.static('public')); //specify location of static assests
app.set('views', __dirname + '/views'); //specify location of templates
app.set('view engine', 'ejs'); //specify templating library

//.............Define server routes..............................//
//Express checks routes in the order in which they are defined
app.get('/', async function(request, response) {
  console.log(request.method, request.url) //event logging

  //-------------------Testing purposes: Verifying users actually exist in DB------------//
  let url = 'http://127.0.0.1:5000/users';
  let res = await fetch(url);
  let details = JSON.parse(await res.text());
  console.log("All Users in DB:")
  console.log(details)
  //-----------------------------------//

  response.status(200);
  response.setHeader('Content-Type', 'text/html');
  response.render("login",{
    feedback:"",
    username:""
  });
});

app.get('/users', async function(request, response) {
  console.log(request.method, request.url) //event logging

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("users/user_details",{
    feedback:"",
    updating:false,
    email:"",
    username:""
  });
});

app.get('/login', async function(request, response) {
    console.log(request.method, request.url) //event logging

    //Get user login info from query string portion of url
    let username = request.query.username;
    let password = request.query.password;
    if(username && password){
      //get alleged user 
      let url = 'http://127.0.0.1:5000/users/'+username;
      let res = await fetch(url);
      let details = JSON.parse(await res.text());
      console.log("Requested user per username:");
      console.log(details);

      //Verify user password matches
      if (details["password"] && details["password"]==password){
        let urlGames = 'http://127.0.0.1:5000/users/games/'+username;
        let resGames = await fetch(urlGames);
        let games = JSON.parse(await resGames.text());
        console.log("Requested games per username:");
        console.log(games);
        let urlHighscores = 'http://127.0.0.1:5000/scores';
        let resHighscores = await fetch(urlHighscores);
        let highscores = JSON.parse(await resHighscores.text());
        console.log("Requested highscores:");
        console.log(highscores);
        response.status(200);
        response.setHeader('Content-Type', 'text/html')
        response.render("game/game_details", {
          feedback:"",
          games: games,
          highscores: highscores,
          username: username
        });
      }else if (details["password"] && details["password"]!=password){
        response.status(401); //401 Unauthorized
        response.setHeader('Content-Type', 'text/html')
        response.render("login", {
          feedback:"Incorrect password. Please try again"
        });
      }else{
        response.status(404); //404 Unauthorized
        response.setHeader('Content-Type', 'text/html')
        response.render("login", {
          feedback:"Requested user does not exist"
        });
      }
    }else{
      response.status(401); //401 Unauthorized
      response.setHeader('Content-Type', 'text/html')
      response.render("login", {
        feedback:"Please provide both a username and password"
      });
    }
    
});//GET /login

app.post('/users', async function(request, response) {
  console.log(request.method, request.url) //event logging

  //Get user information from body of POST request
  let username = request.body.username;
  let email = request.body.email;
  let password = request.body.password
  // HEADs UP: You really need to validate this information!
  console.log("Info recieved:", username, email, password)
  let urlHighscores = 'http://127.0.0.1:5000/scores';
  let resHighscores = await fetch(urlHighscores);
  let highscores = JSON.parse(await resHighscores.text());
  console.log("Requested highscores:");
  console.log(highscores);
  const url = 'http://127.0.0.1:5000/users'
  const headers = {
      "Content-Type": "application/json",
  }
  let res = await fetch(url, {
      method: "POST",
      headers: headers,
      body: JSON.stringify(request.body),
  });
  let posted_user = await res.text();
  let details = JSON.parse(posted_user);
  let games = [] // Because new user
  console.log("Returned user:", details)
  if (details["result"] == "error"){
      response.status(405); //404 Unauthorized
      response.setHeader('Content-Type', 'text/html')
      response.render("users/user_details", {
        feedback:"You are not creating correctly. Try again.",
        username: "",
        updating:false,
        email: ""
      });}
  else{
    response.status(200);
    response.setHeader('Content-Type', 'text/html')
    response.render("game/game_details", {
        feedback:"",
        games: games,
        email: email,
        highscores: highscores,
        username: username
  });}
 
}); //POST /user

app.get('/users/:username', async function(request, response) {
  console.log(request.method, request.url) //event logging
  //Get user information from body of POST request
  let username = request.params.username;
  let url = 'http://127.0.0.1:5000/users/'+username;
  let res = await fetch(url);
  let details = JSON.parse(await res.text());
  console.log("Requested user per username:");
  console.log(details);

  let password = details["password"];
  let email = details["email"];
  console.log("Info received:", username, email, password)
  let urlScoresUser = 'http://127.0.0.1:5000/scores/'+username;
  let ScoresUserRes = await fetch(urlScoresUser);
  let detailsScoreUser = JSON.parse(await ScoresUserRes.text());
  console.log("Requested user per username:");
  console.log(detailsScoreUser);
  
  let games = detailsScoreUser;
  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("users/user_details", {
      feedback:"",
      games: games,
      updating: true,
      username: username,
      password: password,
      email: email
  });
 
});


app.get('/games/:username', async function(request, response) {
  console.log(request.method, request.url) //event logging

  let username = request.params.username; // why the hell is username "style.css"????
  console.log("USERNAME NHHDFHFHSDHFH:", username);
  let url = 'http://127.0.0.1:5000/users/'+username;
  let res = await fetch(url);
  let details = JSON.parse(await res.text());
  console.log("Requested user per username:");
  console.log(details);

  let password = details["password"];
  let email = details["email"];

  console.log("Info received:", username, email, password)

  let urlScoresUser = 'http://127.0.0.1:5000/scores/'+username;
  let ScoresUserRes = await fetch(urlScoresUser);
  
  let games;

  ScoresUserText = await ScoresUserRes.text()
  console.log("Scores User Text:", ScoresUserText);
  if (ScoresUserText == {"error": "This user does not exist"}){
    console.log([{"name":"ion"}, {"name":"ion"}, {"name":"ion"}, {"name":"ion"}]);
    
    games = [{"name":"ion"}, {"name":"ion"}, {"name":"ion"}, {"name":"ion"}];
    console.log("Scores User Text: Theres a problem with it...", games);
  }
  

  let detailsScoreUser = JSON.parse(ScoresUserText);
  console.log("Requested score per username:", detailsScoreUser);

  let urlHighscores = 'http://127.0.0.1:5000/scores';
  let resHighscores = await fetch(urlHighscores);
  textedResHighscores = await resHighscores.text()
  console.log("High Score as Text", textedResHighscores);
  let highscores = JSON.parse( textedResHighscores);
  console.log("JSONed Requested highscores:", highscores);

  if (highscores == { "error": "There are no current games" }){
    console.log("THERE ARE NO GAMES??");
    highscores = [{"name":"ion"}, {"name":"ion"}, {"name":"ion"}, {"name":"ion"}];}
    
  
  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  console.log("Games data:", games);
  try {
    response.render("game/game_details", {
      feedback:"",
      games: games,
      highscores: highscores,
      username: username
    });
  } catch (error) {
    console.error("Error rendering template:", error);
    response.status(500).send("Internal Server Error");
  }
 
});

app.post('/games/create', async function(request, response) {
  let username = request.body.username; 
  let gameName = request.body.game_name;

  if (!gameName) {
      return response.render('game/game_details', {
          feedback: 'Please enter a game name',
          games: [],
          highscores: [], 
          username: username
      });
  }

  try {
      let apiResponse = await fetch('http://127.0.0.1:5000/games', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: gameName })
      });
      
      // if (!apiResponse.statusText) { // Annie are you NOT okay? are you NOT okay annie?
      //     throw new Error('Failed to create the game');}
      let updatedGames = JSON.parse(await apiResponse.text()); // I NEED TO ADD IT TO THE CURRENT LIST OF UPDATED GAMES

      console.log('API Response:', updatedGames);
      let existingGameResponse = await fetch("http://127.0.0.1:5000/games/"+gameName);
      if (existingGameResponse.ok) {
          let existingGameData = await existingGameResponse.json();
          if (existingGameData) {
              return response.render('game/game_details', {
                  feedback: 'Added',
                  games: updatedGames,
                  highscores: [], 
                  username: username
              });
          }
      }

      return response.render('game/game_details', {
          feedback: 'A game with that name already exists',
          games: updatedGames,
          highscores: [], 
          username: username
      });

  } catch (error) {
      console.error('Error creating game:', error);
      return response.render('game/game_details', {
          feedback: 'Error creating game',
          games: [], 
          highscores: [],
          username: username
      });
  }
});

app.get('/games/delete/:gameName/:username', async function(request, response) {
  const { gameName, username } = request.params;

  try {
      await fetch(`http://127.0.0.1:5000/games/${gameName}`, {
          method: 'DELETE'
      });

      response.redirect('/games/' + username);
  } catch (error) {
      console.error('Error deleting game:', error);
  }
});

// Because routes/middleware are applied in order,
// this will act as a default error route in case of
// a request fot an invalid route
app.use("", function(request, response){
  response.status(404);
  response.setHeader('Content-Type', 'text/html')
  response.render("error", {
    "errorCode":"404",
    feedback:"",
    username:""
  });
});

//..............Start the server...............................//
const port = process.env.PORT || 3000;
app.listen(port, function() {
  console.log('Server started at http://127.0.0.1:'+port+'.')
});
