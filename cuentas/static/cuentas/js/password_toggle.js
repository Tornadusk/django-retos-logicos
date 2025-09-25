/**
 * Toggle para mostrar/ocultar contraseñas
 */
console.log('Password toggle script starting...');

function applyPasswordToggle() {
    console.log('Applying password toggles...');
    const passwordFields = document.querySelectorAll('input[type="password"]');

    passwordFields.forEach(function(passwordField) {
        if (passwordField.classList.contains('password-toggle-processed')) {
            console.log('Field already processed:', passwordField);
            return;
        }

        console.log('Processing password field:', passwordField);
        passwordField.classList.add('password-toggle-processed');

        const wrapper = document.createElement('div');
        wrapper.className = 'password-field-wrapper';
        passwordField.parentNode.insertBefore(wrapper, passwordField);
        wrapper.appendChild(passwordField);

        const toggleButton = document.createElement('button');
        toggleButton.type = 'button';
        toggleButton.className = 'password-toggle';
        toggleButton.title = 'Mostrar/Ocultar contraseña';
        wrapper.appendChild(toggleButton);

        const eyeIcon = document.createElement('span');
        eyeIcon.style.fontSize = '14px';
        toggleButton.appendChild(eyeIcon);

        function updateIcon() {
            if (passwordField.type === 'password') {
                eyeIcon.innerHTML = '👁'; // Ojo cerrado
                eyeIcon.style.color = '#6c757d'; // Gris
            } else {
                eyeIcon.innerHTML = ''; // Ojo abierto
                eyeIcon.style.color = '#28a745'; // Verde
            }
        }

        toggleButton.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Toggle clicked, current type:', passwordField.type);
            if (passwordField.type === 'password') {
                passwordField.type = 'text';
            } else {
                passwordField.type = 'password';
            }
            updateIcon();
        });

        // Initial icon setup
        updateIcon();
        console.log('Toggle created successfully for field:', passwordField);
    });
}

// Apply toggles on DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, applying toggles...');
    applyPasswordToggle();
});

// Apply toggles for dynamically added content
const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
            console.log('DOM mutation detected, checking for new password fields...');
            // Give a small delay to ensure elements are fully rendered
            setTimeout(applyPasswordToggle, 50);
        }
    });
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});

// Fallback for ensuring toggles are applied
setTimeout(applyPasswordToggle, 100);
setTimeout(applyPasswordToggle, 500);
setTimeout(applyPasswordToggle, 1000);
