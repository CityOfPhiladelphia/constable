# Constable

A rather nice authentication and authorization service

## Features

- Authentication
	- Login Providers
		- Local - Username/Password
		- TBD: SAML
		- TBD: Google
		- TBD: Facebook
		- TBD: LDAP
	- Sessions
		- Shared - Shares master session
		- TODO: Application - Application specific session and secret
	- Single Sign-On
		- Shared master session
		- TODO: Shared Application Session
		- TBD: SAML
	- TODO: OAuth
		- For mobile, native, 3rd party API access, and often used for SSO
	- Two Factor Authentication
		- TODO: TOTP - Hardware and authenticator apps
		- TODO: Email
		- TBD: SMS
	- API Tokens
		- User generated tokens - API key style
		- TODO: OAuth token exchange
		- TODO: refresh tokens
- Authorization
	- TODO: Role Based Access Control (RBAC)
		- Users
			- Can have roles
			- Can be a member of many groups
		- Group
			- Used to group users
			- Can have roles
			- Can be a member of groups
			- Can have user memberships
		- Role
			-  Used to group permissions
		- Permission
			- Has an action on a resource
			- Optional filter ex `{ entity: ‘projects’, op: ‘=‘, id: 34 }`
	- TODO: Scopes
		- A scope is all or a subset, a scope, of permissions a user has
		- Tokens can have scopes assoicated with them, limiting how much permissions of a user they have
		- Needed for 3rd party API / OAuth
- Views
	- Public / Regular User
		- INPROGRESS: Login
		- TODO: Two Factor Prompt
		- INPROGRESS: Registration
		- TODO: Edit User Profile
		- TODO: Change Password
		- TODO: Change Two Factor Device
		- TODO: Change Recovery Questions
		- TODO: Recover Password
		- TODO: List sessions and tokens - with revoke button
		- TODO: Create API Token
		- TODO: OAuth Scopes/Permissions (part of OAuth exchange)
	- Admin User
		- TODO: List Applications
		- TODO: Create/Edit/View Application
		- TODO: List User
		- TODO: Edit User
			- TODO: Add user to group
			- TODO: Add role to user
		- TODO: List all sessions and token with revoke button
		- TODO: List Groups
		- TODO: Create/Edit/View Group
		- TODO: List Roles
		- TODO: Create/Edit/View Role
		- TODO: List Permissions
		- TODO: Create/Edit/View Permission

## Tech Details

- Passwords
	- Argon2 hashing with 4 rounds
	- [zxcvbn](https://github.com/dropbox/zxcvbn) based minimum strength
		- INPROGRESS: frontend
		- TODO: backend
- Tokens
	- Fernet tokens
		- Encrypted tokens containing
			- Token ID - V4 UUID
			- User ID
			- Expires At
	- A token is first checked against a cyrptographic secret for integrity, then it's expiration is checked, then it's existence in the tokens table.
	- ID is random and the token itself is never stored.
	- Types
		- session - For browsers
		- token - API / OAuth
		- refresh_token - OAuth
- Sessions
	- Session tokens are use an HttpOnly, Secure cookie
	- Expire after 12 hours
- Login
	- Throttles failed login attempts by global, IP, network, and network/ip/user combinations
	- Logs login failures and successes into `auth_log` table (with username, IP, and User-Agent)
	- Enforces a maximum number of active user sessions (default 10)
- CSRF
	- Login provides a CSRF token (Fernet) that is assoicated with the session
	- Any HTTP method that is not GET, HEAD, or OPTIONS requires a CSRF token in the `X-CSRF` header
- Auth Log
	- Events
		- `failed_login_attempt`
       - `failed_password_recovery_attempt`
       - `login`
       - `password_change`
       - `password_recovery`
- Models - TODO: doc more details
	- User
	- Token
	- AuthLogEntry
	- Application
	- OAuthScope
	- Group
	- Role
	- Permission
- Routes
	TODO: basic route doc