window.addEventListener("DOMContentLoaded", (event) => {
    const ele = document.getElementById('generate_submit');
    if (ele) {

        const spinner = document.getElementById('generate_loader')
        ele.addEventListener('click', function() {
            spinner.removeAttribute('hidden')
            var option = generate_select.value
            if (option == "Choose File to Generate receipts") {
                alert("Choose a Valid File")
                spinner.setAttribute('hidden',"hidden")
                return
            }
            fetch('/api/receipt/generate/' + option, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json()
            })
            .then(data => {
                console.log(data.message);
                spinner.setAttribute('hidden',"hidden")
            })
        }) 
    }
    else {
        console.log("Fuck")
    }
});

window.addEventListener("DOMContentLoaded", (event) => {
    const el = document.getElementById('email_submit');
    if (el) {
        const spinner = document.getElementById('email_loader')
        el.addEventListener('click', function() {
            var option = email_select.value
            var confirmed = confirm("Are you sure you want to send email?");
            if (!confirmed) {
                return 
            }
            spinner.removeAttribute('hidden')
            if (option == "Choose Directory to Send") {
                alert("Choose Valid PDF Directory")
                spinner.setAttribute('hidden',"hidden")
                return
            }
            fetch('/api/email/' + option, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json()
            })
            .then(data => {
                console.log(data.message);
                spinner.setAttribute('hidden',"hidden")
            })
        })
    }
});