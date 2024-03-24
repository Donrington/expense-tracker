// document.addEventListener('DOMContentLoaded', function () {
//     const expensesData = JSON.parse('{{ expenses|tojson|safe }}');
//     loadExpensesAndUpdateChart(expensesData);
// });

// function loadExpensesAndUpdateChart(expenses) {
//     // Assuming you have an element with id='expense-list' in your HTML
//     const expenseList = document.getElementById('expense-list');
//     expenses.forEach(expense => {
//         const li = document.createElement('li');
//         li.textContent = `${expense.category}: $${expense.amount}`;
//         expenseList.appendChild(li);
//     });

//     // Prepare data for Chart.js
//     const labels = expenses.map(expense => expense.category);
//     const data = expenses.map(expense => expense.amount);

//     // Assuming you have an element with id='expensesChart' in your HTML
//     const ctx = document.getElementById('expensesChart').getContext('2d');
//     const expensesChart = new Chart(ctx, {
//         type: 'bar',
//         data: {
//             labels: labels,
//             datasets: [{
//                 label: 'Expenses by Category',
//                 data: data,
//                 backgroundColor: [
//                     // Colors
//                 ],
//                 borderColor: [
//                     // Border Colors
//                 ],
//                 borderWidth: 1
//             }]
//         },
//         options: {
//             scales: {
//                 y: {
//                     beginAtZero: true
//                 }
//             }
//         }
//     });
// }