<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Skin Type Quiz</title>
    <style>
        body {
            background-color: #DDD8CA;
            color: #20321E;
            font-family: "Times New Roman", Times, serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
            box-sizing: border-box;
        }
        .quiz-container {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 8px;
            width: 100%;
            max-width: 600px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            text-align: center;
        }
        h1 {
            margin-bottom: 20px;
        }
        .question {
            font-size: 1.2em;
            margin-bottom: 15px;
        }
        .options {
            list-style: none;
            padding: 0;
            margin-bottom: 20px;
        }
        .options li {
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            font-size: 1em;
        }
        .options li::before {
            content: "→";
            margin-right: 8px;
            color: #20321E;
        }
        .nav-buttons {
            display: flex;
            justify-content: space-between;
            margin-top: 20px;
        }
        .nav-buttons button {
            background-color: #20321E;
            color: #FFF;
            border: none;
            padding: 10px 20px;
            font-size: 1em;
            cursor: pointer;
            border-radius: 4px;
        }
        .nav-buttons button:disabled {
            background-color: #AAA;
        }
        .result {
            margin-top: 20px;
            font-size: 1.2em;
            color: #20321E;
            text-align: left;
        }
        .error {
            color: red;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="quiz-container">
        <h1>Skin Type Quiz</h1>
        <form id="quizForm">
            <div id="questionContainer"></div>
            <div class="nav-buttons">
                <button type="button" id="backButton" onclick="goBack()" disabled>Back</button>
                <button type="button" id="nextButton" onclick="goNext()">Next</button>
            </div>
            <div id="errorContainer" class="error" style="display: none;"></div>
        </form>
        <div id="resultContainer" class="result" style="display: none;"></div>
    </div>

    <script>
        // Array of questions and options
        const questions = [
            {
                question: "How does your skin feel after washing?",
                options: [
                    { text: "Dry and tight", value: "Dry" },
                    { text: "Shiny and greasy", value: "Oily" },
                    { text: "Normal, not too dry or oily", value: "Combination" },
                    { text: "Red and irritated", value: "Sensitive" }
                ]
            },
            {
                question: "How often do you experience breakouts?",
                options: [
                    { text: "Rarely", value: "Dry" },
                    { text: "Frequently", value: "Oily" },
                    { text: "Occasionally", value: "Combination" },
                    { text: "Triggered by specific products", value: "Sensitive" }
                ]
            },
            {
                question: "What best describes your skin's texture?",
                options: [
                    { text: "Flaky or rough", value: "Dry" },
                    { text: "Smooth but oily", value: "Oily" },
                    { text: "Combination of both", value: "Combination" },
                    { text: "Thin and sensitive", value: "Sensitive" }
                ]
            },
            {
                question: "Do you often feel itchy or irritated?",
                options: [
                    { text: "Yes, very often", value: "Sensitive" },
                    { text: "Sometimes", value: "Dry" },
                    { text: "Rarely", value: "Combination" },
                    { text: "Never", value: "Oily" }
                ]
            },
            {
                question: "How often do you moisturize your skin?",
                options: [
                    { text: "Never", value: "Oily" },
                    { text: "Sometimes", value: "Combination" },
                    { text: "Always", value: "Dry" },
                    { text: "As needed", value: "Sensitive" }
                ]
            },
            {
                question: "What is your skin's reaction to sun exposure?",
                options: [
                    { text: "Peels and burns easily", value: "Sensitive" },
                    { text: "Gets oily", value: "Oily" },
                    { text: "Tans easily", value: "Combination" },
                    { text: "Rarely reacts", value: "Dry" }
                ]
            },
            {
                question: "How often do you use makeup?",
                options: [
                    { text: "Daily", value: "Oily" },
                    { text: "Occasionally", value: "Combination" },
                    { text: "Rarely", value: "Dry" },
                    { text: "Never", value: "Sensitive" }
                ]
            },
            {
                question: "Do you have large pores?",
                options: [
                    { text: "Yes, very noticeable", value: "Oily" },
                    { text: "Somewhat noticeable", value: "Combination" },
                    { text: "Not really", value: "Dry" },
                    { text: "No", value: "Sensitive" }
                ]
            },
            {
                question: "Is your skin prone to redness?",
                options: [
                    { text: "Yes, often", value: "Sensitive" },
                    { text: "Sometimes", value: "Combination" },
                    { text: "Rarely", value: "Dry" },
                    { text: "Never", value: "Oily" }
                ]
            },
            {
                question: "Do you often use products for sensitive skin?",
                options: [
                    { text: "Yes, always", value: "Sensitive" },
                    { text: "Sometimes", value: "Dry" },
                    { text: "Rarely", value: "Combination" },
                    { text: "Never", value: "Oily" }
                ]
            }
        ];

        let currentQuestionIndex = 0;
        const selectedAnswers = new Array(questions.length).fill(null);

        // Function to load a question
        function loadQuestion() {
            const questionContainer = document.getElementById("questionContainer");
            const question = questions[currentQuestionIndex];

            questionContainer.innerHTML = `
                <p class="question">${currentQuestionIndex + 1}. ${question.question}</p>
                <ul class="options">
                    ${question.options.map((option, index) => {
                        const checked = selectedAnswers[currentQuestionIndex] === option.value ? 'checked' : '';
                        return `
                            <li>
                                <input type="radio" name="answer" value="${option.value}" id="option${currentQuestionIndex}${index}" ${checked} required>
                                <label for="option${currentQuestionIndex}${index}">${option.text}</label>
                            </li>
                        `;
                    }).join('')}
                </ul>
            `;

            document.getElementById("backButton").disabled = currentQuestionIndex === 0;
            document.getElementById("nextButton").textContent = currentQuestionIndex === questions.length - 1 ? "Submit" : "Next";
            document.getElementById("errorContainer").style.display = "none"; // Hide error message
        }

        // Function to go to the next question
        function goNext() {
            // Store the selected answer
            const selected = document.querySelector('input[name="answer"]:checked');
            if (selected) {
                selectedAnswers[currentQuestionIndex] = selected.value;

                // Move to the next question or submit
                if (currentQuestionIndex < questions.length - 1) {
                    currentQuestionIndex++;
                    loadQuestion();
                } else {
                    // Analyze answers and recommend products
                    recommendProducts();
                }
            } else {
                // Show error message if no option is selected
                document.getElementById("errorContainer").textContent = "Please select an option before proceeding.";
                document.getElementById("errorContainer").style.display = "block";
            }
        }

        // Function to go back to the previous question
        function goBack() {
            if (currentQuestionIndex > 0) {
                currentQuestionIndex--;
                loadQuestion();
            }
        }

        // Function to recommend products, ingredients, and tips based on the selected answers
        function recommendProducts() {
            const recommendations = {
                "Dry": {
                    products: "Recommended Products: Hydrating Cream Cleanser with hyaluronic acid and glycerin, Rich Moisturizer with ceramides and essential fatty acids, Overnight Moisture Mask with shea butter and squalane.",
                    bestIngredients: "Best Ingredients: Hyaluronic Acid: Provides intense hydration, Glycerin and Ceramides: Restore the skin barrier, Squalane: Adds moisture without a heavy feel.",
                    avoidIngredients: "Ingredients to Avoid: Alcohol in toners or serums: Strips moisture, Sulfates in cleansers can dry out skin further.",
                    tips: "Tips: Use lukewarm water, as hot water strips oils, Apply moisturizer on damp skin to lock in moisture, Incorporate hydrating serums under your moisturizer."
                },
                "Oily": {
                    products: "Recommended Products: Oil Control Cleanser with tea tree and salicylic acid, Lightweight Gel Moisturizer with hyaluronic acid and niacinamide, Clay Mask with bentonite or kaolin clay for weekly use.",
                    bestIngredients: "Best Ingredients: Salicylic Acid: Clears pores and reduces oiliness, Niacinamide: Balances oil production and soothes skin, Tea Tree Oil: Natural antibacterial to prevent breakouts.",
                    avoidIngredients: "Ingredients to Avoid: Coconut Oil and Mineral Oil: Clog pores, Heavy Butters like shea butter can be too rich.",
                    tips: "Tips: Use a gentle cleanser twice daily, Don’t skip moisturizer; opt for oil-free, lightweight options, Exfoliate weekly to prevent clogged pores." 
                },
                "Combination": {
                    products: "Recommended Products: Balancing Gel Cleanser with mild acids like lactic acid, Light Moisturizer with ceramides and hyaluronic acid, Clay Mask for T-zone use, and Moisture Mask for dry areas.",
                    bestIngredients: "Best Ingredients: Lactic Acid: Gently exfoliates and hydrates, Hyaluronic Acid: Balances moisture across skin, Witch Hazel: Controls oil in the T-zone.",
                    avoidIngredients: "Ingredients to Avoid: Heavy Oils in the T-zone: Can increase oiliness, High-Strength Acids: May be too harsh.",
                    tips: "Tips: Treat different areas according to their needs (e.g., T-zone vs. cheeks), Use a lightweight moisturizer across the face, Multi-mask by using different masks on different areas."
                },
                "Sensitive": {
                    products: "Recommended Products: Gentle Cream Cleanser with chamomile and aloe, Soothing Serum with centella asiatica (cica), Calming Moisturizer with oatmeal and licorice root extract.",
                    bestIngredients: "Best Ingredients: Aloe Vera and Chamomile: Reduce inflammation, Centella Asiatica (Cica): Soothes sensitive, irritated skin, Oat Extract: Helps calm and protect skin.",
                    avoidIngredients: "Ingredients to Avoid: Fragrance and Essential Oils: Can cause irritation, Alcohol: Dries and irritates sensitive skin.",
                    tips: "Tips: Patch test new products before use, Keep your routine minimal and avoid harsh exfoliants, Look for hypoallergenic products."
                }
            };

            // Count occurrences of each skin type
            const skinTypeCounts = {};
            selectedAnswers.forEach(answer => {
                skinTypeCounts[answer] = (skinTypeCounts[answer] || 0) + 1;
            });

            // Determine the most selected skin type
            let mostSelectedSkinType = Object.keys(skinTypeCounts).reduce((a, b) => 
                skinTypeCounts[a] > skinTypeCounts[b] ? a : b
            );

            // Show the recommendation
            const resultContainer = document.getElementById("resultContainer");
            resultContainer.style.display = "block";
            resultContainer.innerHTML = `
                <p>Your skin type is likely: <strong>${mostSelectedSkinType}</strong></p>
                <p>${recommendations[mostSelectedSkinType].products}</p>
                <p>${recommendations[mostSelectedSkinType].bestIngredients}</p>
                <p>${recommendations[mostSelectedSkinType].avoidIngredients}</p>
                <p>${recommendations[mostSelectedSkinType].tips}</p>
            `;
            document.getElementById("questionContainer").style.display = "none";
            document.getElementById("backButton").style.display = "none";
            document.getElementById("nextButton").style.display = "none";
        }

        // Initialize the first question
        loadQuestion();
    </script>
</body>
</html>
