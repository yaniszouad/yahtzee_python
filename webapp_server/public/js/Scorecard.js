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
        return this.category_elements.every(iterated => iterated.disabled)
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
      
    }

    /**
    * Returns the current Grand Total score for a scorecard
    * 
    * @return {Number} an integer value representing the curent game score
    */
    get_score(){

    }

    /**
     * Updates all score elements for a scorecard
    */
    update_scores(){
       
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
        console.log(score_info)
        console.log(this.score_elements)
        let objectToPass = {
            "rolls_remaining":score_info.dice_rolls,
            "upper":{
                "one":score_info.ones,
                "two":score_info.twos,
                "three":score_info.threes,
                "four":score_info.fours,
                "five":score_info.fives,
                "sixe":score_info.sixes
            },
            "lower":{
                "three_of_a_kind":score_info.three_of_a_kind,
                "four_of_a_kind":score_info.four_of_a_kind,
                "full_house":score_info.full_house,
                "small_straight":score_info.small_straight,
                "large_straight":score_info.large_straight,
                "yahtzee":score_info.yahtzee,
                "chance":score_info.chance
            }
        }
        return objectToPass
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
      
    }
}

export default Scorecard;






