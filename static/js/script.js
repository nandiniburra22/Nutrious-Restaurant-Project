$(document).ready(function () {
    // Attach an event handler to the form submission
    $("#contact-form").on("submit", function(event) {
        event.preventDefault(); // Prevent the default form submission

        var formData = $(this).serialize(); // Serialize the form data

        // Make the AJAX request
        $.ajax({
            type: "POST",
            url: "/submit_contact", // Ensure this matches your Flask route
            data: formData,
            success: function(response) {
                console.log(response); // Log the response in the console for debugging
                
                // Hide the form after successful submission
                $("#contact-form").hide(); 
                
                // Show thank you message
                $("#thank-you-message")
                    .text(response.message || "Thank you for submitting the form!") // Use the response message or a default
                    .show(); // Show the thank you message
            },
            error: function(error) {
                console.error("Submission error:", error); // Log error to console for debugging
                alert("There was an error submitting the form. Please try again.");
            }
        });
    });
});
