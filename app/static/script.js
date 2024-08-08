window.addEventListener('load', function() {
    LiveLineGraph();
    updateTable();
});

let isFetchingHoldings = false;
setInterval(async function(){
    if (!isFetchingHoldings) {
        try {
            isFetchingHoldings = true;
            await getHoldings();
        } catch (error) {
            console.error('Error fetching holdings:', error);
        } finally {
            if (isFetchingHoldings) {
                isFetchingHoldings = false; // reset flag to show fetching is complete
            }
        }
    }     
}, 5000);

var holdings;

// live line graph
function LiveLineGraph() {

    var dps = []; // dataPoints
    var chart = new CanvasJS.Chart("chartContainer1", {
        title :{
            text: ""
        },
        backgroundColor: "#F4F4F4",
        data: [{
            type: "line",
            color: "#7A37E8",
            dataPoints: dps
        }]
    });
    
    var xVal = new Date();
    var updateInterval = 5000;
    var dataLength = 20; // number of dataPoints visible at any point
    
    var updateChart = function (count) {
    
        count = count || 1;
    
        for (var j = 0; j < count; j++) {
            dps.push({
                x: new Date(xVal.getTime()),
                y: pnl[pnl.length-1]
            });
            xVal.setSeconds(xVal.getSeconds() + 5);  
        }
    
        if (dps.length > dataLength) {
            dps.shift();
        }
    
        chart.render();
    };
    
    updateChart(1);
    setInterval(function(){updateChart(1)}, updateInterval); 
}

// pie graph
function PieChart(data) {
    let dataPoints = [];
    let totalValue = 0;

    // calculate total portfolio value
    for (const item in data) {
        currItem = data[item];
        let value = currItem["volume"] * parseInt(currItem["curr_price"]);
        totalValue += value;
    }

    // add stock percentage as data points
    for (const item in data) {
        currItem = data[item];
        let value = currItem["volume"] * parseInt(currItem["curr_price"]) / totalValue;
        let ticker = currItem["ticker"];

        if (value != 0) {
            dataPoints.push({
                y: (value * 100).toFixed(2),
                label: ticker
            });
        }
    }

    var chart = new CanvasJS.Chart("chartContainer2", {
        theme: "light2", // "light1", "light2", "dark1", "dark2"
        exportEnabled: false,
        //animationEnabled: true,
        backgroundColor: "#F4F4F4",
        data: [{
            type: "pie",
            startAngle: 25,
            toolTipContent: "<b>{label}</b>: {y}%",
            showInLegend: true,
            legendText: "{label}",
            indexLabelFontSize: 12,
            indexLabel: "{label} {y}%",
            dataPoints: dataPoints
        }]
    });
    chart.render();
}

// store unrealized pnl values
let pnl = [];
function updatePNL(dataPoint) {
    if (pnl.length == 21) {
        pnl.pop();
        pnl.push(dataPoint);
    }
    else {
        pnl.push(dataPoint);
    }
    pnl.forEach(item => console.log("Item: "+item));
}

// display portfolio performance
function displayPerformance(data) {
    // calculate total unrealized value
    let unrealizedVal = 0;
    for (const item in data) {
        currItem = data[item];
        unrealizedVal += parseInt(currItem["unrealized_pnl"]);
    }
    document.getElementById("todaysChange").textContent = unrealizedVal;
    updatePNL(unrealizedVal);


    // calculate total portfolio value
    let accountValue = 0;
    for (const item in data) {
        currItem = data[item];
        let value = currItem["volume"] * parseInt(currItem["curr_price"]);
        accountValue += value;
    }
    document.getElementById("accountValue").textContent = accountValue;
}
    
// Async function for getting transactions data
async function getHoldings(){
    let url = '/api/holdings'
    let response = await fetch(url);
    let result = await response.json();
    if (response.ok){
        console.log("Successfully got Data");
        console.log(result);
        holdings = result;
        displayPortfolio(result);
        PieChart(holdings);
        displayPerformance(holdings);
    }else{
        alert("Error getting holdings: " + result.message);
        return null;
    }
}

// display portfolio holdings
function displayPortfolio(data) {
    const tbody = document.getElementById('holdings-table-body');
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

        if (item["volume"] != 0) {
            tbody.appendChild(row);
        }
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
    if (!isFetchingHoldings) {
        try {
            isFetchingHoldings = true; // set flag to indicate fetching is in progress
            await getTransactions();
            await getHoldings();
        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            if (isFetchingHoldings) {
                isFetchingHoldings = false; // reset flag to show fetching is complete
            }
        }
    }
}

 // handle form submission
 const form = document.getElementById('orderButton');
 form.addEventListener('click', addTransaction);

 // get stock price
 async function getStockPrice(event) {
    event.preventDefault();
    const ticker = document.getElementById('ticker').value;
    const quantityInput = document.getElementById('quantity');
    quantityInput.value = '';
    
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

// display current stock price
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