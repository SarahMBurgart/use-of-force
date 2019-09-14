# use-of-force

A predictive model for probabilities of level of force when the Seattle Police respond to a call or onview concern.

Models were made using Python and SQL on AWS servers, based on voluntary reporting data from the Seattle Police department.

The website is currently hosted on an AWS EC2 instance at: [predictingforce.ml](https://predictingforce.ml)

Currently doing: fixing templating of website, adding an email input, adding range of possible predicted probabilities to results display

More: 
Combining data from two Seattle Police Department public datasets on datetime, this ensemble of a logistic regression model and a gradient boosting classification model effectively deals with the 210:1 class imbalance to return predicted probabilities of 0-4 levels of force based on location, datetime, reason for call, gender and race, with an average AUC of .86.
