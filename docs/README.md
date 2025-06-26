# Spike Connect

## Overview

Currently, volleyball teams face fragmented communication across group chats, emails, and verbal reminders, leading to confusion around training schedules, missed updates, and poor attendance tracking. My clients struggle to coordinate efficiently, especially when dealing with last-minute changes. This centralised platform called 'Spike Connect' will be used to manage team communication, confirm attendance at training sessions and matches, send announcements, and share multimedia content. It serves as a daily tool for my clients to stay organized, informed, and connected with their teams.

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

- System Report

## How to use Spike Connect for developers

### Running required files

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

### How to test role based permissions

- Users can switch their role on the profile page which can be accessed through the navbar when logged in.

![Demonstration of how to switch roles](/docs/README_resources/switching_roles.gif "Demonstration of how to switch roles")

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
