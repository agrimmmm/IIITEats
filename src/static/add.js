const addButtonList = document.querySelectorAll('#addtoplaylist');
addButtonList.forEach((addButton) => {
  addButton.addEventListener('click', () => {
    const item = addButton.dataset.item;
    const canteen = addButton.closest('.ncbox').querySelector('.canteen').textContent;
    const category = addButton.closest('.ncbox').querySelector('.category').textContent;
    const price = addButton.closest('.ncbox').querySelector('.price').textContent;

    // Send data to server to be stored in database
    const data = {item, canteen, category, price};
    fetch('/store_data', {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {'Content-Type': 'application/json'}
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        if (data.message.includes('quantity has been increased')) {
          alert(data.message);
        } else {
          alert("Item has been added to the cart");
        }
      } else {
        alert("Error adding item to the database");
      }
    });
  });
});