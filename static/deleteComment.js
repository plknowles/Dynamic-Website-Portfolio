function deleteComment(commentId) {
    var csrf_token = document.getElementsByName('csrf_token')[0].value;
    if (confirm("Are you sure you want to delete this comment?")) {
        fetch(`/delete_comment/${commentId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token
            },
            credentials: 'same-origin'
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                console.error('Failed to delete comment');
            }
        })
        .catch(error => {
            console.error('Error during the fetch operation:', error);
        });
    }
}