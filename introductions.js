let questionsList = [
        {
            question:"What is one way of greeting a group of people?",
            answer:[
            {questionText:"Nǐ hǎo", isCorrect: false},
            {questionText:"Wǒ hǎo", isCorrect: false},
            {questionText:"Tā hǎo", isCorrect: false},
            {questionText:"Dàjiā hǎo", isCorrect: true}
            ]
        },
        {
            question:"'Hěn gāoxìng rènshì nǐ' means:",
            answer:[
            {questionText:"My name is __", isCorrect: false},
            {questionText:"Pleased to meet you", isCorrect: true},
            {questionText:"Long time no see", isCorrect: false},
            {questionText:"How are you?", isCorrect: false}
            ]
        },
        {
            question:"The word 'Wǒ' means:",
            answer:[
            {questionText:"You", isCorrect: false},
            {questionText:"He/him", isCorrect: false},
            {questionText:"I/Me", isCorrect: true},
            {questionText:"She/her", isCorrect: false}
            ]
            },
        {
            question:"How would you say 'My name is XX'?",
            answer:[
            {questionText:"Wǒ jiào XX", isCorrect: true},
            {questionText:"Wǒ xǐhuān XX", isCorrect: false},
            {questionText:"Wǒ yǒu XX", isCorrect: false},
            {questionText:"Wǒ yào", isCorrect: false}
            ]
            },
        {
            question:"The word 'de' is used:",
            answer:[
            {questionText:"To imply ownership of something", isCorrect: true},
            {questionText:"To imply sorrow", isCorrect: false},
            {questionText:"To imply happiness", isCorrect: false},
            {questionText:"It means none of the above", isCorrect: false}
            ]
            }
    ];
let questionText;
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
    startButton.style.display = "none"
    hideTitle.style.display = "none";
    hideText.style.display = "none";
    vocabularyClass.classList.add("hidden_items");
    questionSection.classList.remove("hidden_items");
    print();
    buttonListener();
}


function print() {
    let questionText = document.getElementById("question_text");
    let answerText = document.querySelectorAll(".button");
    questionText.innerHTML = questionsList[questionCount].question;
    let count = 0;
    for (let answer of questionsList[questionCount].answer) {
        answerText[count].innerText = (answer.questionText);
        count += 1;
    }
}

// Function for allowing each button to have a response and once the amount of answers equals the amount of questions, call the checkAnswers function
function buttonListener() {
    let button = document.querySelectorAll(".button")
    for (let buttonCount = 0; buttonCount < button.length; buttonCount++) {
    button[buttonCount].addEventListener("click", function() {
        if (answerList.length != questionsList.length -1) {
            answerList.push(buttonCount);
            increment();
        }
        else {
            answerList.push(buttonCount);
            checkAnswers();
        }
        })
    }
}

//Increments the question count by one and prints the new set of questions
function increment() {
    questionCount += 1;
    print();
}

function getCookie() {
    let myCookie = document.cookie;
    let cookieArray = myCookie.split(';');
    for (let cookieCount=0; cookieCount<cookieArray.length; cookieCount++) {
        let name = cookieArray[cookieCount].split('=')[0];
        let value = cookieArray[cookieCount].split('=')[1];
        if (name === "user_id") {
            return value;
        }
    }
}

function checkAnswers() {
    for (let answerCounter = 0; answerCounter < questionsList.length; answerCounter++) {
        if (questionsList[answerCounter].answer[answerList[answerCounter]].isCorrect === true) {
            correctCount++;
            }
    }
    let user_id = getCookie();
    let scoreTextElement = document.createElement("h1");
    if (correctCount === 1) {
        scoreTextElement.innerHTML = "You got " + correctCount + " question correct.";
    }
    else {
        scoreTextElement.innerHTML = "You got " + correctCount + " questions correct.";
    }
    document.getElementById("outer_box").insertBefore(scoreTextElement, questions_box)
    let questionSection = document.querySelector("#questions_box")
    questionSection.classList.add("hidden_items");
    let quiz_name = "introductions_quiz_score";
    let url = 'store_score.py?quiz=' + quiz_name + '&user_score=' + correctCount + '&user_id=' + user_id;
    scoreRequest = new XMLHttpRequest();
    scoreRequest.addEventListener("readystatechange", responseHandler, false);
    scoreRequest.open("GET", url, true);
    scoreRequest.send(null);
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
