# Spike Connect

## Overview

Currently, volleyball teams face fragmented communication across group chats, emails, and verbal reminders, leading to confusion around training schedules, missed updates, and poor attendance tracking. My clients struggle to coordinate efficiently, especially when dealing with last-minute changes. This centralised platform called 'Spike Connect' will be used to manage team communication, confirm attendance at training sessions and matches and send announcements. It serves as a daily tool for my players and coaches to stay organized, informed, and connected with their teams.

### Functional Requirements

- Messaging & Group Communication
- Team Creation & Joining
- Event Scheduling & Attendance Tracking
- User Roles & Group Management
- Search & Navigation

### Non-Functional Requirements

- Security & Privacy
- Usability & Accessibility
- Performance & Reliability
- Scalability & Maintainability
- Availability & Support

## Documentation

- [View the System Report (PDF)](/docs/README_resources/system_report.pdf)

### Project Sprints
- [Sprint-1.0](https://github.com/TempeHS/2025SE-Jaiden.W-MajorProject/tree/Sprint-1.0): Set up secure user authentication with 2FA and implemented role-based login for coaches and players.
- [Sprint-2.0](https://github.com/TempeHS/2025SE-Jaiden.W-MajorProject/tree/Sprint-2.0): Built core functionalities including team creation and attendance tracking with RSVP support.
- [Sprint-3.0](https://github.com/TempeHS/2025SE-Jaiden.W-MajorProject/tree/Sprint-3.0): Added team and private messaging using Flask-SocketIO.
- [Sprint-4.0](https://github.com/TempeHS/2025SE-Jaiden.W-MajorProject/tree/Sprint-4.0): Finalised UI, profile page with accessibility features, and responded to client feedback with new features such as joining multiple teams and team profile pictures.


### Gantt Chart
![Gantt chart of the project](/docs/README_resources/gantt_chart.png "Gantt chart of the project")

## How to use Spike Connect for Developers

### Running Required Files

```bash
python main.py
```

```bash
python api.py
```

### Logging In/Signing Up

> [!TIP]
> Developers can use this working login:
>
> - Username: TestDeveloper
> - Password: Test1234%

### Two Factor Authentication

Users need to authenticate themselves using using [Google Authenticator](https://en.wikipedia.org/wiki/Google_Authenticator)

> [!IMPORTANT]
> Users need to remove the space inbetween the code.

> [!TIP]
> Developers can use this QR code for 2FA for the TestDeveloper account:  
> ![2FA tip](/docs/README_resources/test_Developer_2FA.png "Use this QR code for TestDeveloper account")

### How to Test Role Based Permissions
> [!TIP]
>Users can switch their role on the profile page which can be accessed through the navbar when logged in.
>![Demonstration of how to switch roles](/docs/README_resources/switching_roles.gif "Demonstration of how to switch roles")

## Demonstrations of Project in Action

### Team Page

![Demonstration of team page](/docs/README_resources/team_page.gif "Demonstration of team page")

### Profile Page

![Demonstration of profile page](/docs/README_resources/profile_page.gif "Demonstration of profile page")

### Messaging Page

![Demonstration of message page](/docs/README_resources/message_page.gif "Demonstration of message page")

### Schedule Pages

#### Player Access

![Demonstration of schedule page for players](/docs/README_resources/schedule_page_player.gif "Demonstration of schedule page for players")

#### Coach Access

![Demonstration of schedule page for coaches](/docs/README_resources/schedule_page_coach.gif "Demonstration of schedule page for coaches")
