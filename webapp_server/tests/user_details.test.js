const puppeteer = require('puppeteer');
const fetch = require('node-fetch');

let {add_users_to_DB, add_1_player_games, delete_all_scorecards_from_DB, delete_all_games_from_DB, delete_all_users_from_DB }
= require('./util.js')

let url_base='http://127.0.0.1:3000'
let num_games_per_user=3;

describe('user_detailss.html', () => {
  let browser;
  let page;
  let users;
  let game_names;

  beforeAll(async () => {
    browser = await puppeteer.launch({headless:false}); 
    await delete_all_scorecards_from_DB()
    await delete_all_games_from_DB()
    await delete_all_users_from_DB()

    users= await add_users_to_DB(4)
    game_names = await add_1_player_games(users, num_games_per_user)
  });

  beforeEach(async () => {
    page = await browser.newPage()
  });

  afterEach(async () => {
    await page.close()
  });

  afterAll(async () => {
    await browser.close()
    await delete_all_scorecards_from_DB()
    await delete_all_games_from_DB()
    await delete_all_users_from_DB()   
  });

  describe('Required HTML Elements', () => {
    it("user_games.html should contain all required elements", async () => {
      await page.goto(url_base+'/users/'+users[0]["username"], {waitUntil: 'domcontentloaded'})
      let  required={
        '#username_input':{
          "tagName":'INPUT'
        },
        '#email_input':{
          "tagName":'INPUT'
        },
        '#password_input':{
          "tagName":'INPUT'
        },
        '#create_button':{
          "tagName":"BUTTON"
        },
        '#delete_link':{
          "tagName":"A"
        },
        '#user_games_ol':{
          "tagName":"OL"
        },
        '#feedback':{
          "tagName":"SECTION"
        },
        '#my_games_link':{
          "tagName":"A",
          "href":"/games/"+users[0]["username"]
        },
        '#user_details_link':{
          "tagName":"A",
          "href":"/users/"+users[0]["username"]
        }
      } 

      for (let i=1; i<=num_games_per_user; i++){
        let game_name=users[0]["username"]+"_game_"+i;
        let play_game_id="#game_link_"+game_name;
        required[play_game_id]={
          "tagName":"A",
          "href":"/games/"+game_name+"/"+users[0]["username"]
        }
   
      }

      for (let key in required){
        const element = await page.$(key);
        expect(element).toBeTruthy(); //Element is present
        const element_tagName = await page.$eval(key, element => element.tagName);
        expect(element_tagName).toBe(required[key]["tagName"]);//Element is correct tag type
        if(required[key]["href"]){
          const element_href = await page.$eval(key, element => element.href);
          expect(element_href).toBe(url_base+required[key]["href"]);//Element is correct tag type
        }
      }
      const title = await page.title();
      expect(title).toBe('Yahtzee: User Details');
    })
  });//Required HTML Elements
  describe('Delete User', () => {
    it('should delete a user when the delete button is pressed', async () => {
      await page.goto(url_base+'/users/'+users[2]["username"], {waitUntil: 'domcontentloaded'})
     
      //Get original user details for user id
      url='http://127.0.0.1:5000/users/'+users[2]["username"];
      res = await fetch(url);
      returned_user = await res.text();
      let original_user_info = JSON.parse(returned_user)

      let del_game_id="#delete_link";
      await page.click(del_game_id);
      await page.waitForTimeout(1000)//pause to let the browser load the DOM

      const title = await page.title();
      expect(title).toBe('Yahtzee: Login');

       //user is no longer present in DB users tables
       url='http://127.0.0.1:5000/users'
       res = await fetch(url);
       returned_users = await res.text();
       let all_users = JSON.parse(returned_users)
       for (user of all_users){
         expect(original_user_info["id"]).not.toEqual(user["id"]);
       }

      //user is no longer present in DB scorecards tables
      url='http://127.0.0.1:5000/scorecards'
      res = await fetch(url);
      returned_cards = await res.text();
      let all_cards = JSON.parse(returned_cards)
      for (card of all_cards){
        expect(original_user_info["id"]).not.toEqual(card["user_id"]);
      }
    });
  });//Delete Game Links

  describe('Create User Button', () => {
    it('should create a user when Create User button clicked with a valid user info', async () => {
      expect(false).toBe(true);
    });//Create Game Button

    it('should provide feedback when Create User button clicked with no information', async () => {
      expect(false).toBe(true);
    });
  
    it('should provide feedback when Create user button clicked with a duplicate user name', async () => {
      expect(false).toBe(true);
    });
    it('should provide feedback when Create user button clicked with a duplicate email', async () => {
      expect(false).toBe(true);
    });
  
  });//Create user Button

  describe('User Info Input Elements', () => {
    it('should be blank when Creat User buttom is clicked on login.html', async () => {
      expect(false).toBe(true);
    });

    it('should be populated with user info when My Account link clicked on navbar', async () => {
      expect(false).toBe(true);
    });
  
  });//User info input elements

  describe('User High Scores', () => {
    it('should have a <li> element for each user game', async () => {
      expect(false).toBe(true);
    });

    it('<li> elements should be sorted in descending order>', async () => {
      expect(false).toBe(true);
    });
  
  });//User High Scores

});
