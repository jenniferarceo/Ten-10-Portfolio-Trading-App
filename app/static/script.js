//live line graph
window.addEventListener('load', function() {
    getHoldings();
    LiveLineGraph();
    PieChart();
    getTransactions();
});

function LiveLineGraph() {

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
function PieChart(data) {
    let portfolio = [];
    for (const item in data) {
        let value = item["volume"] * parseInt(item["curr_price"]);
        let ticker = item["ticker"];
        portfolio.push([value, ticker]);
    }

    for (const item in portfolio) {
        console.log(item)
    }

    var chart = new CanvasJS.Chart("chartContainer2", {
        theme: "light2", // "light1", "light2", "dark1", "dark2"
        exportEnabled: false,
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
            indexLabelFontSize: 12,
            indexLabel: "{label} - {y}%",
            dataPoints: [
                { y: portfolio[0][0], label: portfolio[0][1] },
                { y: portfolio[1][0], label: portfolio[1][1] },
                { y: portfolio[2][0], label: portfolio[2][1] },
                
            ]
        }]
    });
    chart.render();
}
    
   // Async function for getting transactions data
   async function getHoldings(){
//   let url = 'https://c4rm9elh30.execute-api.us-east-1.amazonaws.com/default/cachedPriceData?ticker=TSLA'
    let url = '/api/holdings'
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
        PieChart(result);
    }else{
        alert("Error getting holdings: " + result.message);
        return null;
    }
   }

// display portfolio
function displayPortfolio(data) {
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = '';

    data.forEach(item => {
        const row = document.createElement('tr');

        // Create and append cells to the row
        const symbol = document.createElement('td');
        symbol.textContent = item["ticker"];
        row.appendChild(symbol);

        const qty = document.createElement('td');
        qty.textContent = item["volume"];
        row.appendChild(qty);

        const currPrice = document.createElement('td');
        currPrice.textContent = item["curr_price"];
        row.appendChild(currPrice);

        tbody.appendChild(row);
    });
}

// asynchronous function to add a transaction
async function addTransaction(event) {
    //prevent the form from submitting the default way
    event.preventDefault();

    const transactiontype = document.getElementById('transactionType').value;
    const ticker = document.getElementById('ticker').value;
    const quantity = document.getElementById('quantity').value;

    //check  if is ticker is alphabetic and quantity is a positive integer
     if (!ticker.match(/^[a-zA-Z]+$/)) {
        alert("Ticker must only contain alphabetic characters. ");
        return;
     }
     if (!(Number.isInteger(Number(quantity)) && Number(quantity) > 0)) {
        alert("Quantity must be a positive whole number.");
        return
     }

    //prepare the request payload
    const transactionData = {
        transactiontype: transactiontype,
        ticker: ticker,
        quantity: parseInt(quantity),
    };
    console.log(transactionData);
    try {
        // send a POST request to the server to add the transaction
        const response = await fetch('/api/addTransaction', {
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify(transactionData)
        });
        console.log("Sent post request to server");
        // Parse the JSON response from the server
        const result = await response.json();
        console.log("result: " , result);
        // check if transaction was successful
        if (response.ok) {
            alert(result.message);
            updateTable();
        } else {
            alert('Error adding transaction: ' + result.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error adding transaction'+ error.message); //just display a generic error message after logging the errors to the console
    }
 }

 // get all transactions
 async function getTransactions() {
    try {
        //request to fetch transactions
        const response = await fetch('/api/transactions', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }


        const text = await response.text();
        console.log("Raw response text:", text);

        try {
            const transactions = JSON.parse(text); //manually parse the text to JSON
            console.log("Fetched transactions: ", transactions);
            displayTransactions(transactions);
        } catch (e) {
            console.error('Failed to parse JSON:', e);
            alert('Server returned invalid JSON');
        }
    } catch (error) {
        console.error('Error fetching transactions:', error);
        alert('Error fetching transactions');
    }
 }
//display transactions
function displayTransactions(transactions) {
    const transactionsTableBody = document.getElementById('transactions-table-body');
    transactionsTableBody.innerHTML = ''; //clear existing table data

    const descendingTransactions = transactions.slice().reverse();

    descendingTransactions.forEach(transaction => {
        const row = document.createElement('tr');
        row.innerHTML = `
        <td>${transaction[2]}</td>
        <td>${transaction[1]}</td>
        <td>${transaction[3]}</td>
        <td>${transaction[4]}</td>
        <td>${transaction[5]}</td>
        `;
        transactionsTableBody.appendChild(row);
    });
}

// update transactions and holdings table
async function updateTable() {
    await getTransactions();
    await getHoldings();
}

 // handle form submission
 const form = document.getElementById('orderButton');
 form.addEventListener('click', addTransaction);

 // get stock price
 async function getStockPrice() {
    const ticker = document.getElementById('ticker').value;
    
    try {
        // request to fetch stock price
        const response = await fetch('/api/checkPrice/' + ticker, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const text = await response.text();
        console.log("Raw response text:", text);

        try {
            const stockPrice = JSON.parse(text); // manually parse the text to JSON
            console.log("Fetched stock price: ", stockPrice);
            displayStockPrice(stockPrice);
        } catch (e) {
            console.error('Failed to parse JSON:', e);
            alert('Server returned invalid JSON');
        }
    } catch (error) {
        console.error('Error fetching stock price:', error);
        alert('Error fetching stock price');
    }
 }

 function displayStockPrice(stock) {
    const currPrice = document.getElementById('currPrice');
    currPrice.textContent = "$" + `${stock}`;
 }

 const price = document.getElementById('checkPrice');
 price.addEventListener('click', getStockPrice);

 // clear current price value when the form is cleared
 const clearPrice = document.getElementById('clearButton')
 clearPrice.addEventListener('click', () => {
    const currPrice = document.getElementById('currPrice');
    currPrice.textContent = "---";
 })