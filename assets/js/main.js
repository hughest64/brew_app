var dropContent = document.getElementById('main-nav-content');

// Click event to open and close the main nav menu on mobile
window.onclick = function(e) {
if (!e.target.matches('.main-nav-button')) {
    dropContent.style.display = 'none';
    }
};

// Toggle classes to hide or display the detials of a recipe on the recipe list
function toggleLinks(id) {
  var recipe = document.getElementById(id);
  recipe.nextElementSibling.classList.toggle('show-recipe-links');
}
