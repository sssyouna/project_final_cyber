// Toggle result sections
function showResult(id) {
    const resultSection = document.getElementById(id);
    resultSection.classList.toggle('active');
}

// Simulate triggering errors
function triggerError() {
    showResult('m2-result');
}

// Simulate directory browsing
function browseDirectory() {
    showResult('m3-result');
}

// Simulate accessing .env file
function accessEnvFile() {
    showResult('m4-result');
}

// Simulate CORS exploitation
function exploitCORS() {
    showResult('m7-result');
}

// Simulate checking headers
function checkHeaders() {
    showResult('m8-result');
}

// Simulate cookie inspection
function inspectCookie() {
    showResult('m9-result');
}

// Simulate checking server banner
function checkBanner() {
    showResult('m10-result');
}

// Simulate triggering verbose error
function triggerVerboseError() {
    showResult('m11-result');
}

// Simulate port scanning
function scanPorts() {
    showResult('m12-result');
}

// Simulate checking permissions
function checkPermissions() {
    showResult('m13-result');
}

// Simulate accessing debug info
function accessDebugInfo() {
    showResult('m14-result');
}

// Simulate JWT brute forcing
function bruteForceJWT() {
    showResult('m15-result');
}