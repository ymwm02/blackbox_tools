// BlackBox Tools JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to all cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });

    // Auto-scroll console to bottom when new content is added
    const console = document.querySelector('.console');
    if (console && console.value) {
        console.scrollTop = console.scrollHeight;
    }

    // Add loading spinner when form is submitted
    const executeForm = document.querySelector('form[action*="execute"]');
    if (executeForm) {
        executeForm.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            
            submitBtn.innerHTML = '<div class="spinner"></div> Executing...';
            submitBtn.disabled = true;
            
            // Re-enable button after 30 seconds (timeout)
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 30000);
        });
    }

    // Add pulse effect to brand
    const brand = document.querySelector('.navbar-brand');
    if (brand) {
        brand.classList.add('pulse');
    }

    // Add typing effect to console
    function typeWriter(element, text, speed = 50) {
        let i = 0;
        element.value = '';
        
        function type() {
            if (i < text.length) {
                element.value += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }
        
        type();
    }

    // Enhanced form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const target = this.querySelector('input[name="target"]');
            if (target) {
                const targetValue = target.value.trim();
                
                // Basic validation for IP/domain
                const ipRegex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
                const domainRegex = /^[a-zA-Z0-9][a-zA-Z0-9-]{1,61}[a-zA-Z0-9](?:\.[a-zA-Z]{2,})+$/;
                
                if (!ipRegex.test(targetValue) && !domainRegex.test(targetValue)) {
                    e.preventDefault();
                    alert('Please enter a valid IP address or domain name.');
                    target.focus();
                    return false;
                }
            }
        });
    });

    // Add real-time clock
    function updateClock() {
        const now = new Date();
        const timeString = now.toLocaleTimeString();
        const clockElement = document.getElementById('clock');
        if (clockElement) {
            clockElement.textContent = timeString;
        }
    }

    // Update clock every second
    setInterval(updateClock, 1000);
    updateClock(); // Initial call

    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl+Enter to submit form
        if (e.ctrlKey && e.key === 'Enter') {
            const form = document.querySelector('form');
            if (form) {
                form.submit();
            }
        }
        
        // Escape to clear console
        if (e.key === 'Escape') {
            const console = document.querySelector('.console');
            if (console) {
                console.value = '';
            }
        }
    });

    // Add tooltips for buttons
    const buttons = document.querySelectorAll('button, .btn');
    buttons.forEach(button => {
        if (!button.title) {
            switch(button.textContent.trim().toLowerCase()) {
                case 'launch':
                    button.title = 'Execute the selected script (Ctrl+Enter)';
                    break;
                case 'view':
                    button.title = 'View detailed results';
                    break;
                case 'download':
                    button.title = 'Download report as text file';
                    break;
                case 'login':
                    button.title = 'Sign in to access the dashboard';
                    break;
            }
        }
    });

    // Add status indicator
    function addStatusIndicator() {
        const navbar = document.querySelector('.navbar-brand');
        if (navbar) {
            const indicator = document.createElement('span');
            indicator.className = 'status-indicator online';
            indicator.title = 'System Online';
            navbar.appendChild(indicator);
        }
    }

    addStatusIndicator();

    // Add copy to clipboard functionality for console output
    const consoleElement = document.querySelector('.console');
    if (consoleElement) {
        consoleElement.addEventListener('dblclick', function() {
            this.select();
            document.execCommand('copy');
            
            // Show feedback
            const feedback = document.createElement('div');
            feedback.textContent = 'Copied to clipboard!';
            feedback.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: var(--accent-primary);
                color: #000;
                padding: 10px 20px;
                border-radius: 5px;
                z-index: 1000;
                font-weight: bold;
            `;
            document.body.appendChild(feedback);
            
            setTimeout(() => {
                document.body.removeChild(feedback);
            }, 2000);
        });
    }
});

// Utility functions
function clearConsole() {
    const console = document.querySelector('.console');
    if (console) {
        console.value = '';
    }
}

function downloadConsoleOutput() {
    const console = document.querySelector('.console');
    if (console && console.value) {
        const blob = new Blob([console.value], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `blackbox_output_${new Date().getTime()}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }
}

