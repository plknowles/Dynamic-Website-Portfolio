// AJAX to handle comment delete function
function deleteComment(commentId) {
    // gets the current csrf token
    var csrf_token = document.getElementsByName("csrf_token")[0].value;
    // Pop up a confirm message
    if (confirm("Are you sure you want to delete this comment?")) {
        // Uses the Fetch API to send a DELETE request to the server
        fetch(`/comments/${commentId}`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrf_token, // Sends the retrieved CSRF token in the header for security
            },
            credentials: "same-origin", // Sends credentials/cookies along with the request
        })
            .then((response) => {
                if (response.ok) {
                    // Reloads the page after successful comment deletion
                    window.location.reload();
                } else {
                    //Logs an error if the server response indicates failure
                    console.error("Failed to delete comment");
                }
            })
            .catch((error) => {
                // Logs an error if fetch operation fails
                console.error("Error during the fetch operation:", error);
            });
    }
}
