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
          const type = category.id.slice(0, -6);
          const uppers = ["one", "two", "three", "four", "five", "six"];
          const dice_counts = this.dice.get_counts();
          if (uppers.includes(type)) {
            const number_index = uppers.indexOf(type);
            return value === dice_counts[number_index] * (number_index + 1);
          }
          switch (type) {
            case "three_of_a_kind":
              return Math.max(...dice_counts) >= 3 && value === this.dice.get_sum();
            case "four_of_a_kind":
              return Math.max(...dice_counts) >= 4 && value === this.dice.get_sum();
            case "full_house":
              let three = false;
              let two = false;
              for (const val of dice_counts) {
                if (val === 2) two = true;
                else if (val === 3) three = true;
              }
              return two && three && value === 25;
            case "small_straight":
              return Math.max(...dice_counts) <= 2 && value === 30;
            case "large_straight":
              return Math.max(...dice_counts) === 1 && value === 40;
            case "yahtzee":
              return Math.max(...dice_counts) === 5 && value === 50;
            case "chance":
              return value === this.dice.get_sum();
          }
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
    load_scorecard(score_info){
        this.dice.rolls_remaining_element.innerHTML = score_info["dice_rolls"];
        if (score_info["upper"]["ones"] == -1){
            this.category_elements[0].disabled = false;
        }else{
            this.category_elements[0].value = score_info["upper"]["ones"];
            this.category_elements[0].disabled = true;
        }
        
        if (score_info["upper"]["twos"] == -1){
            this.category_elements[1].disabled = false;
        }else{
            this.category_elements[1].value = score_info["upper"]["twos"];
            this.category_elements[1].disabled = true;
        }

        if (score_info["upper"]["threes"] == -1){
            this.category_elements[2].disabled = false;
        }else{
            this.category_elements[2].value = score_info["upper"]["threes"];
            this.category_elements[2].disabled = true;
        }

        if (score_info["upper"]["fours"] == -1){
            this.category_elements[3].disabled = false;
        }else{
            this.category_elements[3].value = score_info["upper"]["fours"];
            this.category_elements[3].disabled = true;
        }

        if (score_info["upper"]["fives"] == -1){
            this.category_elements[4].disabled = false;
        }else{
            this.category_elements[4].value = score_info["upper"]["fives"];
            this.category_elements[4].disabled = true;
        }

        if (score_info["upper"]["sixes"] == -1){
            this.category_elements[5].disabled = false;
        }else{
            this.category_elements[5].value = score_info["upper"]["sixes"];
            this.category_elements[5].disabled = true;
        }

        if (score_info["lower"]["three_of_a_kind"] == -1){
            this.category_elements[6].disabled = false;
        }else{
            this.category_elements[6].value = score_info["lower"]["three_of_a_kind"];
            this.category_elements[6].disabled = true;
        }

        if (score_info["lower"]["four_of_a_kind"] == -1){
            this.category_elements[7].disabled = false;
        }else{
            this.category_elements[7].value = score_info["lower"]["four_of_a_kind"];
            this.category_elements[7].disabled = true;
        }

        if (score_info["lower"]["full_house"] == -1){
            this.category_elements[8].disabled = false;
        }else{
            this.category_elements[8].value = score_info["lower"]["full_house"];
            this.category_elements[8].disabled = true;
        }

        if (score_info["lower"]["small_straight"] == -1){
            this.category_elements[9].disabled = false;
        }else{
            this.category_elements[9].value = score_info["lower"]["small_straight"];
            this.category_elements[9].disabled = true;
        }

        if (score_info["lower"]["large_straight"] == -1){
            this.category_elements[10].disabled = false;
        }else{
            this.category_elements[10].value = score_info["lower"]["large_straight"];
            this.category_elements[10].disabled = true;
        }

        if (score_info["lower"]["yahtzee"] == -1){
            this.category_elements[11].disabled = false;
        }else{
            this.category_elements[11].value = score_info["lower"]["yahtzee"];
            this.category_elements[11].disabled = true;
        }

        if (score_info["lower"]["chance"] == -1){
            this.category_elements[12].disabled = false;
        }else{
            this.category_elements[12].value = score_info["lower"]["chance"];
            this.category_elements[12].disabled = true;
        }
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
    to_object(){
        let score_info = {
            "dice_rolls": this.dice.rolls_remaining_element.innerHTML,
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
        if (this.category_elements[0].disabled == true)
            score_info["upper"]["ones"] = this.category_elements[0].value
        if (this.category_elements[1].disabled == true)
            score_info["upper"]["twos"] = this.category_elements[1].value
        if (this.category_elements[2].disabled == true)
            score_info["upper"]["threes"] = this.category_elements[2].value
        if (this.category_elements[3].disabled == true)
            score_info["upper"]["fours"] = this.category_elements[3].value
        if (this.category_elements[4].disabled == true)
            score_info["upper"]["fives"] = this.category_elements[4].value
        if (this.category_elements[5].disabled == true)
            score_info["upper"]["sixes"] = this.category_elements[5].value
        if (this.category_elements[6].disabled == true)
            score_info["lower"]["three_of_a_kind"] = this.category_elements[6].value
        if (this.category_elements[7].disabled == true)
            score_info["lower"]["four_of_a_kind"] = this.category_elements[7].value
        if (this.category_elements[8].disabled == true)
            score_info["lower"]["full_house"] = this.category_elements[8].value
        if (this.category_elements[9].disabled == true)
            score_info["lower"]["small_straight"] = this.category_elements[9].value
        if (this.category_elements[10].disabled == true)
            score_info["lower"]["large_straight"] = this.category_elements[10].value
        if (this.category_elements[11].disabled == true)
            score_info["lower"]["yahtzee"] = this.category_elements[11].value
        if (this.category_elements[12].disabled == true)
            score_info["lower"]["chance"] = this.category_elements[12].value
        
        return score_info
    }
}

export default Scorecard;





