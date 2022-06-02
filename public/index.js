document.getElementById("spinner").style.display = "none";
document.getElementById("loaded").style.display = "block";

const licor = [
  "gin",
  "vermouth rosso",
  "campari",
  "tonic",
  "bourbon",
  "rye whiskey",
  "coffee liqueur",
  "vermouth",
  "whiskey",
  "tequila",
  "orange liqueur",
  "sweet vermouth",
  "white rum",
  "peach schnapps",
  "vodka",
  "raspberry liqueur",
  "prosecco",
  "aperol",
  "triple sec",
  "bourbon whiskey",
  "claret wine",
  "rum",
  "scotch",
  "ginger beer",
  "pisco",
  "cognac",
  "liqueur",
  "dark rum",
  "orgeat",
  "blended scotch",
];
const drops = [
  "bitters",
  "orange bitters",
  "angostura bitters",
  "angostura bitter",
  "tabasco",
];
const spices = ["sugar cube", "salt", "black pepper"];
const cascaras = ["orange peel", "lemon peel"];
const nonLicor = [
  "water",
  "lemon juice",
  "lime juice",
  "syrup",
  "orange juice",
  "pineapple juice",
  "cranberry juice",
  "soda water",
  "coconut juice",
  "honey-ginger syrup",
  "tomato juice",
  "raspberry syrup",
  "grapefruit juice",
];
const coffee = ["espresso"];
const misc = ["blackberries", "mint leaves"];

async function getDrink() {
  let cantidad = document.getElementById("cantidad").value;
  let ingrediente = document.getElementById("ingrediente").value;
  console.log(cantidad, ingrediente);
  document.getElementById("spinner").style.display = "block";
  document.getElementById("loaded").style.display = "none";
  const resp = await fetch(
    "/getDrink?amount=" + cantidad + "&ingredient=" + ingrediente
  );
  const respString = (await resp.json()).result;

  const elemArray = respString.split(",");
  let map = {};
  console.log(elemArray);

  for (i in elemArray) {
    elemArray[i] = elemArray[i].replace("\n", "");
    if (!map[elemArray[i]]) {
      map[elemArray[i]] = 1;
    } else {
      map[elemArray[i]]++;
    }
  }
  tableString = "";
  for (let i in map) {
    console.log(map[i]);
    tableString += "<tr><td>" + i + "</td>";
    if (licor.includes(i)) {
      tableString += "<td>" + map[i] + " oz </td>";
    } else if (drops.includes(i)) {
      tableString += "<td>" + map[i] * 2 + " drops </td>";
    } else if (spices.includes(i)) {
      tableString += "<td>" + map[i] + " pizcas </td>";
    } else if (cascaras.includes(i)) {
      tableString += "<td>" + map[i] + " pedazos </td>";
    } else if (nonLicor.includes(i)) {
      tableString += "<td>" + map[i] * 2 + " oz </td>";
    } else if (coffee.includes(i)) {
      tableString += "<td>" + map[i] + " shot </td>";
    } else {
      tableString += "<td>" + map[i] + " pz </td>";
    }
    tableString += "</tr>";
  }
  $("#table-result").find("tbody").html("");
  $("#table-result").find("tbody").append(tableString);

  //document.getElementById("result").innerHTML = respString;

  document.getElementById("spinner").style.display = "none";
  document.getElementById("loaded").style.display = "block";
}
