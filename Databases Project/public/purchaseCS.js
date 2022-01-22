document.getElementById('purchaseDate').value = new Date().toISOString().slice(0, 10);
console.log(document.getElementById('purchaseDate').value)

document.getElementById('purchaseSubmit').addEventListener('click', function (e) {
    
  e.preventDefault();

  let vid = document.getElementById("vid");
  let purchaseDate = document.getElementById("purchaseDate");
  let vidVal = vid.value;
  let purchaseDateVal = purchaseDate.value;

  let data = {
      vid: vidVal,
      purchaseDate: purchaseDateVal
  }
  var req = new XMLHttpRequest();
  req.open("POST", "/add-purchase", true);
  req.setRequestHeader("Content-type", "application/json");

  req.onreadystatechange = () => {
      if (req.readyState == 4 && req.status == 200) {
          displayPurchase(req.response);
          vid.value = '';
          purchaseDate.value = new Date().toISOString().slice(0, 10);
      }
      else if (req.readyState == 4 && req.status != 200) {
          console.log("There was an error with the input.")
      }
  }
  console.log(data)
  req.send(JSON.stringify(data));

  document.getElementById('itemAdd').addEventListener('click', function(e) {
    e.preventDefault();

    let pid = document.getElementById("pid");
    let purid = document.getElementById("purid");
    let quantity = document.getElementById("quantity");
    let pidVal = pid.value;
    let puridVal = purid.value;
    let quantityVal = quantity.value;

    let data = {
        pid: pidVal,
        purid: puridVal,
        quantity: quantityVal,
    }
    var req = new XMLHttpRequest();
    req.open("POST", "/add-product-purchase", true);
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

displayPurchase = (data) => {
  document.getElementById("transactionDisplay").style.display = "block";
  document.getElementById("addProduct").style.display = "block";
  let parsedData = JSON.parse(data);
  let newPurchase = parsedData[parsedData.length - 1];
  document.getElementById("newpurid").innerText = newPurchase.purchaseID;
  document.getElementById("purid").value = newPurchase.purchaseID;  //sets hidden sid input value to that of the new sale
  document.getElementById("newpurchaseDate").innerText = newPurchase.purchaseDate;
  document.getElementById("newvid").innerText = newPurchase.vid;
  document.getElementById("newtotalPaid").innerText = newPurchase.totalPaid;
};

displayLineItem = (data) => {
  let currentTable = document.getElementById("itemizedPurchase");
  let newRowIndex = currentTable.rows.length;
  let parsedData = JSON.parse(data);
  let newRow = parsedData[parsedData.length - 1]
  let row = document.createElement("TR");
  let pidCell = document.createElement("TD");
  let companyCostCell = document.createElement("TD");
  let quantityCell = document.createElement("TD");
  let totalPaidCell = document.createElement("TD");
  let delCell = document.createElement("TD");
  let delButton = document.createElement("button")
  delButton.innerText = "Delete"
  delButton.id = 
  delCell.appendChild(delButton)
  pidCell.innerText = newRow.pid;
  companyCostCell.innerText = newRow.companyCost;
  quantityCell.innerText = newRow.quantity;
  totalPaidCell.innerText = newRow.totalPaid;
  row.appendChild(pidCell);
  row.appendChild(companyCostCell);
  row.appendChild(quantityCell);
  row.appendChild(totalPaidCell);
  row.appendChild(delCell)
  currentTable.appendChild(row);
  bindDelete(delButton);
};

bindDelete = (delButton) => {
  delButton.addEventListener('click', function(e) {
    e.preventDefault();
    let row = delButton.parentNode.parentNode 
    let puridVal = document.getElementById('newpurid').innerText
    let pidVal = row.firstElementChild.innerText

    let data = {
        pid: pidVal,
        purid: puridVal,
    }
    var req = new XMLHttpRequest();
    req.open("DELETE", "/delete-product-purchase", true);
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

