WALDO
======

Introduction
------------

People with learning disabilities can encounter difficulty in expressing themselves in speech. Makaton is a language programme that uses signs and symbols to enable users of all ages to communicate effectively. WALDO is a machine learning-enabled assisted living device meant for use by Makaton users and their carers in a care home setting. WALDO’s capabilities include:

* Makaton sign language interpretation using machine learning
* Easy-to-use interface, and a cute and endearing package to encourage use by people with learning disabilities and their carers
* Programmable buttons for users to quickly express pre-set phrases or emotions

Intended Use
------------

WALDO is intended for use in a care home setting in the following ways:

Makaton sign interpretation
1. Makaton user (care home patient) signs to WALDO
2. WALDO uses machine learning to interpret sign
3. WALDO vocalises sign for carer to understand what user intends to express
4. Carer reacts accordingly, completing the interaction between the user and carer
This implementation enables the carer to understand the user without having to undergo the time-consuming process of learning Makaton.

Expression of pre-set phrases/emotions
1. User (by him/herself, or via carer) sets common phrases that he/she uses frequently to correspond to physical buttons on WALDO
2. User labels buttons accordingly for ease of use
3. User presses the relevant button, WALDO vocalises pre-set phrase
4. Carer responds accordingly
This implementation enables people with learning disabilities that have difficulty expressing themselves in speech to easily express everyday sentiments.


Device Components
-----------

To achieve the aims outlined above, this group has implemented WALDO using the following components, as will be outlined in this Virtual Design History File.

<table>
  <tr>
    <th>Section</th>
    <th>Subsection</th>
    <th>Description</th>
  </tr>
  <tr>
    <td colspan="2"><span style="font-weight:bold">Overview</span></td>
    <td>Overview of WALDO, contents of Virtual Design History File</td>
  </tr>
  <tr>
    <td rowspan="3"><span style="font-weight:bold">Setup</span></td>
    <td> <a href="https://github.com/patrickjohncyh/ibm-waldo/blob/master/1-Setup/JetsonSetup.md"> Jetson Nano Setup</a></td>
    <td>Setting up Jetson Nano</td>
  </tr>
  <tr>
    <td><a href="https://github.com/patrickjohncyh/ibm-waldo/blob/master/1-Setup/pisetup.md">Pi Setup</a></td>
    <td>Setting up Raspberry Pi</td>
  </tr>
  <tr>
    <td><a href = "https://github.com/patrickjohncyh/ibm-waldo/blob/master/1-Setup/HardwareConnections.md"> Hardware Setup</a></td>
    <td>Diagram of device hardware connections</td>
  </tr>
  <tr>
    <td rowspan="5"><span style="font-weight:bold">Machine Learning</span></td>
    <td><a href="https://github.com/patrickjohncyh/ibm-waldo/tree/master/2-MachineLearning/server-training"> Server Training Code</a></td>
    <td>Code to be run on server for further model training beyond 5 makaton signs</td>
  </tr>
  <tr>
    <td>Jetson Nano Execution Code</td>
    <td>Code to be run on Jetson Nano for running sign recognition</td>
  </tr>
  <tr>
    <td>Model and Weights</td>
    <td>Saved weights of the final trained model</td>
  </tr>
  <tr>
    <td><a href="https://github.com/patrickjohncyh/ibm-waldo/blob/master/2-MachineLearning/ModelHistoryAndEvolution.md"> Model History and Evolution </a></td>
    <td>Model design history and evolution</td>
  </tr>
  <tr>
    <td><a href="https://github.com/patrickjohncyh/ibm-waldo/blob/master/2-MachineLearning/ServerEnvironmentSetup.md"> Server environment setup for further model training</a></td>
    <td>Setting up server environment to train model to recognise more than 5 Makaton signs</td>
  </tr>
  <tr>
    <td rowspan="4"><span style="font-weight:bold">Raspberry Pi</span></td>
    <td><a href="https://github.com/patrickjohncyh/ibm-waldo/tree/master/3-Pi"> Overview of Pi Function</a></td>
    <td>Outline of functions and connections of Pi</td>
  </tr>
  <tr>
    <td>main.py</td>
    <td><a href="https://github.com/patrickjohncyh/ibm-waldo/tree/master/3-Pi/main.py"> Main function controlling operation of Pi</span></td>
  </tr>
  <tr>
    <td>IBM_text_to_speech.py</td>
    <td><a href="https://github.com/patrickjohncyh/ibm-waldo/tree/master/3-Pi/IBM_text_to_speech.py"> Python script to obtain text to speech output from IBM Watson</span></td>
  </tr>
  <tr>
    <td><a href="https://github.com/patrickjohncyh/ibm-waldo/tree/master/3-Pi#overall-pi-function">Logic flow diagram</a></td>
    <td>Logic for Pi function</td>
  </tr>
  <tr>
    <td rowspan="3"><span style="font-weight:bold">Hardware</span></td>
    <td><a href="https://github.com/patrickjohncyh/ibm-waldo/tree/master/4-Hardware/3D%20Printing%20STL%20Files">3D printing files</a></td>
    <td>Contains Standard Tessellation Language (STL) files of the Jetson Nano case, the Pi case, the button support structure and WALDO’s eyepiece</td>
  </tr>
  <tr>
    <td>Power Supply</td>
    <td>Summary of considerations when choosing WALDO’s power supply</td>
  </tr>
  <tr>
    <td>Hardware List</td>
    <td>List of all hardware components used in assembly of WALDO</td>
  </tr>
  <tr>
    <td rowspan="4"><span style="font-weight:bold">Administrative</span></td>
    <td>Record of Meetings</td>
    <td>Meeting minutes and decisions made</td>
  </tr>
  <tr>
    <td>Gantt Chart</td>
    <td>Intended timeline of project (plotted during first meeting at IBM Hursley)</td>
  </tr>
  <tr>
    <td>Bill of Materials</td>
    <td>Record of expenditure and outline of cost of device</td>
  </tr>
  <tr>
    <td>Data Collection</td>
    <td>Outline of procedure, considerations and product of data collection</td>
  </tr>
  <tr>
    <td rowspan="6"><span style="font-weight:bold">Miscellaneous</span></td>
    <td>Ethical Considerations</td>
    <td>Outline of ethical considerations in the design, building and use of WALDO</td>
  </tr>
  <tr>
    <td>Sustainability considerations</td>
    <td>Outline of sustainability considerations in the design, building and use of WALDO</td>
  </tr>
  <tr>
    <td>Blog</td>
    <td>Rationale behind the blog and links to the blog posts</td>
  </tr>
  <tr>
    <td>Future Work</td>
    <td>Discussion of present implementation and possible extensions to the project</td>
  </tr>
  <tr>
    <td>Leaflet</td>
    <td>Informational leaflet on WALDO</td>
  </tr>
  <tr>
    <td>Poster</td>
    <td>Poster for hackbooth and presentation</td>
  </tr>
</table>
