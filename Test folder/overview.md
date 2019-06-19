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

<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;}
.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:black;}
.tg .tg-pq3e{font-style:italic;border-color:inherit;text-align:left}
.tg .tg-xldj{border-color:inherit;text-align:left}
.tg .tg-s268{text-align:left}
.tg .tg-0lax{text-align:left;vertical-align:top}
</style>
<table class="tg">
  <tr>
    <th class="tg-pq3e">Section</th>
    <th class="tg-pq3e">Subsection</th>
    <th class="tg-pq3e">Description</th>
  </tr>
  <tr>
    <td class="tg-xldj" colspan="2"><span style="font-weight:bold">Overview</span></td>
    <td class="tg-xldj">Overview of WALDO, contents of Virtual Design History File</td>
  </tr>
  <tr>
    <td class="tg-xldj" rowspan="3"><span style="font-weight:bold">Setup</span></td>
    <td class="tg-xldj">Pi Setup</td>
    <td class="tg-xldj"></td>
  </tr>
  <tr>
    <td class="tg-xldj">Jetson Nano Setup</td>
    <td class="tg-xldj"></td>
  </tr>
  <tr>
    <td class="tg-xldj">Hardware Setup</td>
    <td class="tg-xldj">Diagram of device hardware connections</td>
  </tr>
  <tr>
    <td class="tg-xldj" rowspan="5"><span style="font-weight:bold">Machine Learning</span></td>
    <td class="tg-xldj">Code</td>
    <td class="tg-xldj"></td>
  </tr>
  <tr>
    <td class="tg-xldj">Model and Weights</td>
    <td class="tg-xldj"></td>
  </tr>
  <tr>
    <td class="tg-xldj">Model History and Evolution</td>
    <td class="tg-xldj"></td>
  </tr>
  <tr>
    <td class="tg-xldj">Input test videos?</td>
    <td class="tg-xldj"></td>
  </tr>
  <tr>
    <td class="tg-xldj">Server environment setup for further model training</td>
    <td class="tg-xldj"></td>
  </tr>
  <tr>
    <td class="tg-xldj" rowspan="4"><span style="font-weight:bold">Pi</span></td>
    <td class="tg-xldj">Overview of Pi Function</td>
    <td class="tg-xldj">Outline of functions and connections of Pi</td>
  </tr>
  <tr>
    <td class="tg-xldj">switchtest.py</td>
    <td class="tg-xldj"><span style="font-weight:bold">(rename?)</span><span style="font-weight:normal"> Main function controlling operation of Pi</span></td>
  </tr>
  <tr>
    <td class="tg-xldj">sound_to_text.py</td>
    <td class="tg-xldj"><span style="font-weight:bold">(rename?)</span><span style="font-weight:normal"> Python script to obtain text to speech output from IBM Watson</span></td>
  </tr>
  <tr>
    <td class="tg-xldj">Logic flow diagram</td>
    <td class="tg-xldj">Logic for Pi function</td>
  </tr>
  <tr>
    <td class="tg-xldj" rowspan="2"><span style="font-weight:bold">Hardware</span></td>
    <td class="tg-xldj">3D printing files</td>
    <td class="tg-xldj">Contains Standard Tessellation Language (STL) files of the Jetson Nano case, the Pi case, the button support structure and WALDO’s eyepiece</td>
  </tr>
  <tr>
    <td class="tg-s268">Power Supply</td>
    <td class="tg-s268">Summary of considerations when choosing WALDO’s power supply</td>
  </tr>
  <tr>
    <td class="tg-s268" rowspan="4"><span style="font-weight:bold">Administrative</span></td>
    <td class="tg-s268">Record of Meetings</td>
    <td class="tg-s268">Meeting minutes and decisions made</td>
  </tr>
  <tr>
    <td class="tg-0lax">Gantt Chart</td>
    <td class="tg-0lax">Intended timeline of project (plotted during first meeting at IBM Hursley)</td>
  </tr>
  <tr>
    <td class="tg-0lax">Bill of Materials</td>
    <td class="tg-0lax">Record of expenditure and outline of cost of device</td>
  </tr>
  <tr>
    <td class="tg-s268">Data Collection</td>
    <td class="tg-s268">Outline of procedure, considerations and product of data collection</td>
  </tr>
  <tr>
    <td class="tg-s268" rowspan="6"><span style="font-weight:bold">Miscellaneous</span></td>
    <td class="tg-s268">Ethical Considerations</td>
    <td class="tg-s268">Outline of ethical considerations in the design, building and use of WALDO</td>
  </tr>
  <tr>
    <td class="tg-0lax">Sustainability considerations</td>
    <td class="tg-0lax">Outline of sustainability considerations in the design, building and use of WALDO</td>
  </tr>
  <tr>
    <td class="tg-0lax">Blog</td>
    <td class="tg-0lax">Rationale behind the blog and links to the blog posts</td>
  </tr>
  <tr>
    <td class="tg-s268">Future Work</td>
    <td class="tg-s268">Discussion of present implementation and possible extensions to the project</td>
  </tr>
  <tr>
    <td class="tg-s268">Leaflet</td>
    <td class="tg-s268">Informational leaflet on WALDO</td>
  </tr>
  <tr>
    <td class="tg-s268">Poster</td>
    <td class="tg-s268">Poster for hackbooth and presentation</td>
  </tr>
</table>
