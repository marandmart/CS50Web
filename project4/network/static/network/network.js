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