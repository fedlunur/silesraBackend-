$(document).ready(function() {
    // When the image preview is clicked
    $('.open-slider').click(function(event) {
        event.preventDefault();
        
        // Get the image URLs from the data attribute
        const images = $(this).data('images').split(',');

        // Show the image slider modal with navigation
        showImageSlider(images);
    });

    // Function to show the image slider modal with navigation
    function showImageSlider(images) {
        // Create the modal HTML
        const modal = $('<div class="image-slider-modal"></div>');
        const sliderContainer = $('<div class="slider-container"></div>');

        // Create the image elements and add them to the slider container
        images.forEach((image, index) => {
            const img = $('<img class="slider-image">').attr('src', image).hide();
            sliderContainer.append(img);
        });

        // Show the first image
        const firstImage = sliderContainer.find('.slider-image').first().show();
        
        // Add next/previous buttons
        const prevButton = $('<button class="prev-btn">Previous</button>');
        const nextButton = $('<button class="next-btn">Next</button>');
        
        // Track the current image index
        let currentIndex = 0;

        // Counter to show current image index
        const counter = $('<span class="counter">1 / ' + images.length + '</span>');
        
        // Handle the next button click
        nextButton.click(function() {
            if (currentIndex < images.length - 1) {
                currentIndex++;
                updateSlider(currentIndex);
            }
        });

        // Handle the previous button click
        prevButton.click(function() {
            if (currentIndex > 0) {
                currentIndex--;
                updateSlider(currentIndex);
            }
        });

        // Function to update the slider to show the current image
        function updateSlider(index) {
            sliderContainer.find('.slider-image').hide();  // Hide all images
            sliderContainer.find('.slider-image').eq(index).show();  // Show the current image
            counter.text((index + 1) + ' / ' + images.length); // Update counter text
        }

        // Append the buttons, image container, and counter to the modal
        modal.append(prevButton);
        modal.append(sliderContainer);
        modal.append(counter);
        modal.append(nextButton);

        // Close button for the modal
        const closeButton = $('<button class="close-slider">Close</button>');
        closeButton.click(function() {
            modal.remove();
        });

        modal.append(closeButton);

        // Add the modal to the body
        $('body').append(modal);
    }
});
