$(function() {
// Deck of Cards Game JavaScript

    // Deck constructor
    function Deck() {
        this.cardMin = 1;
        this.cardMax = 52;

        this.showCardsArr = function() {

            this.dealerCardsArr = [];

            for(var i = this.cardMin; i <= this.cardMax; i++) {
                this.dealerCardsArr.push(i);
            }

            return this.dealerCardsArr;
        };

        this.showDeck = function() {
            $("#dealer-cards").children("img").remove();

            $("#player-cards").children("img").remove();
            $("#player-cards").children("span").empty();

            var cards = this.showCardsArr();
            for(var i = this.cardMin - 1; i <= this.cardMax - 1; i++) {
                $("#dealer-cards").append("<img id='dealer_card_" + cards[i] + "' src='images/" + cards[i] + ".png' width='50'/>");
            }

            return this;
        };

        this.shuffleDeck = function() {
            $("#dealer-cards").empty();

            var cards = this.showCardsArr();
            var j = 0;
            var temp = null;

            for (var i = cards.length - 1; i > 0; i -= 1) {
                j = Math.floor(Math.random() * (i + 1));
                temp = cards[i];
                cards[i] = cards[j];
                cards[j] = temp;

                $("#dealer-cards").append("<img id='dealer_card_" + cards[i] + "' src='images/" + cards[i] + ".png' width='50'/>");
            }

            return this;
        }

        this.dealFirstCard = function() {
            var firstCard = $("#dealer-cards").children("img").first();

            firstCard.clone().appendTo("#player-cards");
            firstCard.remove();

            return this;
        }

        this.dealRandomCard = function() {
            var randomCard = $("#dealer-cards").children("img").eq(Math.floor(Math.random() * this.cardMax));

            randomCard.clone().appendTo("#player-cards");
            randomCard.remove();

            return this;
        }
    }

    function Player() {

        this.discardCard = function(imgID) {
           $(imgID).remove();

            console.log(imgID);
            return this;
        };

        this.addPlayerName = function() {
            var name = prompt("Please enter your name");

            if(name != null) {
                // alert(name);

                $("#player-cards").find("span").append("Name: "+name);
            }

            return this;
        };
    }


    // Create new object instance for Deck
    var dealerDeckAction = new Deck();

    // Show dealer deck when clicking reset deck
    $("#reset-deck").on("click", function(e) {
        e.preventDefault();
        dealerDeckAction.showDeck();
    });

    // When clicking #shuffle-deck link
    // execute shuffle deck function
    $("#shuffle-deck").on("click", function(e) {
        e.preventDefault();
        dealerDeckAction.shuffleDeck();
    });

    $(document).on("click", "#deal-first-card", function(e) {
        e.preventDefault();
        dealerDeckAction.dealFirstCard();
    });

    $(document).on("click", "#deal-random-card", function(e) {
        e.preventDefault();
        dealerDeckAction.dealRandomCard();
    });


    // Create new object instance for Player
    var playerHand = new Player();

    // When clicking on a card image in the player's hand
    // remove it from said player's hand
    $(document).on("click", "#player-cards > img", function(e) {
        e.preventDefault();

        playerHand.discardCard("#" + $(this).attr('id'));
    });

    $("#add-name").on("click", function(e) {
        e.preventDefault();

        playerHand.addPlayerName();
    });

});