This is intended to be a webapp to help people keep up a regular writing habit. 


Simple first pass implementation:
--------
When user first registers, prompt them to say how many words they want to write
per day. 

Allow changing that in preferences.

User home page (what they see on subsequent logins) shows a listing of the past
week with checkmarks next to days they completed the goal.

They get a "free" checkmark for the day they created their account

Also show stats: current streak length in days; longest streak; % of last 100
days where goal was completed. Also, number of words they still need to
complete that day.

Link to page where they can write. 

Listing of their previous writing, with next/prev buttons to cycle through it.

Show "today" sensibly on index page.

Make sure initial login makes sense (shouldn't say "failed to reach goal" for a
bunch of days when you just signed up)


Possible later passes:
-------
When they go to a previous writing, they can edit it. Need to have edits apply
toward word count in a sensible way. I'm thinking: store each "edit" as just a
separate writing object, but keep track of word count. Probably for simplicity
store the full text in each "edit." Add foreign key on "Writing" model to
previous version. Or even add a model for a "group" of writings related by
edit. For keeping track of word count, add field to Writing model that stores
the number of words that writing added - either just the number of words in an
"original" writing or the difference bhetween the current and parent writing.

Ability to share previous writings. Provide a link users can share. Add social
media sharing.

Allow more complex goals - amount of time spent writing? Let it be per
week/month/etc., instead of just per day?


Initial vague goals
--------

Lets the user set goals (like x number of minutes of writing daily), and helps
them track their goals. 

Tracks the time they spend writing in the app, with the option to stop the
timer if the app loses focus. 

Allow option to LIMIT time spent on the writing as well.

Lets the user save their writing, and optionally share it. Allow them to share
an entire set of writings - for example, if they have a goal of spending 10+
minutes writing every day, they can get a shareable link to all of those daily
writings.
