//live line graph
window.onload = function () {

    var dps = []; // dataPoints
    var chart = new CanvasJS.Chart("chartContainer1", {
        title :{
            text: ""
        },
        data: [{
            type: "line",
            dataPoints: dps
        }]
    });
    
    var xVal = 0;
    var yVal = 100; 
    var updateInterval = 1000;
    var dataLength = 20; // number of dataPoints visible at any point
    
    var updateChart = function (count) {
    
        count = count || 1;
    
        for (var j = 0; j < count; j++) {
            yVal = yVal +  Math.round(5 + Math.random() *(-5-5));
            dps.push({
                x: xVal,
                y: yVal
            });
            xVal++;
        }
    
        if (dps.length > dataLength) {
            dps.shift();
        }
    
        chart.render();
    };
    
    updateChart(dataLength);
    setInterval(function(){updateChart()}, updateInterval);
    
    }

// pie graph
window.onload = function() {

    var chart = new CanvasJS.Chart("chartContainer2", {
        theme: "light2", // "light1", "light2", "dark1", "dark2"
        exportEnabled: true,
        animationEnabled: true,
        title: {
            text: ""
        },
        data: [{
            type: "pie",
            startAngle: 25,
            toolTipContent: "<b>{label}</b>: {y}%",
            showInLegend: "true",
            legendText: "{label}",
            indexLabelFontSize: 16,
            indexLabel: "{label} - {y}%",
            dataPoints: [
                { y: 51.08, label: "Chrome" },
                { y: 27.34, label: "Internet Explorer" },
                { y: 10.62, label: "Firefox" },
            ]
        }]
    });
    chart.render();
    
    }

   // Async function for getting transactions data
   async function getTransactions(){
//   let url = 'https://c4rm9elh30.execute-api.us-east-1.amazonaws.com/default/cachedPriceData?ticker=TSLA'
    let url = '/api/transactions'
//    let response = await fetch(url).then(res => {
//        if(!res.ok){
//        console.error("Backend responded with ${res.status} error");
//        return null;
//        }
//        return res.json();
//    }, error=> {
//        console.error("Could not reach backend", error);
//        return null;
//    });
    let response = await fetch(url);
    let result = await response.json();
    if (response.ok){
        console.log("Successfully got Data");
        console.log(result);
        displayPortfolio(result);
//        return result;
    }else{
        alert("Error getting transactions: " + result.message);
        return null;
    }
   }

   getTransactions();

//    asynchronous function to add a transaction
async function addTransaction(event) {
   //prevent the form from submitting the default way
   event.preventDefault();

   const transactiontype = document.getElementByID('transaction-type').value;
   const ticker = document.getElementById('ticker').value;
   const quantity = document.getElementById('quantity').value;

   //prepare the request payload
   const transactionData = {
       transactiontype: transactiontype,
       ticker: ticker,
       quantity: parseInt(quantity)
   };

   try {
       // send a POST request to the server to add the transaction
       const response = await fetch('/api/add-transaction', {
           method: 'POST',
           headers: {
               'Content-Type':'application/json'
           },
           body: JSON.stringify(transactionData)
       });

       // Parse the JSON response from the server
       const result = await response.json();
       // check if transaction was successful
       if (response.ok) {
           alert(result.message);
           //getTransactions(); this will just reload the transactions page if the transaction was successful
       } else {
           alert('Error adding transacion: ' + result.message);
       }
   } catch (error) {
       console.error('Error:', error);
       alert('Error adding transaction'); //just display a generic error message after logging the errors to the console
   }
}

//handle form submission
document.getElementByID('transaction-Form').addEventListener('submit', addTransaction); //will need to give the html form a form id

// display portfolio
function displayPortfolio(data) {
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');

        // Create and append cells to the row
        const symbol = document.createElement('td');
        symbol.textContent = item[2];
        row.appendChild(symbol);

        const qty = document.createElement('td');
        qty.textContent = item[4];
        row.appendChild(qty);

        const purchasePrice = document.createElement('td');
        purchasePrice.textContent = item[3];
        row.appendChild(purchasePrice);

        const currentPrice = document.createElement('td');
        currentPrice.textContent = item[3];
        row.appendChild(currentPrice);

        const date = document.createElement('td');
        date.textContent = item[5];
        row.appendChild(date);

        tbody.appendChild(row);
    });
}

window.onload = getTransactions;
