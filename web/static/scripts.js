document.addEventListener('DOMContentLoaded', function() {
    const linkedinForm = document.getElementById('linkedin-form');
    const modal = document.getElementById('email-modal');
    const sendEmailBtns = document.querySelectorAll('.send-email-btn');
    const closeBtn = document.querySelector('.close');
    const emailForm = document.getElementById('email-form');
    const seeMoreBtns = document.querySelectorAll('.see-more');

    if (linkedinForm) {
        linkedinForm.addEventListener('submit', function(e) {
            const position = document.getElementById('position').value;
            const experience = document.getElementById('experience').value;
            const location = document.getElementById('location').value;

            if (!position || !experience || !location) {
                e.preventDefault();
                alert('Please select an option for all filters before running the scraper.');
            }
        });
    }

    if (sendEmailBtns.length > 0) {
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
    }

    if (seeMoreBtns.length > 0) {
        seeMoreBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                const contentCell = this.closest('.post-content');
                const fullContent = contentCell.querySelector('.full-content');
                const shortContent = contentCell.querySelector('p');
                const seeMoreBtn = shortContent.querySelector('.see-more');
                const seeLessBtn = fullContent.querySelector('.see-more');

                if (fullContent.style.display === 'none') {
                    shortContent.style.display = 'none';
                    fullContent.style.display = 'block';
                    seeMoreBtn.textContent = 'See Less';
                    seeLessBtn.textContent = 'See Less';
                } else {
                    shortContent.style.display = 'block';
                    fullContent.style.display = 'none';
                    seeMoreBtn.textContent = 'See More';
                    seeLessBtn.textContent = 'See More';
                }
            });
        });
    }
});