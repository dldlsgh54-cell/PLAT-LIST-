# Review Approval

Creator OS automates recommendations and checks, but the user gives final approval.

## Flow

```text
AI recommendation
↓
Creator OS check
↓
Waiting for approval
↓
User approval
↓
Render
↓
Final review
↓
Upload
```

## Human Review Queue

Items with low Gemini confidence are sent to the Human Review Queue.

## Rules

- AI recommendations are not final decisions.
- Creator OS checks must run before approval-sensitive steps.
- User approval is required before render.
- Final review is required before upload.
- Low-confidence Gemini results should not be silently accepted.
- Approval events should be logged.
- The Dashboard should show items waiting for user approval.

