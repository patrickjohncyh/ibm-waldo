# Ethical Considerations

As a device meant for use with vulnerable people and relying on a significant amount of data collection, WALDO raises several ethical concerns that need to be addressed. In this report, this group will examine whether these concerns are founded, and outline what steps have been taken in this project to address them.

  
## User Privacy

In recent years, with advancements in connectivity and sensor technology, smart home devices have become increasingly ubiquitous in developed countries [1][2]. However, data privacy is one key concern for smart home users; concerns include[3]:

  

-   Who has access to smart home data: manufacturers are more trusted than government entities, which are in turn more trusted than ISPs
    
-   What data the smart home device is recording: devices that do not record audio and video are more likely to be trusted
    
-   What privacy protections manufacturers have in place
    

  

While WALDO is not strictly a smart home device, it possesses many characteristics similar to that of a smart home device:

  

-   WALDO includes a camera and environmental sensors which are always on
    
-   WALDO is meant for use in a care home setting, which is similar to a home setting as it is a form of long-term habitation for patients
    
-   WALDO can be connected to the Internet
    

  

As such, the privacy concerns that face smart home technologies would face WALDO too, and have to be addressed. Arguably, these concerns are all the more pressing, since WALDO is meant for use with people with learning disabilities, who are more vulnerable than everyday consumers. For example, they might be less aware of the reality of privacy breaches and hacking, and more willing to use a device that is not safe for use. While it may be argued that the onus is on the care home to ensure their residents’ privacy, and care homes such as Precious Homes have their own privacy policy[4], this group believes that WALDO should be built with its users’ privacy as one of its foremost considerations. For context, Precious Homes is the care home that the group worked with during this project, and provided recommendations on the use of Makaton.

  
The first way in which WALDO addresses privacy concerns is in being an on-edge device, with the on-device Nvidia Jetson Nano having sufficient computational power to perform machine learning computation on its own. This obviates the need to send user data, that is, the video used for Makaton interpretation, to a remote server, where it could be compromised or misused.

  

The second way in which WALDO addresses privacy concerns is in not recording more data than it needs to. Besides the camera, WALDO does not contain a microphone, and cannot record conversations around it. Environmental sensors, should they be implemented, do not provide data that can be linked to specific individuals, and would only be used to detect trends in the user’s environment.

  

Additional steps to address privacy concerns could include a physical shutter over the camera for when WALDO is not in use, and physical airgapping between network-connected devices and recording devices when Internet connectivity is not required. However, Internet connectivity should still be retained, to allow for software updates to be provided to WALDO, for example, to improve the accuracy and robustness of its machine learning model.

  

## Data Privacy

  

In making use of machine learning to perform Makaton interpretation, WALDO requires the collection of a large amount of training data from volunteers. This raises the concern of data privacy of the volunteers, as training data has the potential to be misused. This group has addressed this concern by destroying training data after training has been completed, only providing IBM with the trained model. Further elaboration on this point can be found in the ‘Data Collection’ document under ‘5. Administrative > Data Collection’.

  

## Consequences for Jobs

  

A concern with any technological device meant to perform a role previously carried out by a person is the impact on the jobs and livelihoods of workers in that industry. As a Makaton interpreter and companion, WALDO performs several roles that care home carers currently performs. However, WALDO is meant to augment the capabilities of carers, not replace them. WALDO only performs Makaton interpretation, but is unable to act on the signs it interprets, relying on carers to carry out that role. Hence, WALDO is meant to ease interaction between carer and resident, not replace the carer. As WALDO is only a medium for expression, it is unable to act as a true companion that responds, thus also does not supplant the carer in this aspect.

  

In conclusion, WALDO has been designed and built specifically with the abovementioned ethical considerations in mind, with specific measures to safeguard privacy and work within existing care home structures. In addition, these considerations should remain a priority when planning further extensions to WALDO.

## Bibliography

  

[1] Snow, A. Americans Ready for the Smart Home. [Online] Coldwell Banker Blue Matter. Available from: https://www.coldwellbanker.com/blog/americans-ready-for-the-smart-home/?utm_source=pr&utm_medium=referral&utm_campaign=pr-blog-smarthomes&utm_content=CNET [Accessed: 18 June 2019].

  

[2] Alton, L. Are Customers Finally Ready to Adopt Smart Home Technology? Huffington Post. [Online] 2017; Available from: https://www.huffpost.com/entry/are-customers-finally-ready-to-adopt-smart-home-technology_b_59e6e735e4b0e60c4aa3666f [Accessed: 18 June 2019].

  

[3] Zheng, S., Apthorpe, N., Chetty, M. & Feamster, N. (2018) User Perceptions of Smart Home IoT Privacy. Proceedings of the ACM on Human-Computer Interaction - CSCW. [Online] 2 (CSCW). Available from: doi:10.1145/3274469 [Accessed: 18 June 2019].

  

[4] Gennings, W. (n.d.) Privacy Notice. [Online]. Precious Homes. Available from: http://www.precious-homes.co.uk/privacy-policy/ [Accessed: 18 June 2019].