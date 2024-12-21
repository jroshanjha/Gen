const display = document.getElementById('display');
const buttons = document.querySelectorAll('button');

let currentValue = '';
let operator = '';
let previousValue = '';

buttons.forEach(button => {
    button.addEventListener('click', () => {
        const value = button.dataset.value;

        if (value === 'AC') {
            currentValue = '';
            operator = '';
            previousValue = '';
            display.value = '';
        } else if (value === 'DEL') {
            currentValue = currentValue.slice(0, -1);
            display.value = currentValue;
        } else if (value === '=') {
            if (previousValue && currentValue && operator) {
                currentValue = calculate(previousValue, currentValue, operator);
                display.value = currentValue;
                previousValue = '';
                operator = '';
            }
        } else if (['+', '-', '*', '/', '%'].includes(value)) {
            if (currentValue) {
                if (previousValue && operator) {
                    currentValue = calculate(previousValue, currentValue, operator);
                    display.value = currentValue;
                }
                previousValue = currentValue;
                currentValue = '';
                operator = value;
            }
        } else {
            currentValue += value;
            display.value = currentValue;
        }
    });
});

function calculate(a, b, op) {
    a = parseFloat(a);
    b = parseFloat(b);
    switch (op) {
        case '+':
            return (a + b).toString();
        case '-':
            return (a - b).toString();
        case '*':
            return (a * b).toString();
        case '/':
            return (a / b).toString();
        case '%':
            return (a % b).toString();
    }
}