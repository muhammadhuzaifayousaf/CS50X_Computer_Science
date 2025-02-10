// Welcome button functionality
const welcomeBtn = document.getElementById('welcomeBtn');
if (welcomeBtn) {
    welcomeBtn.addEventListener('click', () => {
        alert('Welcome to Programming Languages Hub! Happy learning! 🚀');
    });
}

// Python code execution simulation
function runCode() {
    alert('Output: Hello, Python Developer!');
}

// JavaScript color changing demo
function changeColor() {
    const text = document.getElementById('colorText');
    if (text) {
        const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffeead'];
        const randomColor = colors[Math.floor(Math.random() * colors.length)];
        text.style.color = randomColor;
    }
}

// Contact form handling
function handleSubmit(event) {
    event.preventDefault();
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    alert(`Thank you for your message, ${name}!\nWe'll get back to you at ${email} soon.`);

    // Reset form
    event.target.reset();
}
