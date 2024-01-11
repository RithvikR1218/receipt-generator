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
                    return response.json().then(text => { throw new Error(text.error) })
                }
                return response.json()
            })
            .then(data => {
                console.log(data.message);
                spinner.setAttribute('hidden',"hidden")
                window.location.reload();
            })
        }) 
    }
});


window.addEventListener("DOMContentLoaded", (event) => {
    const elem = document.getElementById('generate_delete');
    if (elem) {
        const spinner = document.getElementById('generate_loader')
        elem.addEventListener('click', function() {
            var option = generate_select.value
            if (option == "Choose File to Generate receipts") {
                alert("Choose a Valid File")
                return
            }
            fetch('/api/receipt/delete/' + option, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(text => { throw new Error(text.error) })
                }
                return response.json()
            })
            .then(data => {
                console.log(data.message);
                window.location.reload();
            })
            .catch(error => {
                alert(error);
            });
        }) 
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
                    return response.json().then(text => { throw new Error(text.error) })
                }
                return response.json()
            })
            .then(data => {
                console.log(data.message);
                spinner.setAttribute('hidden',"hidden")
                window.location.reload();
            })
            .catch(error => {
                alert(error);
            });
        })
    }
});

window.addEventListener("DOMContentLoaded", (event) => {
    const elem = document.getElementById('upload_submit');
    if (elem) {
        elem.addEventListener('click', function() {
            var fileInput = document.getElementById('upload_file');
            // Create FormData object and append the file
            var formData = new FormData();
            formData.append('uploaded_file', fileInput.files[0]);

            fetch('/upload_file/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: formData
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(text => { throw new Error(text.error) })
                }
                return response.json()
            })
            .then(data => {
                console.log(data.message);
                window.location.reload();
            })
            .catch(error => {
                alert(error);
            });
        }) 
    }
});