# Operation Systems Project (Task 1 | Part 2) - Big Brother

If you know your George Orwell, you know that "Big Brother" is watching you. Including the processes that are running on your SO.

## What it should do:

* (1) Given a certain PID, read and prompt to user the information stored in /proc/pid/status
* (2) Prompt to user periodically how many processes are running in the current time
* (3) Prompt the same as previous item, but this time organized by users
* (4) Given a certain PID, print to a file the tree of processes (its children, grandchildren, etc)

## Running (1):

To run (1), the code is inside <strong>status.cpp</strong> and you must pass the PID as argument. But first, navigate to the directory, via prompt and type:

* <code>make init</code>

This will generate the structure needed to compile and run the code. After this, you can simply type:

* <code>./bin/status {arg}</code>

Where {arg} is the PID of the process that you want to identify the status.

## Running (2) and (3):

I felt way more comfortable creating a bash script for those items. It is inside <code>/src/scripts</code> and its called <code>watcher.sh</code>. Before running, you must make sure that it is an executable script, and if not, simply run this:

* <code>chmod +x watcher.sh</code>

After this, you might run the code typing:

* <code>./watcher.sh {arg}</code>

Where {arg} is an integer argument telling how many seconds the script must wait before checking the list of processes again. This is an optional argument, if none is provided the default value is set to 5. 

To stop the script you must simply type:

* <code>Ctrl + C</code>

## Running (4):
