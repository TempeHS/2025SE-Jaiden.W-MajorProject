# Agile Artifacts

## Sprint backlog list of achievables (annotate changes made during sprint, including data required)

- ~~Team chat functionality~~
- ~~Private messaging between users~~
- ~~Allow for search function for chat by keywords.~~
- ~~Responsive interface using Bootstrap~~

## Increment (what must be achieved by the end of the sprint)

- User can message both their team and a person privately
- User can search for previous chats
- Messages are securedly stored in the database

## Sprint Review (Focus on project management)

### What challenges did you have

- Naming Conventions for Private Messaging Rooms:

  - While implementing private messaging, I encountered challenges in consistently naming chat rooms between users. To solve this, I used Python’s `sorted()` function and created room names in the format 'dm_user1_user2', ensuring alphabetical consistency for all user combinations.

- Limited JavaScript Experience:
  - I had little prior experience with JavaScript, which became a challenge when implementing real-time features using Socket.IO. I followed a tutorial ([YouTube Guide](https://www.youtube.com/watch?v=mkXdvs8H7TA)), which helped with team chat, but was insufficient for private messaging. To bridge the gap, I relied on GitHub Copilot for real-time code suggestions.

### What did you do well

- Storing and Securing Messages in the Database:

  - I extended the tutorial implementation by adding backend logic to store messages in a database, enabling users to view past conversations. I ensured inputs were sanitised and used parameterised queries to prevent SQL injection and maintain data integrity.

- Effective Use of Documentation and Resources:
  - I made strong use of Flask-SocketIO documentation and various online resources to expand beyond the basic tutorial. This allowed me to implement key features like private messaging and enhanced room management.

### What will you do differently next time

- Develop JavaScript Proficiency:
  - Moving forward, I aim to develop a stronger understanding of JavaScript. This will improve my ability to build dynamic front-end features independently and reduce reliance on AI tools. It’s also an important step for expanding my web development skillset and preparing for future opportunities.
