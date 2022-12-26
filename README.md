# Line-Stretcher---Akamai2022
Summer 2022 Akamai Internship project: control system for the EHT (Event Horizon Telescope) Greenland Telescope's Fiber Optic System. I was working for ASIAA and the SMA. All codes and programs included are for the software servo PID algorithm that controls a Line Stretcher, correcting for phase drift in the fiber optic system.  

Project Title: Phase Stabilization of a Fiber Optic System using a Line Stretcher 

Project Description: This project was my main objective during my Summer 2022 Akamai Internship. The project was outlined by ASIAA (Academia Sinica Institute of Astronomy and Astrophysics) and the Smithsonian Astrophysical Observatory. My task was to create a lab prototype control system for a Line Stretcher to correct for phase drift in fiber optic cables carrying signal to the telescope. 
This collection of programs were written for the Greenland Telescope’s (GLT) fiber optic system. The collection of programs together create a control system for a Line Stretcher- a device that uses piezoelectric crystals to stretch or contract fiber optic cables. The GLT is a partner in the Event Horizon Telescope, an international array of radio telescopes used to capture black holes and other space objects using interferometry, meaning the alignment and timing accuracy of the radio beams must be precise. Phase drift in the signals going to and from the telescopes causes delays, and compromises the quality of the synthesized images. ASIAA wanted to introduce a Line Stretcher into the GLT’s fiber optic system to counteract phase drift ideally to ± 0.1 degrees. 

The below schematic depicts our system setup. A 10 MHz reference helps generate a 15.75 GHz Pilot tone and a 15.76 GHzReference tone. The Pilot tone is transmitted through the fiber optic cable and fed into the Line Stretcher. The Line Stretcher is controlled with an ADAM, which is controlled by my Python software servo algorithm. The signal is then received and compared to the reference signal for magnitude and phase, which I use as feedback into my algorithm. 

<img width="507" alt="Screen Shot 2022-12-25 at 2 04 13 PM" src="https://user-images.githubusercontent.com/110696642/209485167-a9c4fc9c-3c5b-47e2-84aa-e486a7059959.png">

Attached is the fiber optic Line Stretcher manual for the specific Line Stretcher Model we used. 

In addition, here is a link for some good information on how a PID controller works: https://pidexplained.com/pid-controller-explained/

