const express = require("express");
const bodyParser = require("body-parser");
const { PythonShell } = require("python-shell");
const fetch = require("node-fetch");
const natural = require("natural");
const app = express();
const tokenizer = new natural.WordTokenizer();
const port = process.env.PORT || 3000;
const apiUrl = "http://localhost:5000/predict";
const inputUrl = "https://amazon.com";

app.use(bodyParser.json());


const loadModel = () => {
  PythonShell.run("load_model.py", null, (err) => {
    if (err) {
      console.error(err);
    } else {
      console.log("Model loaded successfully.");
    }
  });
};


app.get("/load-model", (req, res) => {
  loadModel();
  res.send("Loading the model...");
});




app.post("/predict", (req, res) => {
  const inputData = req.body;


  const tokenizedInput = tokenizeURL(inputData.url);

  const maxLength = 100;
  const paddedInput = padArray(tokenizedInput, maxLength);

  fetch(apiUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url: inputData.url }), 
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Prediction:", data.prediction);

  
      PythonShell.run(
        "./predict.py",
        { args: [JSON.stringify(paddedInput)] },
        (err, results) => {
          if (err) {
            console.error(err);
            res.status(500).send("Error making predictions.");
          } else {
            const prediction = JSON.parse(results[0]);
            res.json({ prediction });
          }
        }
      );
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});

function tokenizeURL(url) {

  return url.split(/[^a-zA-Z0-9]+/);
}


function padArray(arr, length) {
  while (arr.length < length) {
    arr.push(""); 
  }
  return arr.slice(0, length); 
}

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
  loadModel();
});
