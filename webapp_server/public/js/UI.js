console.log("UI.js connected")
import Dice from './Dice.js';
import Scorecard from './Scorecard.js';

//-------Dice Setup--------//
let roll_button = document.getElementById('roll_button'); 
roll_button.addEventListener('click', roll_dice_handler);

let rolls_remaining_element = document.getElementById("rolls_remaining");
let dice_elements =[];
for (let i = 0; i<5; i++){
    let die = document.getElementById("die_"+i);
    die.addEventListener('dblclick', reserve_die_handler);
    dice_elements.push(die);
}
let dice = new Dice(dice_elements, rolls_remaining_element);
window.dice = dice;

//-----Scorecard Setup---------//
let category_elements = Array.from(document.getElementsByClassName("category"));
for (let category of category_elements){
    category.addEventListener('keypress', function(event){
        if (event.key === 'Enter') {
            enter_score_handler(event);
        }
    });
}
let score_elements = Array.from(document.getElementsByClassName("score"));
let scorecard = new Scorecard(category_elements, score_elements, dice);
window.scorecard = scorecard;
dice.reset();
//---------Event Handlers-------//
function reserve_die_handler(event){
    console.log("Trying to reserve "+event.target.id);
    console.log(event.target.src.slice(29,-4))
    if (event.target.src.slice(29,-4) == "blank"){
        display_feedback("Cannot reserve a blank die", "bad");
    }
    else{
        dice.reserve(document.getElementById(event.target.id))
    }
}

function roll_dice_handler(){
    if (dice.get_rolls_remaining() > 0) {
        display_feedback("Rolling the dice...", "good");
        dice.roll();
      } else {
        display_feedback("Out of rolls", "bad");
      }
    
      console.log("Dice values:", dice.get_values());
      console.log("Sum of all dice:", dice.get_sum());
      console.log("Count of all dice faces:", dice.get_counts());
}

async function enter_score_handler(event){
    console.log("Score entry attempted for: ", event.target.id.slice(0,-6));
    if (scorecard.is_valid_score(event.target.id.slice(0,-6), parseInt(event.target.value))) {
        display_feedback("Correctly entered the score", "good");
        document.getElementById(event.target.id).disabled = true
        
        let url_routes = window.location.href.split("/");
        let username = url_routes[url_routes.length-1];
        console.log(username)
        console.log("This is the value of the thing ", document.getElementById("scorecard_id").dataset.score)
        let scorecard_id = document.getElementById("scorecard_id").dataset.score;
        let data = window.scorecard.to_object();
        console.log(data)
        
        let res = await fetch("http://127.0.0.1:3000/scorecards/"+scorecard_id, {
            method: "POST",
            headers: {
            "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        });
        dice.reset();
        console.log("Response from update: ", await res.json());   
    }
    else
        display_feedback("Incorrect score", "bad");
    
}

//------Feedback ---------//
function display_feedback(message, context){
    let feedback_element = document.getElementById("feedback");
    feedback_element.innerHTML = message;
    if (context == "good"){
        feedback_element.className = "good";
    } else {
        feedback_element.className = "bad";
    }
}