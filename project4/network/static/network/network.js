document.addEventListener('DOMContentLoaded', () => {
    // adds an event listener to the "New Post" button
    document.getElementById('showPost').addEventListener('click', newPost);
    // adds an event listener to the close button, within the 
    document.getElementById('closePost').addEventListener('click', closePost);

    // checks if the page has the Follow/Unfollow button within it 
    if (!(document.getElementById('followStatusBtn') === null)) {
        // adds action to clicking the button with functions to get the current user_id value and followstatus
        document.getElementById('followStatusBtn').addEventListener('click', () => followUnfollow(getUserId(), getFollowStatus()));
    }

    // goes through all posts and checks for the edit button
    Array.from(document.getElementsByClassName('editBtn')).forEach(button => {
        button.addEventListener('click', () => {
            // gets the post
            let post_id = button.parentElement.dataset.postid;
            // gets the content of the post
            let content = button.parentElement.querySelector(":nth-child(3)");
            // asks the user for the edited post
            let edit = prompt("Edit your post: ", content.innerHTML);
            // if there was an edit, adds it to the HTML and sends it to the server
            if (edit){
                content.innerHTML = edit;
                fetch(`/edit/${post_id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        edit: edit
                    })
                })
            }
        })
    })

    // goes through all the like buttons
    Array.from(document.getElementsByClassName('likeBtn')).forEach(button => {
        button.addEventListener('click', () => {
            // gets the post div
            let post = button.parentElement;
            // gets the post id
            let post_id = post.dataset.postid;
            // gets the status of the pressed button
            let buttonStatus = button.getAttribute('aria-pressed');
            // gets the dislike button
            let otherButton = post.querySelector('button:last-child');
            // get the status of the other button
            let otherButtonStatus = otherButton.getAttribute('aria-pressed');
            // gets the like count
            let likes = post.querySelector('.likeCount');
            // gets the dislike count
            let dislikes = post.querySelector('.dislikeCount');
            // changes the dislike info
            if (otherButtonStatus === "true"){
                otherButton.setAttribute('aria-pressed', 'false');
                otherButton.className = "dislikeBtn btn btn-outline-danger";
                dislikes.innerHTML = parseInt(dislikes.innerHTML) - 1;
            }
            // if the user liked the post, it reverses that and updates server
            if (buttonStatus === "true"){
                button.setAttribute('aria-pressed', 'false');
                button.className = "likeBtn btn btn-outline-primary";
                likes.innerHTML = parseInt(likes.innerHTML) - 1;
                fetch(`like_dislike/${post_id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        like: "false",
                        dislike: "false"
                    })
                })
            // if the user hadn't liked the post, it adds a like and updates server
            } else if (buttonStatus === "false"){
                button.setAttribute('aria-pressed', 'true');
                button.className = "likeBtn btn btn-outline-primary active";
                likes.innerHTML = parseInt(likes.innerHTML) + 1;
                fetch(`like_dislike/${post_id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        like: "true",
                        dislike: "false"
                    })
                })
            }

        })
    })

    // goes through all the dislike buttons
    Array.from(document.getElementsByClassName('dislikeBtn')).forEach(button => {
        button.addEventListener('click', () => {
            // gets the post div
            let post = button.parentElement;
            // gets the post id
            let post_id = post.dataset.postid;
            // gets the status of the pressed button
            let buttonStatus = button.getAttribute('aria-pressed');
            // gets the like button
            let otherButton = post.querySelector('button:nth-last-child(2)')
            // get the status of the other button
            let otherButtonStatus =  otherButton.getAttribute('aria-pressed');
            // gets the like count
            let likes = post.querySelector('.likeCount');
            // gets the dislike count
            let dislikes = post.querySelector('.dislikeCount');
            // changes the like info
            if (otherButtonStatus === "true"){
                otherButton.setAttribute('aria-pressed', 'false');
                otherButton.className = "likeBtn btn btn-outline-primary";
                likes.innerHTML = parseInt(likes.innerHTML) - 1;
            }
            // if the user dislike the post, it reverses that and updates server
            if (buttonStatus === "true"){
                button.setAttribute('aria-pressed', 'false');
                button.className = "dislikeBtn btn btn-outline-danger";
                dislikes.innerHTML = parseInt(dislikes.innerHTML) - 1;
                fetch(`like_dislike/${post_id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        like: "false",
                        dislike: "false"
                    })
                })
            // if the user hadn't disliked the post, it adds a like and updates server
            } else if (buttonStatus === "false"){
                button.setAttribute('aria-pressed', 'true');
                button.className = "dislikeBtn btn btn-outline-danger active";
                dislikes.innerHTML = parseInt(dislikes.innerHTML) + 1;
                fetch(`like_dislike/${post_id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        like: "false",
                        dislike: "true"
                    })
                })
            }
        })
    })
})

// make the post-area div show up
function newPost() {
    document.getElementById('post-area').style.display = 'block';
    return false;
}
// makes the post-area div go away
function closePost() {
    document.getElementById('post-area').style.display = 'none';
    document.getElementById('post').value = '';
    return false;
}
// follow/unfollow function
function followUnfollow(user_id, followStatus){
    // fetches the url and passes in the current follow status
    fetch(`/user/follow_unfollow/${user_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            followStatus: followStatus
        })
    })
    // button info
    var btn = document.getElementById('followStatusBtn');
    //ammount of followers in the followers count span
    var count = parseInt(document.getElementById('followersCount').innerHTML);
    // if true, it means the owner of the page is currently followed and the code bellows changes the page visually to signal that the user has been unfollowed
    if (followStatus === "True"){
        btn.dataset.followstatus = "False";
        btn.innerHTML = "Follow";
        btn.className = "btn btn-primary";
        document.getElementById('followersCount').innerHTML = count - 1;
    // if false, it means the owner of the page is currently not followed and the code bellows changes page visually to signal that the user has been followed
    } else if (followStatus === "False") {
        btn.dataset.followstatus = "True"
        btn.innerHTML = "Unfollow";
        btn.className = "btn btn-danger";
        document.getElementById('followersCount').innerHTML = count + 1;
    }
}
// gets the user id info on the html for the follow/unfollow button
function getUserId(){
    return parseInt(document.getElementById('followStatusBtn').dataset.userid);
}
// gets the user followstatus info on the html for the follow/unfollow button
function getFollowStatus(){
    return document.getElementById('followStatusBtn').dataset.followstatus;
}