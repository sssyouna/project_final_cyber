// Handle login form submission
document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    
    // In a real app, this would send credentials to the server
    alert(`Login attempted for ${email}. In a real application, this would authenticate with the server.`);
});

// Handle JWT token verification
document.getElementById('verifyToken').addEventListener('click', function() {
    const tokenInput = document.getElementById('jwtToken');
    const tokenResult = document.getElementById('tokenResult');
    
    if (!tokenInput.value) {
        alert('Please enter a JWT token to verify.');
        return;
    }
    
    // Display the token for inspection
    tokenResult.style.display = 'block';
    tokenResult.innerHTML = `<strong>Token Analysis:</strong><br>
    Token: ${tokenInput.value}<br><br>
    <strong>Security Alert:</strong> This token was signed with a weak secret (<code>secret123</code>).<br>
    <em>Attackers can forge admin tokens by cracking this weak secret.</em><br><br>
    <strong>Exploitation Hint:</strong> Try using a JWT cracking tool with common weak secrets.`;
});