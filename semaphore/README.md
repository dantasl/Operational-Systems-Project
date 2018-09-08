# Operational Systems Project (Task 3) - Semaphore

A simple application to monitor how much percent of the main memory is being consumed at the time and signal this data to 
three different colored Light Emitting Diodes (LEDs): green, yellow and red ones.

Its output reminds how a traffic light works, thus the project's name is Semaphore.

## What it should do?

To be considered fully operational, Semaphore must:

* Monitor the main memory's percentage of consume;
* If consume is less than 25%, light only the green led out;
* If consume is greater than 25% and less than 50%, light only the yellow led out;
* If consume is greater than 50% and less than 75%, light only the red led out;
* If consume is greater than 75%, initiate the panic sequence.

The panic sequence described above consists in:

* All leds start to blink (0.5 seconds in, 0.5 seconds out);
* The system starts to verify if the panic button is being pressed;
* If (or when) the panic button is pressed, the process that caused the high memory peak shall be killed;
* After the process is killed, all leds are turned off for 3 seconds;
* The system goes back to its previous state of monitoring.

## How it was implemented?
