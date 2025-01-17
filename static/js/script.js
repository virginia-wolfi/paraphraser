document.addEventListener('DOMContentLoaded', function() {
    const pills = document.querySelectorAll('.pill');
    const textarea = document.querySelector('textarea[name="sentence"]');

    // Function to update the textarea placeholder based on the active pill
    function updatePlaceholder() {
    const activePill = document.querySelector('.pill.active');
    if (activePill) {
        const value = activePill.getAttribute('data-value');
        const textarea = document.querySelector('textarea[name="sentence"]');
        textarea.placeholder = value === 'tree' ?
            '(ROOT\n  (S\n    (NP (NNP Sunset))\n    (VP\n      (VBD painted)\n      (NP (DT the) (NN sky))\n      (PP\n        (IN in)\n        (NP\n          (NP (NNS hues))\n          (PP (IN of) (NP (NN orange) (CC and) (NN pink)))))\n      (. .)))' :
            'Sunset painted the sky and sea in hues of orange and pink.';
    }
}

    // Add event listeners to pills for click events
    pills.forEach(function(pill) {
        pill.addEventListener('click', function() {
            // Remove active class from all pills
            pills.forEach(function(p) {
                p.classList.remove('active');
            });

            // Add active class to the clicked pill
            pill.classList.add('active');

            // Check the corresponding radio button
            const radio = pill.querySelector('input[type="radio"]');
            if (radio) {
                radio.checked = true;
            }

            // Clear the textarea
            textarea.value = '';

            // Update placeholder text based on the selected pill
            updatePlaceholder();
        });
    });

    // Update placeholder on page load based on the default selected tab
    updatePlaceholder();

    // Set animation delay for list items
    const listItems = document.querySelectorAll('#list li');
    const delayIncrement = 0.2; // Delay increment in seconds
    listItems.forEach((item, index) => {
        item.style.animationDelay = `${(index + 1) * delayIncrement}s`;
    });
});