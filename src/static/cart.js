const checkout = document.querySelector('.credit-info-content');
const button = checkout.querySelector('.pay-btn');


button.addEventListener('click', ()=>{
    const name = checkout.querySelector('#name').value;
    const contact = checkout.querySelector('#contact').value;
    const hostel = checkout.querySelector('#hostel').value;
    const room = checkout.querySelector('#room').value;

    if (!name || !contact || !hostel || !room) {
        alert('Please fill all the details');
        return;
    }

    console.log('Name:', name);
    console.log('Contact:', contact);
    console.log('Hostel:', hostel);
    console.log('Room:', room);
    const data = {name, contact, hostel, room};
    fetch('/append_data', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {'Content-Type': 'application/json'}
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Call the transfer_data function
            alert(data.message);
        } else {
            alert('Error: ' + data.message);
        }
    });
    window.location.href = "homepage.html";
});
