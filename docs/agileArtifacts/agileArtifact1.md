# Agile Artifacts

## Sprint backlog list of achievables (annotate changes made during sprint, including data required)

- ~~User registration and login system (Coach / Player roles)~~
- ~~Create/join a volleyball team~~
- ~~2FA Authentication~~
- ~~Passwords hashed and securely stored~~
- ~~Implement a strict content security policy~~
- ~~Secure session management~~
- ~~Privacy Handling Policy~~
- Responsive interface using Bootstrap

## Increment (what must be achieved by the end of the sprint)

- SQLite database design and integration for login/sign-up
- Roles clearly defined for user
- Functioning Login & Sign-up page
- Functioning Team page
- Players can join a team
- Coaches can make a team

## Sprint Review (Focus on project management)

### What challenges did you have

- 2FA Reuse & Security Logic:

  - While reusing my 2FA logic from a previous project, I encountered a security flaw: the QR code for authentication was displaying every time a user logged in, defeating the purpose of using a one-time setup. To resolve this, I introduced a new column in the SQL database to act as a flag, only showing the QR code on initial account setup. Implementing this took time and debugging but ultimately improved security and user experience.

- Database Redesign During Development:

  - As I progressed with building out features for my PWA, I frequently had to adjust the database schema. Had to add new columns to support features like roles. This iterative redesign slowed down development.

- Dynamic Data Rendering for Team Pages:
  - I initially struggled with how to use the same frontend layout across different team pages (e.g. separate chats and events per team) while loading the correct backend data dynamically. After researching Flask documentation and forums, I discovered that dynamic routing with Flask (@app.route('/team/<team_id>')) could be used to render content conditionally based on the team ID.

### What did you do well

- Code Reusability from Previous Project:

  - I effectively leveraged code from a previous secure PWA I had built, which significantly accelerated initial development. Core modules like sanitize.py and twoFactor.py were reused, allowing me to quickly implement critical functionality such as login, sign-up, and 2FA. This saved time and reduced bugs by relying on already tested components.

- Security-by-Design Approach:
  - Reusing secure modules also reinforced a security-by-design methodology. The inherited codebase already included essential security practices such as session management, CSRF protection, and a strict Content Security Policy. This meant that strong security measures were embedded from the beginning of development, rather than being added as an afterthought.

### What will you do differently next time

- Plan the SQL Database Schema in Advance:

  - To avoid inefficiencies caused by frequent redesigns of the database structure, I will invest more time in planning a comprehensive and scalable schema during the design phase. This will improve development flow and reduce time spent modifying the database during production.

- Review Documentation Early (e.g., Flask):
  - I’ll prioritise reviewing documentation for core frameworks like Flask before jumping into development. Understanding the built-in functionality will help streamline implementation, reduce trial-and-error, and guide my decisions more effectively.
