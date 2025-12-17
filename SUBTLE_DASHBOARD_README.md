# Subtle Dashboard Implementation

## Overview

This implementation creates a more inconspicuous web interface that resembles a typical school website, with only the M15 vulnerability (Weak JWT Secret) being visibly exploitable. This design allows attackers to naturally navigate the site and discover the M15 vulnerability during their exploration.

## Design Philosophy

The subtle dashboard maintains a normal, benign appearance similar to a typical educational institution's website. All 15 security vulnerabilities are still present in the vulnerable version and fixed in the secure version, but the interface no longer explicitly highlights them as "vulnerabilities" to be exploited.

Instead, the M15 vulnerability (Weak JWT Secret) is presented in a way that would naturally attract an attacker's attention during exploration:

### Vulnerable Version Features:
- Normal school website appearance with typical navigation elements
- Standard login form for students
- Educational content and announcements
- A "Token Verification Tool" section that subtly hints at the weak JWT secret
- Developer note that explicitly mentions the weak secret (`secret123`)

### Secure Version Features:
- Same school website appearance
- Standard login form
- Educational content and announcements
- A "Token Verification Tool" section that encourages proper security practices
- No explicit mention of weak secrets or vulnerabilities

## Key Differences from Previous Implementation

1. **Visual Design**: 
   - Removed explicit vulnerability cards and exploitation buttons
   - Adopted a clean, professional school website aesthetic
   - Used appropriate colors and styling for an educational institution

2. **Content Approach**:
   - Framed the interface as a legitimate student portal
   - Included realistic educational content and navigation
   - Presented the M15 vulnerability as a "technical tool" rather than an obvious exploit target

3. **Vulnerability Presentation**:
   - M15 (Weak JWT Secret) is the only explicitly visible vulnerability
   - Other vulnerabilities remain accessible through API endpoints but are not highlighted
   - Attackers must actively explore the site to discover exploitable weaknesses

## Files Created

### Vulnerable Version:
- `/vulnerable_version/sharepy/backend/templates/subtle_vulnerable_dashboard.html` - New subtle dashboard interface
- Updated `/vulnerable_version/sharepy/backend/main.py` to serve the new dashboard

### Secure Version:
- `/secure_version/sharepy/backend/templates/subtle_dashboard.html` - New subtle secure dashboard interface
- Updated `/secure_version/sharepy/backend/main.py` to serve the new dashboard

## How to Test

1. **Vulnerable Version**:
   ```bash
   cd vulnerable_version/sharepy
   docker-compose up --build
   # Access at http://localhost
   ```

2. **Secure Version**:
   ```bash
   cd secure_version/sharepy
   docker-compose up --build
   # Access at https://localhost (with self-signed certificate)
   ```

## M15 Vulnerability (Weak JWT Secret) Presentation

### In the Vulnerable Version:
The token verification tool explicitly mentions:
- The system uses a weak JWT secret (`secret123`)
- Technical staff can forge admin tokens using this weak secret
- Clear exploitation hint for attackers

### In the Secure Version:
The token verification tool encourages:
- Proper token verification practices
- Secure authentication workflows
- No mention of weak secrets or exploitation opportunities

## Educational Value

This subtle approach teaches:
1. **Realistic Reconnaissance**: Attackers must explore a seemingly benign site to find weaknesses
2. **Contextual Vulnerability Discovery**: Vulnerabilities are discovered through normal interaction
3. **Targeted Exploitation**: Only one clear vulnerability is presented, encouraging focused attacks
4. **Contrast Learning**: The difference between secure and vulnerable implementations is more subtle but still present

The design mimics how real-world attackers would approach a target website - through normal exploration and discovery rather than through explicitly labeled vulnerabilities.