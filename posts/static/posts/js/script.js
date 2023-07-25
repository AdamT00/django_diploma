editBtn = document.querySelectorAll('.update-button');

for (let i = 0; i < editBtn.length; i++) {
    editBtn[i].addEventListener('click', function (e) {
        e.preventDefault();
        let txt = document.getElementById('txt' + editBtn[i].id.match(/\d+/)[0])
        let url = 'http://127.0.0.1:8000/swagger/comment/';
        let id = editBtn[i].id.match(/\d+/)[0];
        let token = 'e5c47a241dafc1876fd1bbdc548ec66e81a1a714';

        fetch(url + id, {
            headers: {
                'Authorization': 'Token ' + token,
            }
        })
            .then((response) => response.json())
            .then((json) => {
                let post_id = window.location.pathname.split('/')[2];
                txt.innerHTML = `
                <form method="post" action="/update-comment/`+ id +`/">
                    <input type="hidden" name="post_id" value="`+ post_id +`">
                    <textarea class="textarea input-bordered w-full text-base" name="comment" rows="5">` + json.text + `</textarea>
                    <input type="submit" class="btn bg-primary w-full hover:bg-emerald-800" value="Save">
                </form>
                `;
            });
    });
}
