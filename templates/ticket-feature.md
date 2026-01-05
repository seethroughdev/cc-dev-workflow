# Feature Template

### User Story

As a [type of user], I want [goal/desire] so that [benefit/reason].

### Description

[Clear description of what needs to be built and why]

### Design & Mockups

- [Figma Design Link]
- [Additional mockups]

### Acceptance Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

### Technical Notes

- [Implementation detail 1]
- [Implementation detail 2]

### Resources

- [Reference link 1]
- [Reference link 2]

---

## Example: Feature: Implement Social Login

### User Story

As a new user, I want to sign in with my existing Google or GitHub account so that I can access the platform without creating a new password.

### Description

Enable users to authenticate using their existing social media accounts (Google, GitHub) for faster onboarding and improved user experience. This eliminates password management friction and leverages trusted OAuth providers.

### Design & Mockups

- [Figma: Login Page Redesign](https://figma.com/example-link)
- [OAuth Flow Diagram](https://example.com/oauth-flow)
- [Account Linking UI](https://figma.com/account-settings)

### Acceptance Criteria

- [ ] User can sign in using Google account
- [ ] User can sign in using GitHub account
- [ ] New user account created on first social login
- [ ] Existing user account can be linked to social accounts
- [ ] User can disconnect social accounts from profile settings
- [ ] OAuth errors display user-friendly messages
- [ ] Session persistence works after social login
- [ ] Email verification handled per OAuth provider status

### Technical Notes

- Implement OAuth 2.0 flow with PKCE for security
- Store OAuth tokens encrypted at rest
- Add rate limiting for OAuth callback endpoints
- Ensure CSRF protection on OAuth endpoints

### Resources

- [OAuth 2.0 Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
- Related: MAY-123 (Add session management)
