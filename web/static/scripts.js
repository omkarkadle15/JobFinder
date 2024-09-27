document.getElementById('query-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const postId = document.getElementById('post_id').value;
    const query = document.getElementById('query').value;

    fetch('/query_post', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ post_id: postId, query: query })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('query-response').innerText = data.response;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});