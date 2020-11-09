document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('showPost').addEventListener('click', newPost);
    document.getElementById('closePost').addEventListener('click', closePost);8
})

function newPost() {
    document.getElementById('post-area').style.display = 'block';
    return false;
}
function closePost() {
    document.getElementById('post-area').style.display = 'none';
    return false;
}