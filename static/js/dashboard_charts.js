


// Connection status handling
document.body.addEventListener('htmx:sseOpen', function(_) {
	document.getElementById('connection-indicator').className = 'loading loading-ring loading-sm text-success';
	document.getElementById('connection-status').textContent = 'Connected';
});
document.body.addEventListener('htmx:sseError', function(_) {
	document.getElementById('connection-indicator').className = 'loading loading-ring loading-sm text-error';
	document.getElementById('connection-status').textContent = 'Connection Error';
});


function showCriticalAlert(data) {
	const alertHtml = `
	<div role="alert" class="alert alert-error text-white mb-4" id="critical-alert">
		<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="h-6 w-6 shrink-0 stroke-current">
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
		</svg>
		<span><strong>🚨 Critical Alert:</strong> Temp ${data.temperature}°C, Humidity ${data.humidity}%</span>
	</div>
	`;

	if (!document.getElementById('critical-alert')) {
		document.querySelector('.container').insertAdjacentHTML('afterbegin', alertHtml);
		setTimeout(() => {
			document.getElementById('critical-alert')?.remove();
		}, 10000); // Auto-dismiss after 10 seconds
	}
}

launchScripts()

function launchScripts() {

	let tempChart, humidityChart;


	// Update charts when new data arrives
	document.body.addEventListener('htmx:afterSwap', function(e) {
		if (e.target.id === 'chart-data') {
			const dataElement = e.target.querySelector('[data-temp]') || e.target;

			if (dataElement.dataset.temp) {
				const tempData = JSON.parse(dataElement.dataset.temp);
				const humidityData = JSON.parse(dataElement.dataset.humidity);
				const labels = JSON.parse(dataElement.dataset.labels);

				if (tempChart && humidityChart) {
					// Update existing charts
					tempChart.data.datasets[0].data = tempData;
					tempChart.data.labels = labels;
					tempChart.update('none'); // No animation for smooth updates

					humidityChart.data.datasets[0].data = humidityData;
					humidityChart.data.labels = labels;
					humidityChart.update('none');


				} else {
					// Create charts for the first time
					const charts = initCharts(tempData, humidityData, labels);
					tempChart = charts.tempChart;
					humidityChart = charts.humidityChart;
					console.log("Charts created")
				}
			}
		}
	});
}


function initCharts(tempData, humidityData, labels) {
	const tempCtx = document.getElementById('tempChart').getContext('2d');
	const tempChart = new Chart(tempCtx, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [{
				data: tempData,
				borderColor: 'rgb(99, 102, 241)',
				backgroundColor: 'rgba(99, 102, 241, 0.1)',
				borderWidth: 2,
				fill: true,
				tension: 0.4
			}]
		},
		options: {
			responsive: true,
			maintainAspectRatio: false,
			plugins: { legend: { display: false } },
			scales: {
				y: { beginAtZero: false },
				x: { display: false }
			}
		}
	});

	const humidityCtx = document.getElementById('humidityChart').getContext('2d');
	const humidityChart = new Chart(humidityCtx, {
		type: 'line',
		data: {
			labels: labels,
			datasets: [{
				data: humidityData,
				borderColor: 'rgb(16, 185, 129)',
				backgroundColor: 'rgba(16, 185, 129, 0.1)',
				borderWidth: 2,
				fill: true,
				tension: 0.4
			}]
		},
		options: {
			responsive: true,
			maintainAspectRatio: false,
			plugins: { legend: { display: false } },
			scales: {
				y: { beginAtZero: false },
				x: { display: false }
			}
		}
	});
	return { tempChart, humidityChart }
}

