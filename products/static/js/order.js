document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('order_form');
  form.addEventListener("submit", submitHandler);
  function submitHandler(event) {
    event.preventDefault();
    console.log(event)
    console.log(form)
    fetch('/products/checkout/', {method: 'POST', body: new FormData(form)})
    .then(response => {
      if(!response.ok) {
        throw new Error('Network response not ok')
      }
      return response.json()})
    .then(data => {
      console.log(data)
      if(data.message === 'success') {
        alert('Success!');
        form.reset();
      }
    })
    .catch(error => {
      console.error('fetch error', error)
    })
  }

 
});
