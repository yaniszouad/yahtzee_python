class Scorecard{
    constructor(category_elements, score_elements, myDice){
        this.category_elements = category_elements;
        this.dice=myDice;
        this.score_elements=score_elements;
    }

    /**
     * Determines whether the scorecard is full/finished
     * A full scorecard is a scorecard where all categories are disabled.
     *
     * @return {} a Boolean value indicating whether the scorecard is full
     */
    is_finished(){
        return this.category_elements.every(item => item.disabled)
    }

    /**
     * Validates a score for a particular category
     * Upper categories should be validated by a single generalized procedure
     * Hint: Make use of this.dice.get_sum() and this.dice.get_counts()
     *
     * @param {String} category the category that should be validated
     * @param {Number} value the proposed score for the category
     * 
     * @return {Boolean} a Boolean value indicating whether the score is valid for the category
    */
    is_valid_score(category, value){
        if (this.dice.get_sum() === 0) {
            return false;
        } else if (value === 0) {
            return true;
        }

        let uppers = ["one", "two", "three", "four", "five", "six"];
        let dice_counts = this.dice.get_counts();
        if (uppers.includes(category)) {
            let indexN = uppers.indexOf(category);
            return value === dice_counts[indexN] * (indexN + 1);
        }
        if (category === "three_of_a_kind" || category === "four_of_a_kind") {
            let requiredCount = category === "three_of_a_kind" ? 3 : 4;
            return Math.max(...dice_counts) >= requiredCount && value === this.dice.get_sum();
        }
        if (category === "full_house"){
            if (category === "full_house") {
                let hasThree = dice_counts.some(count => count === 3);
                let hasTwo = dice_counts.some(count => count === 2);
                return hasThree && hasTwo && value === 25;
            }}
        if (category === "large_straight")
            return this.isLargeStraight(dice_counts) && value === 40;
        if (category === "small_straight")
            return this.isSmallStraight(dice_counts) && value === 30;  
        if (category === "yahtzee"){
            return Math.max(...dice_counts) === 5 && value === 50;}
        if (category === "chance"){
            return value === this.dice.get_sum();}
        else{
            return "Error";}
          
    }
    isSmallStraight(dice_counts) {
        let straights = [
          [1,2,3,4],
          [2,3,4,5],
          [3,4,5,6]
        ];
        for (let straight of straights) {
          if (straight.every(num => dice_counts[num-1] > 0)) {
            return true;
          }
        }
        return false;
      }
      
      isLargeStraight(dice_counts) {
        let straights = [
          [1,2,3,4,5],
          [2,3,4,5,6]
        ];
        for (let straight of straights) {
          if (straight.every(num => dice_counts[num-1] > 0)) {
            return true;
          }
        }
        return false;
      }
    /**
    * Returns the current Grand Total score for a scorecard
    * 
    * @return {Number} an integer value representing the curent game score
    */
    get_score(){
        let count = 0;
        for (let i = 0; i < this.category_elements.length; i++)
            if (this.category_elements[i].disabled === true)
                count += parseInt(this.category_elements[i].value)

        let uppercount = 0
        for (let i = 0; i<6; i++)
            uppercount += parseInt(this.category_elements[i].value)
        
        if (uppercount > 63)
            count += 35
        return count
    }

    /**
     * Updates all score elements for a scorecard
    */
    update_scores(){
        const upper_score = this.category_elements
        .filter(
            (element) => element.classList.contains("upper") && element.disabled
        )
        .map((element) => element.value)
        .reduce((partialSum, a) => partialSum + parseInt(a), 0);
        const upper_bonus = upper_score >= 63;
        const upper_total = upper_bonus ? upper_score + 35 : upper_score;

        const lower_total = this.category_elements
        .filter(
            (element) => element.classList.contains("lower") && element.disabled
        )
        .map((element) => element.value)
        .reduce((partialSum, a) => partialSum + parseInt(a), 0);

        this.score_elements[0].innerHTML = upper_score;
        this.score_elements[1].innerHTML = upper_bonus ? 35 : "";
        this.score_elements[2].innerHTML = upper_total;
        this.score_elements[3].innerHTML = lower_total;
        this.score_elements[4].innerHTML = upper_total;
        this.score_elements[5].innerHTML = upper_total + lower_total;
    }

    /**
     * Loads a scorecard from a JS object in the specified format
     * Format:
     * {
            "dice_rolls":0,
            "upper":{
                "ones":-1,
                "twos":-1,
                "threes":-1,
                "fours":-1,
                "fives":-1,
                "sixes":-1
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":-1,
                "full_house":-1,
                "small_straight":-1,
                "large_straight":-1,
                "yahtzee":-1,
                "chance":-1
            }
        }
     *
     * @param {Object} gameObject the object version of the scorecard
    */
    load_scorecard(score_info) {
        this.dice.rolls_remaining_element.innerHTML = score_info.dice_rolls;
        let scores = {
        ...score_info.upper,
        ...score_info.lower};
        this.category_elements.forEach((element) => {
        let raw_id = element.id.slice(0, -6);
        //because the score_info format doesn't match the score_elements' ids
        let id = element.classList.contains("upper")
            ? raw_id === "six"
            ? "sixes"
            : raw_id + "s"
            : raw_id;
        let val = scores[id];
        if (val === -1) {
            element.value = "";
            element.disabled = false;
        } else {
            element.value = val;
            element.disabled = true;}
        });
        this.update_scores();
    }

  /**
     * Creates a JS object from the scorecard in the specified format
     * Useful for preparing a scorecard to send to the webapp server
     * 
     * Format:
     * {
            "dice_rolls":0,
            "upper":{
                "ones":-1,
                "twos":-1,
                "threes":-1,
                "fours":-1,
                "fives":-1,
                "sixes":-1
            },
            "lower":{
                "three_of_a_kind":-1,
                "four_of_a_kind":-1,
                "full_house":-1,
                "small_straight":-1,
                "large_straight":-1,
                "yahtzee":-1,
                "chance":-1
            }
        }
     *
     * @return {Object} an object version of the scorecard
     *
     */
  to_object() {
    console.log("running to object")
    let dice_rolls = this.dice.rolls_remaining_element.innerHTML;
    let upper = {};
    let lower = {};
    this.category_elements.forEach((element) => {
      let raw_id = element.id.slice(0, -6);
      if (element.classList.contains("upper")) {
        let id = raw_id === "six" ? "sixes" : raw_id + "s";
        upper[id] = element.disabled ? parseInt(element.value) : -1;
      } else {
        lower[raw_id] = element.disabled ? parseInt(element.value) : -1;
      }
    });
    return {
      dice_rolls,
      upper,
      lower,
    };
  }
}

export default Scorecard;






