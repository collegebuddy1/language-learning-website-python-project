let questionsList = [
        {
            question:"What does 'Jiǔ' mean?",
            answer:[
            {questionText:"Long (with relation to time)", isCorrect: true},
            {questionText:"Long (with relation to distance)", isCorrect: false},
            {questionText:"Short (with relation to time)", isCorrect: false},
            {questionText:"Short (with relation to distance)", isCorrect: false}
            ]
        },
        {
            question:"'Zuìjìnguò de zěnyàng' means:",
            answer:[
            {questionText:"Not bad", isCorrect: false},
            {questionText:"Long time no see", isCorrect: false},
            {questionText:"How have things gone recently?", isCorrect: true},
            {questionText:"Have you eaten?", isCorrect: false}
            ]
        },
        {
            question:"How would you ask somebody if they already ate?",
            answer:[
            {questionText:"Hǎojiǔ", isCorrect: false},
            {questionText:"Bùjiàn", isCorrect: false},
            {questionText:"Hái bùcuò", isCorrect: false},
            {questionText:"Nǐ chīfàn le ma", isCorrect: true}
            ]
            },
        {
            question:"How would you reply if someone asked you 'Zuìjìnguò de zěnyàng'?",
            answer:[
            {questionText:"Nǐ chīfàn le ma", isCorrect: false},
            {questionText:"Hǎo bùcuò", isCorrect: true},
            {questionText:"Hǎojiǔ bùjiàn", isCorrect: false},
            {questionText:"Nǐ hǎo", isCorrect: false}
            ]
            },
    ];
let questionCount = 0;
let answerList = [];
let correctCount = 0;
let scoreRequest;

if (document.querySelector("#start") !== null) {
    let startButton = document.querySelector("#start");
    startButton.addEventListener("click", init, false);
}

function init() {
	let vocabularyClass = document.querySelector(".vocabulary");
    let startButton = document.querySelector("#start");
    let questionSection = document.getElementById("questions_box");
    let hideTitle = document.querySelector("#outer_box h1");
    let hideText = document.querySelector("#outer_box p");
    hideTitle.style.display = "none";
    hideText.style.display = "none";
    vocabularyClass.classList.add("hidden_items");
    startButton.classList.add("hidden_items");
    questionSection.classList.remove("hidden_items");
    print()
    buttonListener()
}

// - Prints out the current question to be displayed as well as mapping each answer to a button
function print() {
    let questionText = document.getElementById("question_text");
    let answerText = document.querySelectorAll(".button");
    questionText.innerHTML = questionsList[questionCount].question;
    let count = 0;
    for (let answer of questionsList[questionCount].answer) {
        answerText[count].innerText = (answer.questionText)
        count += 1
    }

}

// - Adds a button listener to each button.
// - If the total answers is not equal to the total questions, it adds the answer to an array and calls the increment function
// - Once the amount of questions answered equals the total number of questions, calls the checkAnswers function
function buttonListener() {
    let button = document.querySelectorAll(".button")
    for (let buttonCount = 0; buttonCount < button.length; buttonCount++) {
    button[buttonCount].addEventListener("click", function() {
        if (answerList.length != questionsList.length -1) {
            answerList.push(buttonCount)
            increment()
        }
        else {
            answerList.push(buttonCount)
            checkAnswers()
        }
        })
    }
}

// - Increments the question count by one and prints the new set of questions
function increment() {
    questionCount += 1
    print()
}

// - Searchs cookies in header for a user ID
function getCookie() {
    let myCookie = document.cookie;
    let cookieArray = myCookie.split(';');
    for (let cookieCount=0; cookieCount < cookieArray.length; cookieCount++) {
        let name = cookieArray[cookieCount].split('=')[0];
        let value = cookieArray[cookieCount].split('=')[1];
        if (name === "user_id") {
            return value
        }
    }
}

// - Checks the user answers against the correct answerList
// - Sends the results to a database
function checkAnswers() {
    for (let answerCounter = 0; answerCounter < questionsList.length; answerCounter++) {
        if (questionsList[answerCounter].answer[answerList[answerCounter]].isCorrect === true) {
            correctCount++
            }
    }
    let user_id = getCookie();
    let scoreTextElement = document.createElement("h1");
    scoreTextElement.innerHTML = "You got " + correctCount + " questions correct.";
    if (correctCount === 1) {
        scoreTextElement.innerHTML = "You got " + correctCount + " question correct.";
    }
    else {
        scoreTextElement.innerHTML = "You got " + correctCount + " questions correct.";
    }
    document.getElementById("outer_box").insertBefore(scoreTextElement, questions_box);
    let questionSection = document.querySelector("#questions_box");
    questionSection.classList.add("hidden_items");
    let quiz_name = "acquaintances_quiz_score"
    let url = 'store_score.py?quiz=' + quiz_name + '&user_score=' + correctCount + '&user_id=' + user_id;
    scoreRequest = new XMLHttpRequest();
    scoreRequest.addEventListener("readystatechange", responseHandler, false);
    scoreRequest.open("GET", url, true);
    scoreRequest.send(null);
    responseHandler();
}

function responseHandler() {
    let scoreTextElement = document.querySelector("#outer_box h1 ~ h1");
    if (scoreRequest.readyState === 4) {
        if (scoreRequest.status === 200) {
            if (scoreRequest.responseText.trim() === "Success") {
                scoreTextElement.textContent += " Thanks for playing.";
            }
            else {
                scoreTextElement.textContent += " However there was an issue saving the data.";
            }
        }
    }
}
