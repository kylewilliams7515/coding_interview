# Installation Instructions

1. Install the most recent python version (3.10) for your platform of choice (I'm running on a Windows machine, so this would be the [Windows Installer (64 bit)](https://www.python.org/downloads/windows/).
2. Run the Installer, ensuring that the box at the beginning to add python to your path is checked
3. Python should now work from a terminal/powershell window
4. Pull down the main branch of this package from GitHub into your local machine.

# Running
Once python is properly set up and able to be run from a terminal and the code is pulled from GitHub, running the script simply requires `cd`ing into the workspace where you've pulled the code down locally. Then, simply run the script, such as `python availability.py Maggie Joe Jordan`, in order to find shared availabilities.

#Approach

When attacking solving this problem, I first decided to go with Python for the language of the solution due to its simplicity for script writing as opposed to my primary language of choice otherwise, Java.

With regards to the actual algorithm, I wanted to ensure that I was only iterating over the data set a single time in my search for available time slots. In order to do this, I sorted the events in the events data set by start time after pulling them into the script at the beginning. 

After iterating over the user data set to map from user to ID, it was easy to filter out events for users who weren't selected during my one iteration over the events. 

In order to find availabilities, I simply needed to hold the last end time for the previous event and print it along with the start time for the next event.

I also needed to handle a few edge cases, namely:

1. When an event starts at the beginning of a day
2. When the previous event ended on the day prior to the current event
3. When an event ends at the end of a day
4. When the next event starts after the last one ends
5. When a previous event's time frame fully encompasses the time frame of one or more future events

My handling of these edge cases, all of which were demonstrated by the example run for Maggie, Joe, and Jordan, are documented further in comments in the script itself. In brief, in order to handle each of these, I:

1. Don't print any prior availability for a day if the event starts at the beginning of the business day
2. Check the day for the previous event via lastEndTime and next event to determine whether we need to print availability for multiple dates between events
3. When checking the day for the previous event, ensure we're not printing anything if the last end time's hour was 21
4. Ensured we were skipping over events with a start time prior to the last end time, with the caveat that
5. If the next event starts before the last event ends and ends after the last event ends, just update the last end time

Time complexity is O(n), where n is the size of the events data set, due to only having to iterate through it once.
Space complexity is also O(n) as we have to load and store all of the events.