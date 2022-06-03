const express = require('express')
const path = require('path')
const hbs = require ('hbs')
const dotenv = require("dotenv");
const publicPath = path.join(__dirname, "../public");
const templatePath = path.join(__dirname, "../templates");
const partialsPath = path.join(__dirname, "../templates/partials");

dotenv.config();

const port = process.env.PORT;
const app = express()
app.use(express.json())
app.set('view engine', 'hbs')
app.set('views', templatePath)

app.use(express.static(publicPath))
hbs.registerPartials(partialsPath)

app.get('/', (req, res)=>{
    res.render('index')
})

app.get("/getDrink", async (req, res) => {
  console.log(req.query);
  try {
    var spawn = require("child_process").spawn;
    var pyProg = spawn(
      "python3",
      ["./scripts/hmm.py", req.query.ingredient, Number(req.query.amount)],
      {
        cwd: __dirname,
      }
    );
    let result;
    pyProg.stdout.on("data", function (data) {
      result = data.toString();
    });
    pyProg.stderr.on("data", (data) => {
      console.log(data.toString());
    });
    pyProg.stderr.on("close", () => {
      console.log("DONE: ", result);
      res.status(200).send({ result });
    });
  } catch (e) {
    console.log(e);
    return res.status(500).send(e.body);
  }
});


app.listen(port, ()=>{
    console.log('Server is up on 3000')
})