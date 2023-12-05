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
        // let urlHighscores = 'http://127.0.0.1:5000/scores';
        // let resHighscores = await fetch(urlHighscores);
        // let highscores = JSON.parse(await resHighscores.text());
        // console.log("Requested highscores:");
        // console.log(highscores);
        response.status(200);
        response.setHeader('Content-Type', 'text/html')
        response.render("game/game_details", {
          feedback:"",
          games: games,
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
  let detailsScoreUser = JSON.parse(await ScoresUserRes.text());
  
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

// app.get('/games/:username', async function(request, response) {
//   console.log(request.method, request.url) //event logging

//   let username = request.params.username; // why the hell is username "style.css"????
//   console.log("USERNAME NHHDFHFHSDHFH:", username);
//   let url = 'http://127.0.0.1:5000/users/'+username;
//   let res = await fetch(url);
//   let details = JSON.parse(await res.text());
//   console.log("Requested user per username:");
//   console.log(details);

//   let password = details["password"];
//   let email = details["email"];

//   console.log("Info received:", username, email, password)

//   let urlScoresUser = 'http://127.0.0.1:5000/scores/'+username;
//   let ScoresUserRes = await fetch(urlScoresUser);
  
//   let games;

//   ScoresUserText = await ScoresUserRes.text()
//   console.log("Scores User Text:", ScoresUserText);
//   if (ScoresUserText == {"error": "This user does not exist"}){
//     games = [{"name":"ion"}, {"name":"ion"}, {"name":"ion"}, {"name":"ion"}];
//     console.log("Scores User Text: Theres a problem with it...", games);
//   }
  

//   let detailsScoreUser = JSON.parse(ScoresUserText);
//   console.log("Requested score per username:", detailsScoreUser);

//   // let urlHighscores = 'http://127.0.0.1:5000/scores';
//   // let resHighscores = await fetch(urlHighscores);
//   // textedResHighscores = await resHighscores.text();
//   // console.log("High Score as Text", textedResHighscores);
//   // let highscores = JSON.parse( textedResHighscores);
//   // console.log("JSONed Requested highscores:", highscores);
  

//   // if (highscores == { "error": "There are no current games" }){
//   //   console.log("THERE ARE NO GAMES??");
//   //   highscores = [{"name":"ion"}, {"name":"ion"}, {"name":"ion"}, {"name":"ion"}];}
    
//   highscores = [{"name":"ion"}, {"name":"ion"}, {"name":"ion"}, {"name":"ion"}];

//   response.status(200);
//   response.setHeader('Content-Type', 'text/html')
//   console.log("Games data:", games);
//   try {
//     response.render("game/game_details", {
//       feedback:"",
//       games: games,
//       highscores: highscores,
//       username: username
//     });
//   } catch (error) {
//     console.error("Error rendering template:", error);
//     response.status(500).send("Internal Server Error");
//   }
 
// });


app.get('/games/:username', async function(request, response) {
  console.log(request.method, request.url) //event logging

  let username = request.params.username;
  

  let url = 'http://127.0.0.1:5000/users/games/'+username
  let res = await fetch(url);
  let details = JSON.parse(await res.text());
  let gameNames = [];

  let urlAllGames = 'http://127.0.0.1:5000/games'
  let resAllGames = await fetch(urlAllGames);
  let detailsAllGames = JSON.parse(await resAllGames.text());
  
  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  try {
    response.render("game/game_details", {
      feedback:"",
      games: detailsAllGames,
      username: username
      });
  } catch (error) {
    console.error("Error rendering template:", error);
    response.status(500).send("Internal Server Error");
  }

});
// app.post('/games', async function(request, response) {
//   console.log(request.method, request.url) //event logging
//   //...

//   //Get user information from body of POST request
//   let username = request.body.username;
//   let game_name = request.body.game_name;
//   // HEADS UP: You really need to validate this information
//   console.log("Info received:", username, game_name)
//   if (username.length > 0 && game_name.length > 0) {
//     let url = "http://127.0.0.1:5000/games/" + game_name;
//     let res = await fetch(url);
//     let gras = await res.text();
//     console.log("GAMES!!", gras)
//     let details = JSON.parse(gras);
//     console.log("Requested game per game_name:")
//     console.log(details)
//   }

//   url = "http://127.0.0.1:5000/games"
//   res = await fetch(url);
//   game_list = JSON.parse(await res.text());

//   if(game_list.some(game => game.name == game_name)) {
//     res = await fetch(url);
//     details = JSON.parse(await res.text());
//     url = "http://127.0.0.1:5000/scores"
//     res = await fetch(url);
//     let highscore_list = JSON.parse(await res.text());
//     response.status(401);
//     response.setHeader('Content-Type', 'text/html')
//     response.render('game/user_games', {
//       feedback: "Duplicate Name. Please try another game name.",
//       username: username,
//       gamelist: details,
//       highscore_list: highscore_list
//     });
//   } else if (JSON.stringify(details) === '{}'){
//     const headers = {
//       "Content-Type": "application/json",
//     }
//     res = await fetch(url, {
//       method: "POST",
//       headers: headers,
//       body: JSON.stringify({name: game_name}),
//     });

//     let posted_game = await res.text();
//     new_game = JSON.parse(posted_game);
//     console.log("Returned game:", new_game) //create the game

//     url = 'http://127.0.0.1:5000/users/' + username;
//     res = await fetch(url)
//     related_user = JSON.parse(await res.text());

//     url = 'http://127.0.0.1:5000/scorecards'
//     res = await fetch(url, {
//       method: "POST",
//       headers: headers,
//       body: JSON.stringify({game_id: new_game["id"], user_id: related_user["id"], turn_order: 0}),
//     });
//     await res.text();

//     url = 'http://127.0.0.1:5000/scores/' + username;
//     res = await fetch(url);
//     details = JSON.parse(await res.text());
//     url = "http://127.0.0.1:5000/scores"
//     res = await fetch(url);
//     let highscore_list = JSON.parse(await res.text());
//     response.status(200);
//     response.setHeader('Content-Type', 'text/html')
//     response.render('game/user_games', {
//       feedback: "",
//       username: username,
//       gamelist: details,
//       highscore_list: highscore_list
//     });
//   }
// });

// app.post('/games', async function(request, response) {
//   let username = request.body.username;
//   let gameName = request.body.game_name;

//   if (gameName == "" || gameName == null) {
//     return response.render('game/game_details', {
//         feedback: 'Please enter a game name',
//         games: [],
//         username: username
//     });
//   }

//   let url = 'http://127.0.0.1:5000/games' //make a post request to this url
//   const headers = {"Content-Type": "application/json",}

//   let res = await fetch(url, {
//     method: "POST",
//     headers: headers,
//     body: JSON.stringify({name: gameName}),
//   });

//   let gotten_game = await res.text(); //this is what the POST request sends back
//   console.log("GOTTEN GAME", gotten_game)
  
//   let details = JSON.parse(gotten_game);
//   console.log("Returned user:", details)

//   response.status(200);
//   response.setHeader('Content-Type', 'text/html')
//   response.render("game/game_details", {
//       games: details,
//       feedback:"",
//       username: username
//   });

// });

// app.post('/games', async function(request, response) {
//   let username = request.body.username; 
//   let gameName = request.body.game_name;
//   console.log("GAME NAME AQUI MOFO:", gameName)
//   if (gameName == "" || gameName == null || username == "" || username == null) {
//     console.log("GAME NAME AQUI THIS SHIT IS EMPTTYYYY AS HELKLLLLLLLL:", gameName)
//       return response.render('game/game_details', {
//           feedback: 'Please enter a game name',
//           games: [],
//           username: username
//       });
//   }

//   try {
//       let existingGameResponse = await fetch("http://127.0.0.1:5000/games/"+gameName); // Checking if the game already exists
//       console.log('API Response Existing Game Response:', existingGameResponse);
//       if (existingGameResponse.ok) {
//           console.log('DONT DO THAT SHIT')
//           let existingGameData = JSON.parse(await existingGameResponse.text());
//               return response.render('game/game_details', {
//                   feedback: 'A game with that name already exists',
//                   games: existingGameData,
//                   username: username
//               });
//       }

//       let resCreate = await fetch('http://127.0.0.1:5000/games', {
//           method: 'POST',
//           headers: { 'Content-Type': 'application/json' },
//           body: JSON.stringify({ name: gameName })
//       });
        
//       console.log("New Game Response:", resCreate);
  
//       let resTexted = await resCreate.text();
//       console.log('API Response 1:', resTexted);
//       let resTextedJson = JSON.parse(resTexted); 
//       console.log('json response:', resTextedJson);
//       let updatedGames = resTextedJson;

//       if (resCreate.status !== 200) { // Annie are you NOT okay? are you NOT okay annie?
//         throw new Error(resCreate.statusText);}

//       console.log('YES THATS ITS THATS THAT SHIT THAT SHIT')
//       return response.render('game/game_details', {
//           feedback: 'Added',
//           games: updatedGames,
//           username: username
//       });

//   } catch (error) {
//       console.error('Error creating game:', error);
//       return response.render('game/game_details', {
//           feedback: 'Error creating game',
//           games: [], 
//           username: username
//       });
//   }
// });

app.post('/games', async function(request, response) {
  let gamename = request.body.game_name;
  let username = request.body.username;
  console.log("/games")
  console.log(gamename)
   
  const url_2 = 'http://127.0.0.1:5000/games';

  let res_2 = await fetch(url_2); 
  let text_2 = await res_2.text();
  let details_2 = JSON.parse(text_2);

  let total_games = [];
  for (let p = 0; p < details_2.length; p++) {
    total_games.push(details_2[p]["name"]);
   }

  if (total_games.includes(gamename)){
    response.status(200);
    response.setHeader('Content-Type', 'text/html');
    response.render("game/game_details", {
      feedback:"Please enter a valid gamename",
      username: username,
      games:total_games
  });
  }

  else{
    let url = 'http://127.0.0.1:5000/games';
    const headers = {
      "Content-Type": "application/json",
  }  
    let res = await fetch(url, {
        method: "POST",
        headers: headers,
        body: JSON.stringify({name:gamename}),
    });
    let text = await res.text();
    let details = JSON.parse(text);
    
    if (details["name"]){
      if(details.length > 1){
        for (let i = 0; i < details.length; i++) {
          total_games.push(details[i]["name"]);
        }
      }
      else{
        total_games.push(details["name"]);
      }
      response.status(200);
      response.setHeader('Content-Type', 'text/html');
      response.render("game/game_details", {
          feedback:"",
          username: username,
          games: total_games
      });
    }else{
      response.status(200);
      response.setHeader('Content-Type', 'text/html');
      response.render("game/game_details", {
        feedback:"Please enter a valid gamename",
        username: username,
        games: total_games
    });
  }
}
});

app.get('/games/delete/:gameName/:username', async function(request, response) {
  let username = request.params.username;
  let gameName = request.params.gameName;
  console.log("THIS IS THE GAME NAME OF /games/delete/gameName/username", request.params.gameName)
  try {
      await fetch(`http://127.0.0.1:5000/games/${gameName}`, {
          method: 'DELETE'
      });
      response.redirect('/games/' + username);
  } catch (error) {
      console.error('Error deleting game:', error);
  }
});

app.get('/games/:gameName/:username', async function(request, response) {
  console.log("THIS IS THE GAME NAME OF /games/gameName/username", request.params.gameName)
  let username = request.params.username; 
  let gameName = request.params.gameName;

  response.status(200);
  response.setHeader('Content-Type', 'text/html')
  response.render("game/game",{
    feedback:"",
    gameName:gameName,
    username:username
  });
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
