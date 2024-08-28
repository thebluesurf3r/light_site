document.addEventListener('DOMContentLoaded', function () {
    // Initialize the date range slider
    const dateRangeSlider = document.getElementById('dateRangeSlider');
    const dateRangeStart = document.getElementById('dateRangeStart');
    const dateRangeEnd = document.getElementById('dateRangeEnd');
    
    const minDate = new Date('{{ min_date }}');
    const maxDate = new Date('{{ max_date }}');
    
    const minDateTime = minDate.getTime();
    const maxDateTime = maxDate.getTime();
    const totalDays = (maxDateTime - minDateTime) / (1000 * 60 * 60 * 24);
    
    noUiSlider.create(dateRangeSlider, {
        start: [0, totalDays],
        connect: true,
        range: {
            'min': 0,
            'max': totalDays
        },
        step: 1,
        tooltips: [false, false],
        format: {
            to: function(value) {
                return Math.round(value);
            },
            from: function(value) {
                return Number(value);
            }
        }
    });
    
    dateRangeSlider.noUiSlider.on('update', function (values) {
        const startDate = new Date(minDateTime + values[0] * 24 * 60 * 60 * 1000);
        const endDate = new Date(minDateTime + values[1] * 24 * 60 * 60 * 1000);
        
        dateRangeStart.textContent = startDate.toISOString().split('T')[0];
        dateRangeEnd.textContent = endDate.toISOString().split('T')[0];
    });

    // Initialize the amount threshold slider
    const amountThresholdSlider = document.getElementById('amountThresholdSlider');
    const amountThresholdValue = document.getElementById('amountThresholdValue');

    const minAmount = {{ min_amount }};
    const maxAmount = {{ max_amount }};
    const midAmount = (maxAmount - minAmount) / 2;
    const stepSizeAmount = (maxAmount - minAmount) / 300;

    noUiSlider.create(amountThresholdSlider, {
        start: midAmount,
        connect: [true, false],
        range: {
            'min': minAmount,
            'max': maxAmount
        },
        step: stepSizeAmount,
        tooltips: false,
        format: {
            to: function(value) {
                return Math.round(value);
            },
            from: function(value) {
                return Number(value);
            }
        }
    });

    amountThresholdSlider.noUiSlider.on('update', function (values) {
        amountThresholdValue.textContent = values[0];
    });

    // Initialize the balance threshold slider
    const balanceThresholdSlider = document.getElementById('balanceThresholdSlider');
    const balanceThresholdValue = document.getElementById('balanceThresholdValue');

    const minBalance = {{ min_balance }};
    const maxBalance = {{ max_balance }};
    const midBalance = (maxBalance - minBalance) / 2;
    const stepSizeBalance = (maxBalance - minBalance) / 300;

    noUiSlider.create(balanceThresholdSlider, {
        start: midBalance,
        connect: [true, false],
        range: {
            'min': minBalance,
            'max': maxBalance
        },
        step: stepSizeBalance,
        tooltips: false,
        format: {
            to: function(value) {
                return Math.round(value);
            },
            from: function(value) {
                return Number(value);
            }
        }
    });

    balanceThresholdSlider.noUiSlider.on('update', function (values) {
        balanceThresholdValue.textContent = values[0];
    });

    // Handle transaction type button clicks
    let transactionType = 'Both'; // Default value
    function setTransactionType(type) {
        transactionType = type;
        updateButtonStyles(type);
    }

    function updateButtonStyles(selected) {
        document.getElementById('debitButton').classList.toggle('btn-primary', selected === '-1');
        document.getElementById('debitButton').classList.toggle('btn-secondary', selected !== '-1');
        document.getElementById('creditButton').classList.toggle('btn-primary', selected === '1');
        document.getElementById('creditButton').classList.toggle('btn-secondary', selected !== '1');
        document.getElementById('bothButton').classList.toggle('btn-info', selected === 'Both');
        document.getElementById('bothButton').classList.toggle('btn-secondary', selected !== 'Both');
    }

    document.getElementById('debitButton').addEventListener('click', function () {
        setTransactionType('-1'); // Debit
    });
    document.getElementById('creditButton').addEventListener('click', function () {
        setTransactionType('1'); // Credit
    });
    document.getElementById('bothButton').addEventListener('click', function () {
        setTransactionType('Both'); // Both
    });

    // Debounced search box input handling
    let debounceTimeout;
    const searchBox = document.getElementById('searchBox');

    searchBox.addEventListener('input', function () {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(updateFilters, 300); // 300ms debounce
    });

    // Submit filters
    function updateFilters() {
        const amountThreshold = document.getElementById('amountThresholdSlider').noUiSlider.get();
        const balanceThreshold = document.getElementById('balanceThresholdSlider').noUiSlider.get();
        const searchTerm = searchBox.value;

        const startDate = dateRangeStart.textContent;
        const endDate = dateRangeEnd.textContent;

        fetch(`/fetch_data/?start_date=${startDate}&end_date=${endDate}&transaction_type=${transactionType}&amount_threshold=${amountThreshold}&balance_threshold=${balanceThreshold}&search_term=${searchTerm}`)
            .then(response => response.json())
            .then(data => {
                // Handle data update here
                console.log(data);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }
});