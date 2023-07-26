const editCommentBtn = document.querySelectorAll('.update-comment-button');
const editPostBtn = document.querySelector('.update-post-button');
const url = 'http://127.0.0.1:8000/';
const token = 'e5c47a241dafc1876fd1bbdc548ec66e81a1a714';

for (let i = 0; i < editCommentBtn.length; i++) {
    editCommentBtn[i].addEventListener('click', function (e) {
        e.preventDefault();
        let id = editCommentBtn[i].id.match(/\d+/)[0];
        let txt = document.getElementById('txt' + id)

        fetch(url + 'comment/' + id, {
            headers: {
                'Authorization': 'Token ' + token,
            },
            credentials: 'same-origin'
        })
            .then((response) => response.json())
            .then((json) => {
                let post_id = window.location.pathname.split('/')[2];
                txt.innerHTML = `
                <form method="post" action="/update-comment/` + id + `/">
                    <input type="hidden" name="post_id" value="` + post_id + `">
                    <textarea class="textarea input-bordered w-full text-base" name="comment" rows="5">` + json.text + `</textarea>
                    <input type="submit" class="btn bg-primary w-full hover:bg-emerald-800" value="Save">
                </form>
                `;
            });
    });
}

editPostBtn.addEventListener('click', function (e) {
    e.preventDefault();
    let id = editPostBtn.id.match(/\d+/)[0];
    let txt = document.getElementById('post' + id)

    fetch(url + 'post/' + id, {
        headers: {
            'Authorization': 'Token ' + token,
        },
        credentials: 'same-origin'
    })
        .then((response) => response.json())
        .then((json) => {
            console.log(json);
            txt.innerHTML = `
                <form method="post" action="/update-post/` + id + `/">
                    <textarea class="textarea input-bordered w-full text-base" name="body" rows="5">` + json.body + `</textarea>
                    <input type="submit" class="btn bg-primary w-full hover:bg-emerald-800" value="Save">
                </form>
                `;
        });
});