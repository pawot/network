document.addEventListener('DOMContentLoaded', function() {
    const follow_button = document.querySelector('.follow-button');
    const editButtons = document.querySelectorAll('.edit-post');
    const likeButtons = document.querySelectorAll('.thumb-container');
    const likeInfo = document.querySelectorAll('.like-info');

    if (likeInfo) {
        likeInfo.forEach(info => {
            if (info.children.length > 0) {
                thumb_container = document.querySelector(`#unlike-${info.dataset.postId}`);
                thumb_container.classList.remove('hidden');
            }
            else {
                thumb_container = document.querySelector(`#like-${info.dataset.postId}`);
                thumb_container.classList.remove('hidden');
            }
        })

    }

    if (follow_button) {
        follow_button.addEventListener('click', () => change_follow(follow_button.id));
    } 

    if (editButtons) {
        editButtons.forEach(editButton => editButton.addEventListener('click', () => edit_post(editButton.dataset.postId)));
    };

    if (likeButtons) {
        likeButtons.forEach(likeButton => likeButton.addEventListener('click', () => like_post(likeButton.dataset.postId, likeButton.dataset.type)));
    };
});


function change_follow(value) {
    const author = document.querySelector('#author_name').innerHTML;
    fetch('/change_follow', {
        method: 'POST',
        body: JSON.stringify({
            value: value,
            author: author
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        document.querySelector('#followers').innerHTML = "Followers: " + result.followers;  
        document.querySelector('#following').innerHTML = "Following: " + result.following;
        button_container = document.querySelector('#follow-button-container');
        button_container.innerHTML = "";
        if (value == "follow") {
            button = document.createElement('button');
            button.setAttribute('id', 'unfollow');
            button.setAttribute('class', 'follow-button btn btn-outline-danger');
            button.innerHTML = "Unfollow";
            button.addEventListener('click', () => change_follow(button.id));
            button_container.append(button);
        }
        else if (value == "unfollow") {
            button = document.createElement('button');
            button.setAttribute('id', 'follow');
            button.setAttribute('class', 'follow-button btn btn-outline-primary');
            button.innerHTML = "Follow";
            button.addEventListener('click', () => change_follow(button.id));
            button_container.append(button);
        }
    })
}


function edit_post(post_id) {
    oldText = document.querySelector(`#text-${post_id}`);
    newForm = document.createElement('form');
    newForm.setAttribute('data-post-id', post_id);
    newForm.setAttribute('id', `form-${post_id}`);
    newForm.setAttribute('class', 'edit-form');
    newText = document.createElement('textarea');
    newText.setAttribute('id', `new-text-${post_id}`);
    newText.setAttribute('class', 'form-control');
    newText.innerHTML = oldText.innerHTML;
    submit = document.createElement('input');
    submit.setAttribute('class', 'btn btn-primary');
    submit.setAttribute('type', 'submit');
    
    newForm.append(newText, submit);
    oldText.parentNode.replaceChild(newForm, oldText);
    const editForms = document.querySelectorAll('.edit-form');
    if (editForms) {
        editForms.forEach(editForm => editForm.onsubmit = () => {
            text = document.querySelector(`#new-text-${editForm.dataset.postId}`)
            fetch(`/update_post/${editForm.dataset.postId}`, {
                method: 'PUT',
                body: JSON.stringify({
                    text: text.value
                })
            })
            .then(response => response.json())
            .then(post => {
                console.log(post);
                postText = document.createElement('p');
                postText.setAttribute('id', `text-${editForm.dataset.postId}`);
                postText.setAttribute('class', 'text');
                postText.innerHTML = post['text'];
                form = document.querySelector(`#form-${editForm.dataset.postId}`);
                form.parentNode.replaceChild(postText, form);
            })        
            return false
        }) 
    }
}


function like_post(post_id, type) {
    fetch(`/like_post/${post_id}/${type}`)
    .then(response => response.json())
    .then(post => {
        console.log(post);
        document.querySelector(`#num-likes-${post_id}`).innerHTML = post.num_likes;
        if (type == "like") {
            document.querySelector(`#like-${post_id}`).classList.add('hidden');
            document.querySelector(`#unlike-${post_id}`).classList.remove('hidden');            
        }
        else if (type == "unlike") {
            document.querySelector(`#unlike-${post_id}`).classList.add('hidden');
            document.querySelector(`#like-${post_id}`).classList.remove('hidden');            
        }
    })
}

