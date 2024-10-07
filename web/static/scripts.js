document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('email-modal');
    const sendEmailBtns = document.querySelectorAll('.send-email-btn');
    const closeBtn = document.querySelector('.close');
    const emailForm = document.getElementById('email-form');

    sendEmailBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            const email = this.getAttribute('data-email');
            document.getElementById('post-id').value = postId;
            document.getElementById('to').value = email;
            modal.style.display = 'block';
        });
    });

    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });

    emailForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        fetch('/send_email', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            modal.style.display = 'none';
            emailForm.reset();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while sending the email.');
        });
    });

    // See More functionality
    document.querySelectorAll('.see-more').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            const contentDiv = this.previousElementSibling;
            if (contentDiv.classList.contains('expanded')) {
                contentDiv.classList.remove('expanded');
                this.textContent = 'See More';
            } else {
                fetch(`/get_full_content/${postId}`)
                    .then(response => response.json())
                    .then(data => {
                        contentDiv.innerHTML = `<p><strong>Content:</strong> ${data.content}</p>`;
                        contentDiv.classList.add('expanded');
                        this.textContent = 'See Less';
                    });
            }
        });
    });
});