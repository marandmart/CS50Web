document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('showPost').addEventListener('click', new_post);
})

function new_post() {
    document.getElementById('post-area').style.display = 'block';
}