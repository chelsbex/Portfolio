var express = require('express');
var db = require('./database/dbcon.js');
var app = express();
var exphbs = require('express-handlebars').create({defaultLayout:'main'});

app.engine('handlebars', exphbs.engine)
app.set('view engine', 'handlebars');
app.set('port', 7715);
app.use(express.json())
app.use(express.urlencoded({extended: true}))
app.use(express.static('public'));

app.get('/', function(req,res){
  res.render('index');
});

app.get('/add-category', function(req,res){
  res.render('addCategory');
});

app.post('/new-category', function(req, res){
  let data = req.body
  query1 = `INSERT INTO Categories (name)
                   VALUES ('${data.name}');`
  db.pool.query(query1, function(error, rows, fields){
    if(error) {
      console.log(error)
      res.sendStatus(400)
    } else {
      res.send(rows)
    }
  });
});

app.get('/add-customer', function(req,res){
  res.render('addCustomer');
});

app.post('/new-customer', function(req, res){
  let data = req.body
  query1 = `INSERT INTO Customers (fname, lname, email, phoneNumber, streetAddress, city, state, countryCode, acceptingEmails) VALUES ('${data.fname}', '${data.lname}', '${data.email}', '${data.phoneNumber}', '${data.streetAddress}', '${data.city}', '${data.state}', '${data.countryCode}', '${data.emails}');`
  db.pool.query(query1, function(error, rows, fields){
    if(error) {
      console.log(error);
      res.sendStatus(400);
    } else {
      res.send(rows);
    }
  });
});

app.get('/add-product', function(req,res){
  let query1 = `SELECT * FROM Vendors;`
  let query2 = `SELECT * FROM Categories;`
  db.pool.query(query1, function(error, rows, fields){
    let vendors = rows;
    db.pool.query(query2, function(error, rows, fields){
      let categories = rows;
      res.render('addProduct', {vendors: vendors, categories: categories});
    });
  });
});     


app.post('/new-product', function(req, res){
  let data = req.body
  query1 = `INSERT into Products (vid, catid, name, companyCost, salePrice, expirationDate, stockQuant)
  VALUES ('${data.vid}', '${data.cat}', '${data.name}', '${data.companyCost}', '${data.salePrice}', '${data.expirationDate}', '${data.stockQuant}');`
  db.pool.query(query1, function(error, rows, fields){
    if (error) {
      console.log(error)
      res.sendStatus(400);
    } else {
      res.send(rows);
    }
  });
});

app.get('/add-vendor', function(req,res){
  res.render('addVendor');
});

app.post('/new-vendor', function(req, res){
  let data = req.body
  query1 = `INSERT INTO Vendors (name, email, description)
  VALUES ('${data.name}', '${data.email}', '${data.vendorDescription}');`
  db.pool.query(query1, function(error, rows, fields){
    if (error) {
      console.log(error)
      res.sendStatus(400)
    } else {
      res.send(rows)
    }
  });
});

app.get('/purchase', function(req,res){
  let query1 = `SELECT * FROM Vendors;`
  let query2 = `SELECT * FROM Products`
  db.pool.query(query1, function(error, rows, fields){
    if (error) {
        console.log(error);
        res.sendStatus(400);
    } else {
        let vendors = rows
        db.pool.query(query2, function(error, rows, fields){
          if (error) {
              console.log(error);
              res.sendStatus(400);
          } else {
            let products = rows
              res.render('purchase', {products: products, vendors: vendors});
          }
        });
    }
  });
});


app.post('/add-purchase', function(req, res) {
    let data = req.body;
    query1 = `INSERT INTO Purchases (vid, purchaseDate) VALUES ('${data.vid}', '${data.purchaseDate}');`
    db.pool.query(query1, function(error, rows, fields){
        if (error) {
            console.log(error)
            res.sendStatus(400);
        } else {
            query2 = `SELECT purchaseID, vid, DATE_FORMAT(purchaseDate, '%m-%d-%Y') AS purchaseDate, totalPaid FROM Purchases WHERE purchaseID = (SELECT max(purchaseID) FROM Purchases);`
            db.pool.query(query2, function(error, rows, fields){
                if (error) {
                    console.log(error);
                    res.sendStatus(400);
                } else {
                    res.send(rows);
                }
            })
        }
    })
});

app.post('/add-product-purchase', function(req, res) {
  let data = req.body;
  query1 = `INSERT INTO Product_Purchases (pid, purid, quantity) 
    VALUES ('${data.pid}', '${data.purid}', '${data.quantity}');`
  db.pool.query(query1, function(error, rows, fields){
    if (error) {
      console.log(error)
      res.sendStatus(400);
    } else {
      query2 = `UPDATE Purchases
        SET totalPaid = totalPaid + 
        ((SELECT quantity FROM Product_Purchases WHERE pid = ${data.pid} AND purid = ${data.purid})
        *(SELECT companyCost from Products WHERE productID = ${data.pid}))  
        WHERE purchaseID = ${data.purid};`
      db.pool.query(query2, function(error, rows, fields){
        if (error) {
            console.log(error);
            res.sendStatus(400);
        } else {
          query3 = `SELECT PP.pid, PR.companyCost, PP.quantity, P.totalPaid
            FROM Product_Purchases PP
            INNER JOIN Products PR ON PP.pid = PR.productID
            INNER JOIN Purchases P ON PP.purid = P.purchaseID 
            WHERE purid = ${data.purid};`
          db.pool.query(query3, function(error, rows, fields){
            if (error) {
              console.log(error);
              res.sendStatus(400);
            } else {
              res.send(rows);
            }
          }); 
        }
      });
    }
  });
});

app.delete('/delete-product-purchase', function(req, res) {
  let data = req.body;
  query1 = `UPDATE Purchases
    SET totalPaid = totalPaid - ((SELECT companyCost FROM Products WHERE productID = ${data.pid}) 
    *(SELECT quantity FROM Product_Purchases WHERE pid = ${data.pid} AND purid = ${data.purid}))
    WHERE purchaseID = ${data.purid};`
  db.pool.query(query1, function(error, rows, fields){
    if (error) {
      console.log(error)
      res.sendStatus(400);
    } else {
      query2 = `DELETE FROM Product_Purchases WHERE pid = ${data.pid} AND purid = ${data.purid}`
      db.pool.query(query2, function(error, rows, fields){
        if (error) {
            console.log(error);
            res.sendStatus(400);
        } else {
            res.send(rows);
        }
      });
    }
  });
});

app.get('/sale', function(req,res){
  let query1 = `SELECT customerID, CONCAT(fname, " ", lname) AS name FROM Customers;`
  let query2 = `SELECT * FROM Products`
  db.pool.query(query1, function(error, rows, fields){
    if (error) {
        console.log(error);
        res.sendStatus(400);
    } else {
        let customers = rows
        db.pool.query(query2, function(error, rows, fields){
          if (error) {
              console.log(error);
              res.sendStatus(400);
          } else {
            let products = rows
              res.render('sale', {products: products, customers: customers});
          }
        });
    }
  });
});

app.post('/add-sale', function(req, res) {
    let data = req.body;
    query1 = `INSERT INTO Sales (cid, saleDate, paymentMethod) VALUES ('${data.cid}', '${data.saleDate}', '${data.paymentMethod}');`
    db.pool.query(query1, function(error, rows, fields){
      if (error) {
        console.log(error)
        res.sendStatus(400);
      } else {
        query2 = `SELECT saleID, cid, DATE_FORMAT(saleDate, '%m-%d-%Y') AS saleDate, totalPrice FROM Sales WHERE saleID = (SELECT max(saleID) FROM Sales);`
        db.pool.query(query2, function(error, rows, fields){
          if (error) {
              console.log(error);
              res.sendStatus(400);
          } else {
              res.send(rows);
          }
        });
      }
    });
});

app.post('/add-product-sale', function(req, res) {
  let data = req.body;
  query1 = `INSERT INTO Product_Sales (pid, sid, quantity) 
    VALUES ('${data.pid}', '${data.sid}', '${data.quantity}');`
  db.pool.query(query1, function(error, rows, fields){
    if (error) {
      console.log(error)
      res.sendStatus(400);
    } else {
      query2 = `UPDATE Sales
        SET totalPrice = totalPrice + 
        ((SELECT quantity FROM Product_Sales WHERE pid = ${data.pid} AND sid = ${data.sid})
        *(SELECT salePrice FROM Products WHERE productID = ${data.pid}))  
        WHERE saleID = ${data.sid};`
      db.pool.query(query2, function(error, rows, fields){
        if (error) {
            console.log(error);
            res.sendStatus(400);
        } else {
          query3 = `SELECT PS.pid, PR.salePrice, PS.quantity, S.totalPrice
            FROM Product_Sales PS
            INNER JOIN Products PR ON PS.pid = PR.productID
            INNER JOIN Sales S ON PS.sid = S.saleID 
            WHERE sid = ${data.sid};`
          db.pool.query(query3, function(error, rows, fields){
            if (error) {
              console.log(error);
              res.sendStatus(400);
            } else {
              res.send(rows);
            }
          }); 
        }
      });
    }
  });
});

app.delete('/delete-product-sale', function(req, res) {
  let data = req.body;
  query1 = `UPDATE Sales
    SET totalPrice = totalPrice - ((SELECT salePrice FROM Products WHERE productID = ${data.pid}) 
    *(SELECT quantity FROM Product_Sales WHERE pid = ${data.pid} AND sid = ${data.sid}))
    WHERE saleID = ${data.sid};`
  db.pool.query(query1, function(error, rows, fields){
    if (error) {
      console.log(error)
      res.sendStatus(400);
    } else {
      query2 = `DELETE FROM Product_Sales WHERE pid = ${data.pid} AND sid = ${data.sid}`
      db.pool.query(query2, function(error, rows, fields){
        if (error) {
            console.log(error);
            res.sendStatus(400);
        } else {
            res.send(rows);
        }
      });
    }
  });
});

app.get('/update-product', function(req,res){
  let query1 = `SELECT * FROM Products;`
  let query2 = `SELECT * FROM Vendors;`
  let query3 = `SELECT * FROM Categories;`
  db.pool.query(query1, function(error, rows, fields){
    let products = rows;
    db.pool.query(query2, function(error, rows, fields){
      let vendors = rows;
      db.pool.query(query3, function(error, rows, fields){
        let categories = rows;
        res.render('updateProduct', {products: products, vendors: vendors, categories: categories});
      });
    });
  });     
});


app.get('/update-product-form', function(req, res){
  let data=req.query
  console.log(data)
  let query1
  let params = []
  query1 = "SELECT * FROM Products WHERE "
    for (q in req.query) {
      if (req.query[q] !== '') {
        if (q == "productID") {
          query1 = query1.concat("productID = ? AND ");
          params.push(req.query.productID);
        } else if (q == "vid") {
          query1 = query1.concat("vid = ? AND ");
          params.push(req.query.vid);
        } else if (q == "catid") {
          query1 = query1.concat("catid = ? AND ");
          params.push(req.query.catid);
        }
      }
    }
    query1 = query1.slice(0,-5);
    query1 = query1.concat(";");
  db.pool.query(query1, params, function(error, rows, fields){
    let results = rows;
    res.render('updateProductForm', {data:results});
  });     
});

app.post('/update-product-action', function(req, res){
  let data=req.body
  db.pool.query('SELECT * FROM Products WHERE productID=?', data.productID, function(err, rows, fields){
    if (err){
      console.log(err);
      res.sendStatus(400);
    }
    if (rows.length == 1){
      var curVals = rows[0]
      query1 = `UPDATE Products
                SET vid=?, catid=?, name=?, companyCost=?, salePrice=?, expirationDate=?, stockQuant=? WHERE productID=?;`
      db.pool.query(query1, [data.vid || curVals.vid, data.catid || curVals.catid, data.name || curVals.name, data.companyCost || curVals.companyCost, data.salePrice || curVals.salePrice, data.expirationDate || curVals.expirationDatep, data.stockQuant || curVals.stockQuant,  data.productID], function(error, rows, fields){
        if (error) {
          console.log(error)
          res.sendStatus(400)
        } else {
          res.send(rows)
        }
      });
    }
  })
});


app.get('/profit-analysis', function(req,res){
  let query1 
  let params = []
  let query2 = `SELECT * FROM Categories`
  if (Object.keys(req.query).length === 0){
    query1 = "SELECT P.productID AS pid, P.name, C.name AS catName, V.vendorID AS vid, V.name AS vendName, SUM(PS.quantity * P.salePrice) AS totalSales FROM Products P INNER JOIN Product_Sales PS ON P.productID = PS.pid INNER JOIN Categories C ON P.catid = C.categoryID INNER JOIN Vendors V ON P.vid = V.vendorID GROUP BY P.productID;"
  } else {
    query1 = "SELECT P.productID AS pid, P.name, C.name AS catName, V.vendorID AS vid, V.name as vendName, SUM(PS.quantity * P.salePrice) AS totalSales FROM Products P INNER JOIN Product_Sales PS ON P.productID = PS.pid INNER JOIN Sales S ON PS.sid = S.saleID INNER JOIN Categories C ON P.catid = C.categoryID INNER JOIN Vendors V ON P.vid = V.vendorID WHERE "
    for (q in req.query) {
      if (req.query[q] !== '') {
        if (q == "pid") {
          query1 = query1.concat("P.productID = ? AND ");
          params.push(req.query.pid);
        } else if (q == "vid") {
          query1 = query1.concat("V.vendorID = ? AND ");
          params.push(req.query.vid);
        } else if (q == "catName") {
          query1 = query1.concat("C.name = ? AND ");
          params.push(req.query.catName);
        } else if (q == "earlyDate") {
          query1 = query1.concat("S.saleDate > '?' AND ");
          eDate = String(req.query.earlyDate)
          params.push(eDate);
        } else if (q == "lateDate") {
          query1 = query1.concat("S.saleDate < '?' AND ");
          let lDate = String(req.query.lateDate)
          params.push(lDate);
        }
      }
    }
    query1 = query1.slice(0,-5)
    query1 = query1.concat(" GROUP BY P.productID;")
  }
  db.pool.query(query1, params, function(error, rows, fields){
    let results = rows;
    db.pool.query(query2, function(error, rows, fields){
      let categories = rows;
      res.render('profitAnalysis', {data: results, categories: categories});
    });  
  });     
});

app.get('/sale-history', function(req,res){       //display all past sales
  let query1 
  let params = []
  let query2 = `SELECT customerID, CONCAT(fname, " ", lname) AS name FROM Customers;`
  if (Object.keys(req.query).length === 0){
    query1 = `SELECT S.cid, CONCAT(fname, " ", lname) AS custName, S.saleID, DATE_FORMAT(S.saleDate, '%m-%d-%Y') AS saleDate, S.totalPrice, paymentMethod 
    FROM Sales S 
    INNER JOIN Customers C ON S.cid = C.customerID;`
  } else {
    query1 = "SELECT cid, CONCAT(C.fname, ' ', C.lname) AS custName, saleID, DATE_FORMAT(S.saleDate, '%m-%d-%Y') AS saleDate, totalPrice, paymentMethod FROM Sales S INNER JOIN Customers C ON S.cid = C.customerID WHERE "
    for (q in req.query) {
      if (req.query[q] !== '') {
        if (q == "cid") {
          query1 = query1.concat("S.cid = ? AND ");
          params.push(req.query.cid);
        } else if (q == "saleID") {
          query1 = query1.concat("S.saleID = ? AND ");
          params.push(req.query.saleID);
        } else if (q == "minTotal") {
          query1 = query1.concat("S.totalPrice > ? AND ");
          params.push(req.query.minTotal);
        } else if (q == "maxTotal") {
          query1 = query1.concat("S.totalPrice < ? AND ");
          params.push(req.query.maxTotal);
        } else if (q == "earlyDate") {
          query1 = query1.concat("S.saleDate > '?' AND ");
          eDate = String(req.query.earlyDate)
          params.push(eDate);
        } else if (q == "lateDate") {
          query1 = query1.concat("S.saleDate < '?' AND ");
          let lDate = String(req.query.lateDate)
          params.push(lDate);
        } else if (q == "paymentMethod") {
          query1 = query1.concat("paymentMethod = ? AND ");
          params.push(req.query.paymentMethod);
        }
      }
    }
    query1 = query1.slice(0,-5)
    query1 = query1.concat("GROUP BY saleID;")
  }
  db.pool.query(query1, params, function(error, rows, fields){
      let results = rows;
    db.pool.query(query2, function(error, rows, fields){
      let customers = rows;
      res.render('saleHistory', {data: results, customers: customers});
    });
  });     
});

app.get('/purchase-history', function(req,res){    //display all past purchases
  let query1
  let params = []
  let query2 = `SELECT * FROM Categories;`
  let query3 = `SELECT * FROM Vendors;`
  if (Object.keys(req.query).length === 0){
    query1 = `SELECT P.vid AS vid, V.name AS vendName, purchaseID, DATE_FORMAT(purchaseDate, '%m-%d-%Y') AS purchaseDate, totalPaid 
          FROM Purchases P 
          INNER JOIN Vendors V ON P.vid = V.vendorID;`
  } else {
    query1 = "SELECT P.vid AS vid, V.name AS vendName, P.purchaseID, DATE_FORMAT(purchaseDate, '%m-%d-%Y') AS purchaseDate, totalPaid FROM Purchases P INNER JOIN Vendors V ON P.vid = V.vendorID INNER JOIN Product_Purchases PP ON P.purchaseID = PP.purid INNER JOIN Products PR ON PP.pid = PR.productID INNER JOIN Categories C ON PR.catid = C.categoryID WHERE "
    for (q in req.query) {
      if (req.query[q] !== '') {
        if (q == "vid") {
          query1 = query1.concat("P.vid = ? AND ");
          params.push(req.query.vid);
        } else if (q == "catName") {
          query1 = query1.concat("C.name = ? AND ");
          params.push(req.query.catName);
        } else if (q == "minTotal") {
          query1 = query1.concat("totalPaid > ? AND ");
          params.push(req.query.minTotal);
        } else if (q == "maxTotal") {
          query1 = query1.concat("totalPaid < ? AND ");
          params.push(req.query.maxTotal);
        } else if (q == "earlyDate") {
          query1 = query1.concat("purchaseDate > ? AND ");
          eDate = String(req.query.earlyDate)
          params.push(eDate);
        } else if (q == "lateDate") {
          query1 = query1.concat("purchaseDate < ? AND ");
          let lDate = String(req.query.lateDate)
          params.push(lDate);
        }
      }
    }
    query1 = query1.slice(0,-5)
    query1 = query1.concat("GROUP BY P.purchaseID;")
  }
  db.pool.query(query1, params, function(error, rows, fields){
    let results = rows;
    db.pool.query(query2, function(error, rows, fields){
      let categories = rows;
      db.pool.query(query3, function(error, rows, fields){
        let vendors = rows;
        console.log(vendors)
        res.render('purchaseHistory', {data: results, categories: categories, vendors: vendors});
      });
    });
  });     
});


app.use(function(req,res){
  res.status(404);
  res.render('404');
});

app.use(function(err, req, res, next){
  console.error(err.stack);
  res.type('plain/text');
  res.status(500);
  res.render('500');
});

app.listen(app.get('port'), function(){
  console.log('Express started on http://localhost:' + app.get('port') + '; press Ctrl-C to terminate.');
});