document.getElementById('saleDate').value = new Date().toISOString().slice(0, 10);

document.getElementById('saleSubmit').addEventListener('click', function (e) {
    
  e.preventDefault();

  let cid = document.getElementById("cid");
  let saleDate = document.getElementById("saleDate");
  let paymentMethod = document.getElementById("paymentMethod");
  let cidVal = cid.value;
  let saleDateVal = saleDate.value;
  let paymentMethodVal = paymentMethod.value;

  let data = {
      cid: cidVal,
      saleDate: saleDateVal,
      paymentMethod: paymentMethodVal,
  }
  var req = new XMLHttpRequest();
  req.open("POST", "/add-sale", true);
  req.setRequestHeader("Content-type", "application/json");

  req.onreadystatechange = () => {
      if (req.readyState == 4 && req.status == 200) {
          displaySale(req.response);
          cid.value = '';
          saleDate.value = new Date().toISOString().slice(0, 10);
          paymentMethod.value = '';
      }
      else if (req.readyState == 4 && req.status != 200) {
          console.log("There was an error with the input.")
      }
  }
  req.send(JSON.stringify(data));

  document.getElementById('itemAdd').addEventListener('click', function(e) {
    e.preventDefault();

    let pid = document.getElementById("pid");
    let sid = document.getElementById("sid");
    let quantity = document.getElementById("quantity");
    let pidVal = pid.value;
    let sidVal = sid.value;
    let quantityVal = quantity.value;

    let data = {
        pid: pidVal,
        sid: sidVal,
        quantity: quantityVal,
    }
    var req = new XMLHttpRequest();
    req.open("POST", "/add-product-sale", true);
    req.setRequestHeader("Content-type", "application/json");

    req.onreadystatechange = () => {
        if (req.readyState == 4 && req.status == 200) {
            displayLineItem(req.response);
            pid.value = '';
            quantity.value = '';
        }
        else if (req.readyState == 4 && req.status != 200) {
            console.log("There was an error with the input.")
        }
    }
    req.send(JSON.stringify(data));
  });
});

displaySale = (data) => {
  document.getElementById("transactionDisplay").style.display = "block";
  document.getElementById("addProduct").style.display = "block";
  let parsedData = JSON.parse(data);
  let newSale = parsedData[parsedData.length - 1];
  document.getElementById("newsid").innerText = newSale.saleID;
  document.getElementById("sid").value = newSale.saleID;  //sets hidden sid input value to that of the new sale
  document.getElementById("newsaleDate").innerText = newSale.saleDate;
  document.getElementById("newcid").innerText = newSale.cid;
  document.getElementById("newtotalPrice").innerText = newSale.totalPrice;
};

displayLineItem = (data) => {
  let currentTable = document.getElementById("itemizedSale");
  let newRowIndex = currentTable.rows.length;
  let parsedData = JSON.parse(data);
  let newRow = parsedData[parsedData.length - 1]
  let row = document.createElement("TR");
  let pidCell = document.createElement("TD");
  let salePriceCell = document.createElement("TD");
  let quantityCell = document.createElement("TD");
  let totalPriceCell = document.createElement("TD");
  let delCell = document.createElement("TD");
  let delButton = document.createElement("button")
  console.log(newRow)
  delButton.innerText = "Delete"
  delCell.appendChild(delButton)
  pidCell.innerText = newRow.pid;
  salePriceCell.innerText = newRow.salePrice;
  quantityCell.innerText = newRow.quantity;
  totalPriceCell.innerText = newRow.totalPrice;
  row.appendChild(pidCell);
  row.appendChild(salePriceCell);
  row.appendChild(quantityCell);
  row.appendChild(totalPriceCell);
  row.appendChild(delCell)
  currentTable.appendChild(row);
  bindDelete(delButton);
};

bindDelete = (delButton) => {
  delButton.addEventListener('click', function(e) {
    e.preventDefault();
    let row = delButton.parentNode.parentNode 
    let sidVal = document.getElementById('newsid').innerText
    let pidVal = row.firstElementChild.innerText

    let data = {
        pid: pidVal,
        sid: sidVal,
    }
    var req = new XMLHttpRequest();
    req.open("DELETE", "/delete-product-sale", true);
    req.setRequestHeader("Content-type", "application/json");

    req.onreadystatechange = () => {
        if (req.readyState == 4 && req.status == 200) {
          row.remove();
        }
        else if (req.readyState == 4 && req.status != 200) {
            console.log("There was an error with the input.")
        }
    }
    req.send(JSON.stringify(data));
  });
};