// Global
const api = 'http://127.0.0.1:5000'; // Change This
// const api = 'https://tokopaedi-api.dapuntaratya.com'; // Change This
let buffer = '';
let list_product = [];

// Add Event Listener Input
const inputForm = document.getElementById('product_link');
inputForm.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        const url_product = inputForm.value;
        fetchURL(url_product);
    }
});

// Add Event Listener Submit Button
const submitButton = document.getElementById('submit_button');
submitButton.addEventListener('click', (event) => {
    const url_product = inputForm.value;
    fetchURL(url_product);
});

// Loading Spinner
function loading(element_id, active) {
    const loadingBox = document.getElementById(element_id);
    if (active)  {
        loadingBox.innerHTML = `<div id="loading-spinner" class="spinner-container"><div class="spinner"></div></div>`;
        loadingBox.style.pointerEvents = 'none';
    }
    else {
        loadingBox.innerHTML = `<i class="fa-solid fa-arrow-right"></i>`;
        loadingBox.style.pointerEvents = 'auto';
    }
}

// Fetch URL
async function fetchURL(raw_url) {
    const url_product = raw_url.replace(/\s/g, '') === '' ? null : encodeURIComponent(raw_url);
    if (url_product) {
        list_product = [];
        document.getElementById('title-related').className = 'title-container-output-inactive';
        document.getElementById('title-result').className = 'title-container-result-inactive';
        document.getElementById('container-output').innerHTML = '';
        document.getElementById('container-result').innerHTML = '';
        loading('submit_button', true);
        const fetch_url = `${api}/fetch?url=${url_product}`;
        const eventSource = new EventSource(fetch_url);
        eventSource.onmessage = function(event) {
            buffer += event.data;
            processBuffer();
        };
        eventSource.addEventListener('end', function(event) {
            eventSource.close();
            loading('submit_button', false);
            inputForm.value = '';
            if (list_product.length !== 0) rankProduct();
        });
        eventSource.onerror = function(err) {
            eventSource.close();
            loading('submit_button', false);
            inputForm.value = '';
        };
    }
    else {
        loading('submit_button', false);
        inputForm.value = '';
    }
}

// Buffer Read Response
function processBuffer() {
    let braceCount = 0;
    let startIndex = -1;
    for (let i = 0; i < buffer.length; i++) {
        if (buffer[i] === '{') {
            if (braceCount === 0) startIndex = i;
            braceCount++;
        }
        else if (buffer[i] === '}') {
            braceCount--;
            if (braceCount === 0 && startIndex !== -1) {
                const jsonStr = buffer.substring(startIndex, i + 1);
                try {
                    const product = JSON.parse(jsonStr);
                    displayProduct(product);
                    buffer = buffer.substring(i + 1);
                    i = -1;
                }
                catch (e) {
                    console.error('Failed to parse JSON:', e);
                }
                startIndex = -1;
            }
        }
    }
}

// Display Product
function displayProduct(product) {
    list_product.push(product);
    if (list_product.length !== 0) document.getElementById('title-related').className = 'title-container-output-active';
    const productDiv = document.createElement('div');
    productDiv.className = 'item-output';
    productDiv.innerHTML = `
        <div class="image-container"><img src="${product.picture}" alt="${product.name}"></div>
        <div class="container-output-description">
            <a class="output-price">Rp ${product.price.toLocaleString().replace(/,/g, '.')}</a>
            <a class="output-ongkir"><i class="fa-solid fa-truck"></i>Rp ${product.ongkir.toLocaleString().replace(/,/g, '.')}</a>
            <a class="output-waktu"><i class="fa-regular fa-clock"></i>${product.waktu} Hari</a>
            <a class="output-sold"><i class="fa-solid fa-box-open"></i>${product.sold}</a>
            <a class="output-review"><i class="fa-regular fa-comments"></i>${product.review}</a>
            <a class="output-rating"><i class="fa-regular fa-star"></i>${product.rating}</a>
        </div>`;
    productDiv.addEventListener('click', function() {
        openSequentially(product.url);
    });
    document.getElementById('container-output').appendChild(productDiv);
    productDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'end' });
}

// Buka URL Pada Tab Baru
function openSequentially(url) {
    const link1 = document.createElement('a');
    link1.href = url;
    link1.target = '_blank';
    link1.rel = 'noopener noreferrer';
    link1.click();
}

// Ranking
async function rankProduct() {
    const heuristic_url = `${api}/heuristic`;
    const headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
    };
    const data = {
        'method'  : 'POST',
        'mode'    : 'cors',
        'headers' : headers,
        'body'    : JSON.stringify({'data':list_product})
    };
    const req = await fetch(heuristic_url, data);
    const response = await req.json();
    if (response.data.length !== 0) {
        document.getElementById('title-result').className = 'title-container-result-active';
        response.data.forEach((item, index)=>{
            displayResult(item, index+1);
        });
    }
}

// Display Result
function displayResult(product, index) {
    const productDiv = document.createElement('div');
    productDiv.className = 'item-result';
    productDiv.innerHTML = `
        <div class="item-result">
            <div class="image-container">
                <span>${index}</span>
                <img src="${product.picture}" alt="${product.name}">
            </div>
            <div class="result-description-container">
                <a class="result-title">${product.name}</a>
                <a class="result-totalprice">Rp ${product.price.toLocaleString().replace(/,/g, '.')} + ${product.ongkir.toLocaleString().replace(/,/g, '.')}</a>
                <div class="result-info-container">
                    <a>Terjual ${product.sold}</a>
                    <a>Rating ${product.rating}</a>
                    <a>Stok Tersisa ${product.stock}</a>
                    <a>Pengiriman ${product.waktu} Hari</a>
                </div>
            </div>
        </div>`;
    productDiv.addEventListener('click', function() {
        openSequentially(product.url);
    });
    document.getElementById('container-result').appendChild(productDiv);
}