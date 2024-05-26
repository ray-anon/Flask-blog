const likes = document.querySelectorAll('.like');

likes.forEach(like => {
    
    like.addEventListener('click', changecolor);
});

function changecolor() {
    this.style.backgroundColor = 'blue'
}
