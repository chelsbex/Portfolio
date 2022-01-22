
app.post('/update-product-get-id', function(req, res){
       let data=req.body
        context = {}
        db.pool.query('SELECT productID, vid, catid, name, companyCost, salePrice, expirationDate, stockQuant  FROM Products WHERE productID=?;', data.productID, function(err, rows, fields){
          if (err){
            console.log(err);
            res.sendStatus(400);
          } else {
                results = JSON.parse(JSON.stringify(rows))

                results[0].expirationDate = new Date(results[0].expirationDate).toISOString().slice(0, 10);

                query1 = `SELECT vendorID, name FROM Vendors`
                query2 = `SELECT categoryID, name FROM Categories`
                db.pool.query(query1, query2, function(error, rows, fields){
                        if (error) {
                                console.log(error)
                                res.sendStatus(400)
                        } else {


                                results3=JSON.parse(JSON.stringify(rows))

                                res.render('updateProductForm', {results: results});


                        }

                })
                }
        });
});

