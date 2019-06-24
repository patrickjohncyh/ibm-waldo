5.4 Data Collection
===============

Go To
------
* [Group Members](#group-members)
* [Data Privacy](#data-privacy)
* [Method of Data Collection](#method-of-data-collection)
* [Ethnic Distribution](#ethnic-distribution)

<Br>

Group Members
--------------

Initially, data collection was conducted internally, with three members of the group acting as signers. The initial dataset, encompassing all 5 actions, has the following characteristics:

 -   3 signers (3 members of group)
 -   20 backgrounds
 -   9 angles (three heights, three directions -- left, straight and right)

This initial dataset consisted of 2700 videos. However, it was quickly discovered that the low amount of diversity in this dataset would be severely insufficient to train a machine learning model robust enough to interpret signs from a range of signers. Furthermore, all three group members were of the same ethnicity (Asian -- Chinese). Hence, volunteers were required as signers for further data collection.

<Br>
 
Data Privacy
-----------

In order to keep the project ‘internal’ for now, the decision was taken to only film volunteers around the Imperial College London campus at South Kensington. As such, only staff and students of Imperial College were filmed as volunteers. Before filming any volunteer, the purpose of the project and the reasons for filming were explained. Filming would then take place only if he or she gave their consent to the video recordings on the basis that the recordings were only to be used for this project and would be deleted at the end of the project.

<Br>

Method of Data Collection
------------------------

It soon became clear that in order to have an accurate and robust neural network model, a significantly larger amount of data had to be collected. In other words, the gathering of data had to be extended beyond the three group members. The dataset collected had to comprise of different people of varying ethnicity, filmed under different lighting conditions and backgrounds.

Volunteers were randomly found and filmed around the Imperial College London campus at South Kensington. Each volunteer would be filmed 5 times, corresponding to the 5 actions. In order not to demand too much of the volunteer, each volunteer was only filmed from a single angle- from a straight direction and a middle height with the volunteer stood approximately 2 metres from the camera. This angle and distance was chosen as the approximate height at which WALDO would eventually be placed at. A total of 162 volunteers were filmed.

<Br>

Ethnic Distribution
-------------------

The dataset has the following ethnic composition(1).

| Ethnicity                  	| Number 	| Percentage 	|
|----------------------------	|--------	|------------	|
| Asian-East/Southeast Asian 	| 67     	| 41.4       	|
| Asian-South Asian          	| 18     	| 11.1       	|
| Black                      	| 7      	| 4.32       	|
| White                      	| 70     	| 43.2       	|

<Br>

![Enthicity and Gender Distributions](https://github.com/patrickjohncyh/ibm-waldo/blob/master/imgs/data_diversity4.png "Ethnicity and Gender Distributions")

> (1) A more detailed ethnic breakdown is not feasible as volunteers were not asked for information on their ethnicity when data was collected.

<Br>

This compares well with Imperial College’s ethnic composition(2), shown below.

| Ethnicity                                          	| Postgraduate (PG)   	| Undergraduate (UG)   	| PG%  	| UG%  	|
|----------------------------------------------------	|------	|------	|------	|------	|
| White                                              	| 2310 	| 1177 	| 43.4 	| 40.1 	|
| Black or Black British – African, Caribbean, Other 	| 168  	| 82   	| 3.2  	| 2.8  	|
| Asian or Asian British – Indian                    	| 293  	| 250  	| 5.5  	| 8.5  	|
| Asian or Asian British – Pakistani                 	| 69   	| 63   	| 1.3  	| 2.1  	|
| Asian or Asian British – Bangladeshi               	| 33   	| 24   	| 0.6  	| 0.8  	|
| Chinese                                            	| 1533 	| 651  	| 28.8 	| 22.2 	|
| Other Asian background                             	| 317  	| 212  	| 6.0  	| 7.2  	|
| Mixed Ethnicities                                  	| 208  	| 132  	| 3.9  	| 1.3  	|
| Arab                                               	| 172  	| 39   	| 3.2  	| 1.3  	|
| Other ethnic background                            	| 79   	| 33   	| 1.5  	| 1.1  	|
| Not known                                          	| 16   	| 201  	| 0.3  	| 6.8  	|
| Information refused                                	| 119  	| 74   	| 2.2  	| 2.5  	|

<Br>

> (2) Acquired from a freedom of information request, accessible online at [https://www.whatdotheyknow.com/request/statistics_on_ethnicity](https://www.whatdotheyknow.com/request/statistics_on_ethnicity)
