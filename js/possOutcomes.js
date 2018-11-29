function getInputs(){
    var tb = document.querySelector('input[name="topBottom"]:checked').value;
    var inning = document.getElementById("inning").value
    var totalInning = tb + "" + inning;
    var outs = document.querySelector('input[name="outs"]:checked').value;
    var first = document.getElementById("first").checked ? 1 : 0
    var second = document.getElementById("second").checked ? 1 : 0
    var third = document.getElementById("third").checked ? 1 : 0
    var scoreDiff = gameScoreDiff
    var strikes = document.querySelector('input[name="strikes"]:checked').value;
    var balls = document.querySelector('input[name="balls"]:checked').value;

    return {
        'inning':totalInning,
        'outs':outs,
        'first':first,
        'second':second,
        'third':third,
        'scoreDiff':scoreDiff,
        'strikes':strikes,
        'balls':balls
    }
}

function givenOrDefault(given, def, type) {
    if (typeof given[type] !== 'undefined') {
        return given[type];
    } else {
        return def[type];
    }
}
function getResults(inputDict,changes) {
    const inpInning = givenOrDefault(changes,inputDict,'inning');
    const inpScoreDiff = givenOrDefault(changes,inputDict,'scoreDiff');
    const inpOuts = givenOrDefault(changes,inputDict,'outs');
    const inpBalls = givenOrDefault(changes,inputDict,'balls');
    const inpStrikes = givenOrDefault(changes,inputDict,'strikes');
    const inpFirst = givenOrDefault(changes,inputDict,'first');
    const inpSecond = givenOrDefault(changes,inputDict,'second');
    const inpThird = givenOrDefault(changes,inputDict,'third');
    return jsonResults[inpInning][inpScoreDiff][inpOuts][inpBalls][inpStrikes][inpFirst][inpSecond][inpThird];
}

function appendToOutcomeList(item){
    const outcomeList = document.getElementById('outcomeList');
    var node = document.createElement("LI");
    var textnode = document.createTextNode(item);
    node.appendChild(textnode);
    outcomeList.appendChild(node);
}
function seePossOutcomes(inputDict){
    document.getElementById('outcomeList').innerHTML = "";
    const ballOutcome = ball(inputDict);
    const strikeOutcome = strike(inputDict);
    const walkOutcome = walk(inputDict);
    if(ballOutcome){
        appendToOutcomeList("Ball: " + getProbability(ballOutcome));
    }
    if(walkOutcome){
        appendToOutcomeList("Walk: " + getProbability(walkOutcome));
    }
    if(strikeOutcome){
        appendToOutcomeList("Strike: " + getProbability(strikeOutcome));
    }
}

function getProbability(outcome){
    return (outcome['1'] / (outcome['0'] + outcome['1']) * 100).toFixed(2) + "%";
}

function ball(inputDict){
    let balls = parseInt(inputDict['balls']);
    if(balls == 3){
        return;
    }
    balls++;
    const changes = {
        'balls' :balls
    }
    return getResults(inputDict, changes);
}

function strike(inputDict){
    let strikes = parseInt(inputDict['strikes']);
    if(strikes == 2){
        return;
    }
    strikes++;
    const changes = {
        'strikes' :strikes
    }
    return getResults(inputDict, changes);
}

function walk(inputDict){
    if(inputDict['balls'] != 3){
        return;
    }
    let first = inputDict['first'];
    let second = inputDict['second'];
    let third = inputDict['third'];
    let scoreDiff = inputDict['scoreDiff'];
    if(first == 1){
        if(second == 1){
            if(third == 1){
                if(inputDict['inning'].charAt(0) == '0'){
                    scoreDiff --;
                }
                else{
                    scoreDiff ++;
                }
            }
            third = 1;
        }
        second = 1;
    }
    first = 1;
    const changes = {
        'balls': 0,
        'strikes': 0,
        'first': first,
        'second':second,
        'third': third,
        'scoreDiff': scoreDiff
    }
    return getResults(inputDict,changes);
}

function strikeOut(inputDict){
    if(inputDict['strikes'] != 3){
        return;
    }
    if(inputDict['outs'] == 2){
        return;
    }
}