# Agile Artifacts

## Sprint backlog list of achievables (annotate changes made during sprint, including data required)

- ~~Edit profile (name, team, role, password)~~
- ~~Responsive interface using Bootstrap~~
- ~~Dark mode toggle~~
- ~~Large-font accessibility option~~
- ~~Users given the option to delete their data/account~~

## Increment (what must be achieved by the end of the sprint)

- Working profile page that includes accessibility options such as dark mode, and large font
- Users can delete their data/account
- Implement any final client feedback
- Finalise development, going through final testing and debugging

## Sprint Review (Focus on project management)

### What challenges did you have

- Content Security Policy (CSP) and Dark Mode Integration

  - While implementing the dark mode toggle, I encountered an issue where the functionality didn’t apply on the homepage (index.html). Using browser developer tools, I traced the issue to a strict Content Security Policy (CSP) header that was blocking the script. Upon further inspection, I identified a syntax error in my CSP declaration: `"script-src": "'self' AND https://cdnjs.cloudflare.com"` was incorrect. After correcting the syntax to a valid CSP format, the issue was resolved, and dark mode functioned as intended.

- Styling with CSS
  - Achieving a polished and professional look with CSS was initially challenging. While Bootstrap provided a solid foundation, it didn’t fully meet the visual requirements for the interface. I had to write custom CSS to enhance the UI. Given the complexity of styling, I leveraged GitHub Copilot to assist in refining elements and ensuring consistent aesthetics across the PWA.

### What did you do well

- Responsiveness to Client Feedback

  - Meeting with clients in person and conducting black box testing using live data allowed me to validate that the solution aligned with user expectations. A key example was Ms Bolton’s suggestion to allow teams to upload profile pictures. I successfully implemented this feature, enabling coaches to upload images that visually personalise their team pages.

- Implementation of Multi-Team Joining
  - Based on client input, I enabled users to join multiple teams rather than being limited to one. This was achieved through a many-to-many relationship in the database, allowing users to be associated with multiple team_id entries. I updated the relevant database management functions and integrated this change smoothly.

### What will you do differently next time

- More Frequent Client Check-Ins

  - Although I conducted two in-person meetings with each client, more frequent check-ins throughout the sprint would have ensured continuous alignment with user needs. Regular feedback loops could have uncovered more refinements earlier in development.

- CSS and Mobile Responsiveness
  - While the desktop version of the PWA functions well, the mobile layout lacks full responsiveness. For the future, optimising CSS for smaller screens would be needed. Although Bootstrap supports responsive design, some of my custom styles override those defaults and need to be adjusted for a consistent mobile experience.
