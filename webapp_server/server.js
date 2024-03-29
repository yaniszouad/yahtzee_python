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

//.............Instantiate socket................................//

//Socket Conection
let server = require('http').Server(app);
let io = require('socket.io')(server);

io.on('connection', function(socket){  
  io.emit('connection', {
    num_total_connections: io.engine.clientsCount
  }); 

  socket.on('game_connection', function(data) {  
    socket.join(data.game_name);
    console.log('Socket game connection event:', data.username, io.sockets.adapter.rooms.get(data.game_name).size);
    io.to(data.game_name).emit('game_connection', {
        username:data.username,
        num_game_connections: io.sockets.adapter.rooms.get(data.game_name).size
    });
  }); 

  socket.on('chat', function(data) {
    console.log('Socket chat event:', data);
    io.to(data.game_name).emit('chat', {
      username: data.username,
      message: data.message
    });
  });
});

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
    games: [],
    password:"",
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

      //Verify user password matches
      if (details["password"] && details["password"]==password){
        let urlGames = 'http://127.0.0.1:5000/users/games/'+username;
        let resGames = await fetch(urlGames);
        let games = JSON.parse(await resGames.text());
        let newGames = games.filter((game) => game != "There is no game with this name or this id." && game != "There is no game with this name/id.")
        response.status(200);
        response.setHeader('Content-Type', 'text/html')
        response.render("game/game_details", {
          feedback:"",
          games: newGames,
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
    
});

app.post('/users', async function(request, response) {
  console.log(request.method, request.url) //event logging

  let username = request.body.username;
  let email = request.body.email;
  let password = request.body.password;

  if (username.length > 0 & email.length > 0 & password.length > 0){
    let url = 'http://127.0.0.1:5000/users/'+username;
    let res = await fetch(url);
    let details = JSON.parse(await res.text());

    url = "http://127.0.0.1:5000/users"
    res = await fetch(url);
    user_list = JSON.parse(await res.text());
    if(user_list.some(user => user.username == username)) {
      response.status(401);
      response.setHeader('Content-Type', 'text/html')
      response.render("users/user_details", {
        feedback:"This username is taken.",
        updating:false,
        email:"",
        password:"",
        games: [],
        username:""
    });
    } else if (user_list.some(user => user.email == email)){
      response.status(401);
      response.setHeader('Content-Type', 'text/html')
      response.render("users/user_details", {
        feedback:"This email is already in use.",
        updating:false,
        email:"",
        password:"",
        games: [],
        username:""
    })
    } else if (JSON.stringify(details) === '{}'){
      url = 'http://127.0.0.1:5000/users'
      const headers = {
          "Content-Type": "application/json",
      }
      res = await fetch(url, {
          method: "POST",
          headers: headers,
          body: JSON.stringify(request.body),
      });
    
      let posted_user = await res.text();
      details = JSON.parse(posted_user);
      let urlNewStuff = 'http://127.0.0.1:5000/users/games/'+username
      let resNewStuff = await fetch(urlNewStuff);
      let detailsOfStuff = JSON.parse(await resNewStuff.text());
      response.status(200);
      response.setHeader('Content-Type', 'text/html')
      response.render("game/game_details", {
          feedback:"",
          games: detailsOfStuff,
          username: username
      });
    } else {
      url = 'http://127.0.0.1:5000/users/' +username;
      const headers = {
          "Content-Type": "application/json",
      }
      res = await fetch(url, {
          method: "PUT",
          headers: headers,
          body: JSON.stringify(request.body),
      });
      
      let posted_user = await res.text();
      details = JSON.parse(posted_user);
      
      let urlNewStuff1 = 'http://127.0.0.1:5000/users/games/'+username
      let resNewStuff2 = await fetch(urlNewStuff1);
      let detailsOfStuff3 = JSON.parse(await resNewStuff2.text());
      response.status(200);
      response.setHeader('Content-Type', 'text/html')
      response.render("game/game_details", {
          feedback:"Success",
          games: detailsOfStuff3,
          username: username
      });
    } 
  } else {
    response.status(401); //401 Unauthorized
    response.setHeader('Content-Type', 'text/html')
    response.render("users/user_details", {
      feedback:"Some fields are empty. Please try again",
      updating:false,
      email:"",
      password:"",
      games: [],
      username:""
    });
  }
});

app.get('/users/delete/:username', async function(request, response) {
  let username = request.params.username;

  try {
      res = await fetch('http://127.0.0.1:5000/users/'+username, {
          method: 'DELETE',
      });
      let details = JSON.parse(await res.text());
      let user_id = details["id"];
      res2 = await fetch('http://127.0.0.1:5000/scorecards')
      let scorecards = JSON.parse(await res2.text());

      scorecards.forEach(async function(scorecard){
        if(scorecard["user_id"] == user_id){
          let url = 'http://127.0.0.1:5000/scorecards/' +scorecard.id;
          const headers = {
              "Content-Type": "application/json",
          }
          resDeletedScorecard = await fetch(url, {
              method: "DELETE"
          });
          
          let deletedScorecard = await resDeletedScorecard.text();
          scorecardJsoned = JSON.parse(deletedScorecard);
        }
      });
      
      response.render("login",{
        feedback:"Successfully deleted user",
        username:""
      })
  } catch (error) {
      console.error('Error deleting game:', error);
  }
});

app.get('/users/:username', async function(request, response) {
  console.log(request.method, request.url) //event logging
  //Get user information from body of POST request
  let username = request.params.username;
  let url = 'http://127.0.0.1:5000/users/'+username;
  let res = await fetch(url);
  let details = JSON.parse(await res.text());

  let password = details["password"];
  let email = details["email"];
  let urlScoresUser = 'http://127.0.0.1:5000/scores/'+username;
  let ScoresUserRes = await fetch(urlScoresUser);
  let scoreUserText = await ScoresUserRes.text()
  console.log(scoreUserText)
  let detailsScoreUser = JSON.parse(scoreUserText);
  
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

  let username = request.params.username;

  let url = 'http://127.0.0.1:5000/users/games/'+username
  let res = await fetch(url);
  let details = JSON.parse(await res.text());

  let newGames = details.filter((game) => game != "There is no game with this name or this id." && game != "There is no game with this name/id.")

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  try {
    response.render("game/game_details", {
      feedback:"",
      games: newGames,
      username: username
      });
  } catch (error) {
    console.error("Error rendering template:", error);
    response.status(500).send("Internal Server Error");
  }

});

app.post("/games", async function (request, response) {
  console.log(request.method, request.url, request.body); //event logging

  //Get game information from body of POST request
  const username = request.body.username;
  const game_name = request.body.game_name;

  // HEADs UP: You really need to validate this information!
  console.log("Info recieved:", username, game_name);

  const game_url = "http://127.0.0.1:5000/games";
  const headers = {
    "Content-Type": "application/json",
  };
  const game_res = await fetch(game_url, {
    method: "POST",
    headers,
    body: JSON.stringify({ name: game_name }),
  });

  const posted_game = await game_res.text();
  const game = JSON.parse(posted_game);
  if (
    game === "UNIQUE constraint failed: games.link" ||
    game === "game details is of the wrong format"
  ) {
    response.status(401);
    response.setHeader("Content-Type", "text/html");
    response.redirect("/games/" + username + "?feedback=invalid");
    return;
  }

  console.log("Returned game:", game);

  const user_url = "http://127.0.0.1:5000/users/" + username;
  const user_res = await fetch(user_url);
  const user = JSON.parse(await user_res.text());

  const scorecard_url = "http://127.0.0.1:5000/scorecards";
  const scorecard_res = await fetch(scorecard_url, {
    method: "POST",
    headers,
    body: JSON.stringify({ game_id: game.id, user_id: user.id, turn_order: 1 }),
  });

  const posted_scorecard = await scorecard_res.text();
  const scorecard = JSON.parse(posted_scorecard);
  console.log("Returned scorecard:", scorecard);

  response.status(200);
  response.setHeader("Content-Type", "text/html");
  response.redirect("/games/" + username);
}); //POST /games

app.get('/games/delete/:gameName/:username', async function(request, response) {
  let username = request.params.username;
  let gameName = request.params.gameName;
  console.log("THIS IS THE GAME NAME OF /games/delete/gameName/username", request.params.gameName)
  try {
      await fetch('http://127.0.0.1:5000/games/'+gameName, {
          method: 'DELETE'
      });
      response.redirect('/games/' + username);
  } catch (error) {
      console.error('You have had an error deleting:', error);
  }
});

app.get("/games/:game_name/:username", async function (request, response) {
  const game_name = request.params.game_name;
  const username = request.params.username;
  // add link
  console.log(
    "games/:game_name/:username",
    request.method,
    request.url,
    request.params
  ); //event logging

  const user_url = "http://127.0.0.1:5000/users/" + username;
  const user_res = await fetch(user_url);
  const user = JSON.parse(await user_res.text());
  const user_id = user.id;

  const url = `http://127.0.0.1:5000/games/scorecards/${game_name}`;
  const res = await fetch(url);
  const scorecard_details = JSON.parse(await res.text());
  const scorecards = scorecard_details;

  // for (const scorecard of scorecards) {
  //   console.log(
  //     "filters",
  //     scorecards.filter((e) => e.user_id === user_id)
  //   );
  //   console.log(scorecard.score_info.upper, scorecard.score_info.lower);
  // }
  // console.log(scorecard_details);

  response.status(200);
  response.setHeader("Content-Type", "text/html");
  response.render("game/game", {
    feedback: "",
    username,
    gameName: game_name,
    scorecards,
    user_id,
    scorecard_id: scorecards,
    scorecard_info:scorecards
  });
});

app.post('/scorecards/:scorecard_id', async function(request, response) {
  console.log(request.method, request.url) //event logging
  let scorecard_id = request.params.scorecard_id;
  let scorecard_data = request.body;
  console.log("THIS IS THE SCORECARD ID", scorecard_id, scorecard_data)

  url = 'http://127.0.0.1:5000/scorecards/' + scorecard_id;
  headers = {"Content-Type": "application/json"}

  let res = await fetch(url, {
    method: "PUT",
    headers: headers,
    body: JSON.stringify(scorecard_data)
  });
  json_data = await res.text();
  res_data = JSON.parse(json_data);
  console.log("THIS THE DATA OF RES", res_data)

  io.emit('update', res_data)

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.send({
    message: "Scorecard updated successfully"
  });
});

app.post("/games/join/:username", async function (request, response) {
  console.log(request.method, request.url, request.body); //event logging

  //Get game information from body of POST request
  let username = request.params.username;
  let game_name = request.body.game_name;

  // HEADS UP: You really need to validate this information!
  console.log("Info recieved:", username, game_name);

  let game_url = "http://127.0.0.1:5000/games/" + game_name;
  let headers = {
    "Content-Type": "application/json",
  };
  let game_res = await fetch(game_url);

  let got_game = await game_res.text();
  let game = JSON.parse(got_game);

  console.log("Returned game:", game);

  const user_url = "http://127.0.0.1:5000/users/" + username;
  const user_res = await fetch(user_url);
  const user = JSON.parse(await user_res.text());

  const scorecard_url = "http://127.0.0.1:5000/scorecards";
  const scorecard_res = await fetch(scorecard_url, {
    method: "POST",
    headers,
    body: JSON.stringify({ game_id: game.id, user_id: user.id, turn_order: 1 }),
  });

  const posted_scorecard = await scorecard_res.text();
  const scorecard = JSON.parse(posted_scorecard);
  console.log("Returned scorecard:", scorecard);

  response.status(200);
  response.setHeader("Content-Type", "text/html");
  response.redirect("/games/" + username);
}); //POST /games/join/:username


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
app.set('port', port); //let heroku pick the port if needed
server.listen(port, function() {
 console.log('Server started at http://localhost:'+port+'.')
});