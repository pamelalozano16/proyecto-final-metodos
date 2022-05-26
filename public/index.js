async function getDrink() {
  let cantidad = document.getElementById("cantidad").value;
  let ingrediente = document.getElementById("ingrediente").value;
  console.log(cantidad, ingrediente);

  const resp = await fetch(
    "/getDrink?amount=" + cantidad + "&ingredient=" + ingrediente
  );
  const respString = (await resp.json()).result;
  document.getElementById("result").innerHTML = respString;
}
