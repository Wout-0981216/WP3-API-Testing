fetch('https://api.example.com/investigations')
	.then(response => response.json())
	.then(data => {
		// Update the HTML with the number of ongoing investigations
		document.getElementById('investigationCount1').innerHTML = data[0].count;
		document.getElementById('investigationCount2').innerHTML = data[1].count;
		document.getElementById('investigationCount3').innerHTML = data[2].count;
	})	
	.catch(error => console.error('Error:', error));