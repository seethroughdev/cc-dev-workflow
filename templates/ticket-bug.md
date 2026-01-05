# Bug Template

## Bug Description
[Clear description of the bug]

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- Browser:
- OS:
- Version:
- User Role:

## Screenshots/Recordings
[Attach if applicable]

## Error Messages/Logs
```
[Paste error messages or logs here]
```

## Impact
- Severity: [Low/Medium/High/Critical]
- Users Affected: [Number/Type]

---

## Example: Login Button Not Responding on Mobile

## Bug Description
The login button on the mobile app does not respond to touch events on iOS devices, preventing users from accessing their accounts.

## Steps to Reproduce
1. Open the app on an iOS device (iPhone 12 or newer)
2. Navigate to the login page
3. Enter valid credentials
4. Tap the "Login" button

## Expected Behavior
The login button should respond to the tap and initiate the authentication process.

## Actual Behavior
The login button does not respond to touch events. No visual feedback is provided and no authentication attempt is made.

## Environment
- Browser: Safari Mobile
- OS: iOS 16.4+
- Version: App v2.1.3
- User Role: All users

## Screenshots/Recordings
[Screenshot showing unresponsive login button]

## Error Messages/Logs
```
No console errors observed
Touch event listeners not firing on button element
```

## Impact
- Severity: High
- Users Affected: All iOS mobile users (~40% of user base)