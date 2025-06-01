# Agile Artifacts

## Sprint backlog list of achievables (annotate changes made during sprint, including data required)

- ~~Build shared event view (e.g., matches, training).~~
- ~~Implement “create event” feature for coaches with recurrence options.~~
- ~~Add RSVP system for events~~
- ~~Attendance tracking system~~
- Responsive interface using Bootstrap

## Increment (what must be achieved by the end of the sprint)

- Create a shared event view so players can see and RSVP
- Coaches can create events with a recurrence option
- Coaches can see attendance of players for events
- Coaches can delete events

## Sprint Review (Focus on project management)

### What challenges did you have

- Complexity of teamEvents.html:
  - This file had many components and elements, which made it difficult to navigate and maintain. I struggled at times with integrating new features into the existing layout. However, using Bootstrap components helped streamline the process and ensure a consistent UI.
- SQL Knowledge Gaps:
  - My SQL skills were not always sufficient for certain backend operations, particularly in the dbHandler functions. I had to frequently refer to documentation to resolve issues, especially when implementing conditional/constraint queries.

### What did you do well

- Attendance/RSVP System:
  - I successfully implemented a functional RSVP system. Players can mark their attendance for upcoming events, and coaches have access to a detailed attendance summary that includes both the total number of attendees and the names of confirmed users.
- Role-Based Views (Coach/Player):
  - The conditional rendering of elements based on user roles was effectively implemented. Using simple if statements in Jinja2 templates, I was able to customise the interface for players and coaches, enhancing the clarity and relevance of displayed content.

### What will you do differently next time

- More Thorough Function Planning:
  - I often found myself adding new features on the fly during development. In future sprints, I’ll aim to plan and document feature sets more clearly ahead of time. Improved early stage communication with the clients could also help anticipate functionality that improves the user experience.
