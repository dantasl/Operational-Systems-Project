# Operational Systems Project (Task 3) - Semaphore

A simple application to monitor how much percent of the main memory is being consumed at the time and signal this data to 
three different colored <b>Light Emitting Diodes</b> (LEDs): green, yellow and red ones.

Its output reminds how a traffic light works, thus the project's name is Semaphore.

## What it should do?

To be considered fully operational, Semaphore must:

* Monitor the main memory's percentage of consume;
* If consume is <b>less than 25%</b>, light only the green led out;
* If consume is <b>greater than 25%</b> and <b>less than 50%</b>, light only the yellow led out;
* If consume is <b>greater than 50%</b> and <b>less than 75%</b>, light only the red led out;
* If consume is <b>greater than 75%</b>, initiate the panic sequence.

The panic sequence described above consists in:

* All leds start to blink (0.5 seconds in, 0.5 seconds out);
* The system starts to verify if the panic button is being pressed;
* If (or when) the panic button is pressed, the process that caused the high memory peak <b>shall be killed</b>;
* After the process is killed, all leds are turned off for <b>3 seconds</b>;
* The system goes back to its previous state of monitoring.

## How it was implemented?

We implemented the monitoring part in <b>Bash Script</b>. You can find the code in <code>/src/<b>semaphore.sh</b></code>.

There you'll see that the code was divided in sections from 0 to 4, each one with comments and a clear implementation and we highly recommend you to check out the source.

Since we implemented the hardware part using the <b>Beagle Bone Black (BBB)</b> single board computer, you can check out
the schematics both in a PNG file (<code>/docs/<b>schematics.png</b></code>) and a Fritzing file (<code>/docs/<b>schematics.fzz</b></code>), the one that suits you better.

Also, there is a simple <b>C++</b> code to stress out the main memory consumption. It was developed <b>purely by empirical analisys</b> (the one that worked with the BBB that we were using), so you may have to change the values to work properly on yours.

Contact us for any doubts. ;)
