-- add a new Customer
INSERT INTO Customers (fname, lname, email, phoneNumber, streetAddress, city, state, countryCode, acceptingEmails) VALUES (:fnameInput, :lnameInput, :emailInput, :phoneNumberInput, :streetAddressInput,
:cityInput, :stateInput, :countryCodeInput, :acceptingEmails_from_dropdown);


-- add a Vendor
INSERT INTO Vendors (name, email, description) 
VALUES (:vendorNameInput, :emailInput, :descriptionInput_from_textbox);


-- add a new Product
INSERT INTO Products (vid, catid, name, companyCost, salePrice, expirationDate, stockQuant) 
VALUES ((SELECT vendorId FROM Vendors WHERE name = :vendorNameInput), (SELECT categoryID FROM Categories 
WHERE name = :categoryNameInput), :productNameInput, :companyCostInput, :salePriceInput, :expirationPriceInput, :stockQuantInput);

-- display Product information to be updated
SELECT * FROM Products
WHERE productID = :productIDInput, vid = :vendorIDInput, catid = categoryIDInput;

-- update Product information
UPDATE Products 
SET vid = :vendorIDInput, name = :nameInput, companyCost = :companyCostInput, salePrice = :salePriceInput, expirationDate = :expirationDateInput, stockQuant = :stockQuantInput
WHERE productID = :productId_from_hidden_input;


-- add a new Category
INSERT INTO Categories (name) 
VALUES (:categoryNameInput);


-- add a new Purchase (value for totalPaid will be auto entered as 0 initially and filled out as items are added to the Purchase)
INSERT INTO Purchases (vid, purchaseDate) 
VALUES (:vendorIDInput, :purchaseDateInput);

-- display the general Purchase information
SELECT purchaseID, vid, DATE_FORMAT(purchaseDate, '%m-%d-%Y') AS purchaseDate, totalPaid 
FROM Purchases 
WHERE purchaseID = (SELECT max(purchaseID) FROM Purchases);

-- associate a Product with a Purchase (M:M relationship addition)
INSERT INTO Product_Purchases (pid, purid, quantity) 
VALUES (:pidInput, :inputFromPurchaseIDTableCol, :quantityInput);

UPDATE Purchases
SET totalPaid = totalPaid + (SELECT salePrice from Products WHERE productID = :inputFromProductIDTableCol)*(SELECT quantity FROM Product_Purchases WHERE pid = :inputFromProductIDTableCol AND purid = :inputFromPurchaseIDTableCol))
WHERE purchaseID = :inputFromPurchaseIDTableCol FROM Purchases);

-- display the Product-Purchase line item added to the purchase
SELECT PP.pid, PR.companyCost, PP.quantity, P.totalPaid
FROM Product_Purchases PP
INNER JOIN Products PR ON PP.pid = PR.productID
INNER JOIN Purchases P ON PP.purid = P.purchaseID 
WHERE purid = :inputFromPurchaseIDTableCol;

-- delete a Product from a Purchase (M:M relationship)
UPDATE Purchases
SET totalPaid = totalPaid - ((SELECT companyCost FROM Products WHERE productID = :inputFromProductIDTableCol) *(SELECT quantity FROM Product_Purchases WHERE pid = :inputFromProductIDTableCol AND purid = :inputFromPurchaseIDTableCol))
WHERE purchaseID = :inputFromPurchaseIDTableCol FROM Purchases);  

DELETE FROM Product_Purchases 
WHERE pid = :inputFromProductIDTableCol AND purid = :inputFromPurchaseIDTableCol FROM Purchases); 


-- add a new Sale (Sale row needs to be created and have an id before anything can get added to Product_Sales, so totalPrice will be initialized to 0)
INSERT INTO Sales (cid, saleDate, paymentMethod) 
VALUES (:customerIdInput, :saleDateInput, :paymentMethodInput);

-- display the general Sale information
SELECT saleID, cid, DATE_FORMAT(saleDate, '%m-%d-%Y') AS saleDate, totalPrice 
FROM Sales 
WHERE saleID = (SELECT max(saleID) FROM Sales);

-- associate a Product with a Sale (M:M relationship addition)
INSERT INTO Product_Sales (pid, sid, quantity) 
VALUES (:pidInput, :sidInput, :quantityInput);

UPDATE Sales
SET totalPrice = totalPrice + ((SELECT quantity FROM Product_Sales WHERE pid = :inputFromProductIDTableCol AND sid = max(saleID))*(SELECT salePrice from Products WHERE productID = :inputFromProductIDTableCol))  
WHERE saleID = :sidInput FROM Sales);

-- display the Product-Sale line item added to the sale
SELECT PS.pid, PR.salePrice, PS.quantity, S.totalPrice
FROM Product_Sales PS
INNER JOIN Products PR ON PS.pid = PR.productID
INNER JOIN Sales S ON PS.sid = S.saleID 
WHERE sid = :inputSaleIDTableCol;

-- delete a Product from a Sale (M:M relationship)
UPDATE Sales
SET totalPrice = totalPrice - ((SELECT salePrice FROM Products WHERE productID = :inputFromProductIDTableCol)*(SELECT quantity FROM Product_Sales WHERE pid = :inputFromProductIDTableCol) AND sid = :inputFromSaleIDTableCol))
WHERE saleID = :inputFromSaleIDTableCol;  

DELETE FROM Product_Sales 
WHERE pid = :inputFromProductIDTableCol AND sid = :inputFromSaleIDTableCol;
 

--display the table for searching sale history

--by input customerID

SELECT cid, CONCAT(fname, " ", lname) AS custName, saleID, DATE_FORMAT(saleDate, '%m-%d-%Y') AS saleDate, totalPrice, paymentMethod
FROM Sales S
INNER JOIN Customers C ON S.cid = C.customerID
WHERE cid = :customerIDInput;

--by input saleID
SELECT cid, CONCAT(fname, " ", lname) AS custName, saleID, DATE_FORMAT(saleDate, '%m-%d-%Y') AS saleDate, totalPrice, paymentMethod
FROM Sales S
INNER JOIN Customers C ON S.cid = C.customerID
WHERE saleID = :saleIDInput;

--by input transaction amount
SELECT cid, CONCAT(fname, " ", lname), saleID, DATE_FORMAT(saleDate, '%m-%d-%Y') AS saleDate, totalPrice, paymentMethod
FROM Sales S
INNER JOIN Customers C ON S.cid = C.customerID
WHERE totalPrice >= :priceInput1 AND totalPrice <= :priceInput2;

--by inputted date range
SELECT cid, CONCAT(fname, " ", lname), saleID, DATE_FORMAT(saleDate, '%m-%d-%Y') AS saleDate, totalPrice, paymentMethod
FROM Sales S
INNER JOIN Customers C ON S.cid = C.customerID
WHERE saleDate >= :dateInput1 AND saleDate <= :saleInput2;

--by selected payment method
SELECT cid, CONCAT(fname, " ", lname), saleID, DATE_FORMAT(saleDate, '%m-%d-%Y') AS saleDate, totalPrice, paymentMethod
FROM Sales S
INNER JOIN Customers C ON S.cid = C.customerID
WHERE paymentMethod = :paymentMethod_select_from_dropdown;


--display the table for searching purchase history

--by input vendorID
SELECT vid, name, purchaseID, DATE_FORMAT(purchaseDate, '%m-%d-%Y') AS purchaseDate, totalPaid
FROM Purchases P
INNER JOIN Vendors V ON P.vid = V.vendorID
WHERE vendorID = :vendorIDInput;

--by input expense range
SELECT vid, name, purchaseID, DATE_FORMAT(purchaseDate, '%m-%d-%Y') AS purchaseDate, totalPaid
FROM Purchases P
INNER JOIN Vendors V ON P.vid = V.vendorID
WHERE totalPaid >= :totalPaidInput1 AND totalPaid <= :totalPaidInput2;

--by input date range
SELECT vid, name, purchaseID, DATE_FORMAT(purchaseDate, '%m-%d-%Y') AS purchaseDate, totalPaid
FROM Purchases P
INNER JOIN Vendors V ON P.vid = V.vendorID
WHERE purchaseDate >= :purchaseDateInput1 AND purchaseDate <= :purchaseDateInput2;


--perfrom profit analysis

--by productID
SELECT P.productID, P.name, C.name AS catName, V.vendorID, V.name as vendName, SUM(PS.quantity * P.salePrice) AS totalSales 
FROM Products P 
INNER JOIN Product_Sales PS ON P.productID = PS.pid 
INNER JOIN Categories C ON P.catid = C.categoryID 
INNER JOIN Vendors V ON P.vid = V.vendorID
WHERE pid = :productIDInput
GROUP BY pid;

--by vendorID
SELECT P.productID, P.name, C.name AS catName, V.vendorID, V.name as vendName, SUM(PS.quantity * P.salePrice) AS totalSales 
FROM Products P 
INNER JOIN Product_Sales PS ON P.productID = PS.pid 
INNER JOIN Categories C ON P.catid = C.categoryID 
INNER JOIN Vendors V ON P.vid = V.vendorID
WHERE vendorID = :vendorIDInput
GROUP BY pid;

--by category
SELECT P.productID, P.name, C.name AS catName, V.vendorID, V.name as vendName, SUM(PS.quantity * P.salePrice) AS totalSales 
FROM Products P 
INNER JOIN Product_Sales PS ON P.productID = PS.pid 
INNER JOIN Categories C ON P.catid = C.categoryID 
INNER JOIN Vendors V ON P.vid = V.vendorID
WHERE catName = :categoryNameInput
GROUP BY pid;

--by date range
SELECT P.productID, P.name, C.name AS catName, V.vendorID, V.name as vendName, SUM(PS.quantity * P.salePrice) AS totalSales 
FROM Products P 
INNER JOIN Product_Sales PS ON P.productID = PS.pid 
INNER JOIN Categories C ON P.catid = C.categoryID 
INNER JOIN Vendors V ON P.vid = V.vendorID
WHERE S.saleDate >= :saleDateInput1 AND S.saleDate <= :saleDateInput2
GROUP BY pid;
  