# FitTrack - Gym Workout Tracker

A desktop app built with customtkinter. The idea is to have something simple but complete enough to actually use day to day for tracking gym progress.

---

## Auth

Basic signup and login. Signup asks for name, profile image, email and password. Login just needs email and password.

---

## Profile Setup (First Login)

When someone logs in for the first time they should be prompted to fill out some info about themselves before they can use the app. Things like:

- Height and current weight
- Gender
- Target weight
- Goal — pick from options like: Getting Lean, Build Muscle Mass, Reduce Weight, Maintain Weight, etc.
- Target muscles — Back, Shoulder, Arm, Chest, Abs, Glute, Leg, or Full Body
- Optional: 1RM (max) for Squat, Bench Press, Deadlift

---

## Exercises

There will be a bunch of exercises already built into the app. Each exercise has:
- Name
- Target muscle group
- An image

Users can also add their own custom exercises with the same fields.

---

## Workout Plans

Users can create their own workout plans. When building a plan:
- Give it a name
- Add one or more exercises
- For each exercise, set how many sets, and for each set define the reps and weight
- Can go back and edit a plan later

---

## Logging a Workout

On the current day the user can pick one of their saved workout plans and start a session. During the session:
- Each set of each exercise can be ticked off as done
- The user can change the reps/weight on the fly for that session (since in practice you might not hit the planned numbers)
- After finishing, show a quick summary/report of what was done

One workout per day only.

---

## Workout History

A calendar-style or list view showing which days the user worked out and what exercises they did. Clicking on a past session shows a quick report of that session.

---

## Body Weight Tracking

The user can log their weight for the day. One entry per day.

Optional: A graph showing how body weight has changed over time.

---

## Notes

- Desktop app only, no backend/server, local storage probably with SQLite
- Keep the UI clean and functional, nothing fancy
- The optional stuff (1RM, weight graph) can be added later if time allows
