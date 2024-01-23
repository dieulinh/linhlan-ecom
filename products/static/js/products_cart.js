// shopping_cart.js test
document.addEventListener('DOMContentLoaded', function() {
  const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');

  addToCartButtons.forEach(button => {
      button.addEventListener('click', function(event) {
        console.log(event)
          const productId = this.dataset.productId;

          // Send a request to add the product to the cart
          fetch(`/products/add-to-cart/${productId}/`)
              .then(response => response.json())
              .then(data => {
                  alert(data.message);  // Display a success message
              })
              .catch(error => {
                  console.error('Error:', error);
              });
      });
  });
});
