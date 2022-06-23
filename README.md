# 2AMD20
Knowledge Engineering Course TU/e Eindhoven

This repository contains the project work related to the Knowledge Engineering course offered at the Technical University of Eindhoven.
The focus of the project work is to answer a set of (sub)-questions provided by a client group.

### Question(s)
In which location (municipality) in the Netherlands are people the healthiest? 
* What attributes can be used as indicators for having a healthy population?
* What is the best location (municipality or smaller) to live healthy in The Netherlands for which demographic group of people (i.e. age: students, elderly or different ethnicity)?
* How do population attributes (such as income, education level, energy consumption, etc.) relate to health within the population of the Netherlands?

In order to answer these questions, a new dataset was created using a selection of datasets gathered from the StatLine CBS.
This final dataset was the result of numerous pre-processing steps and is stored in the /data/ folder of the repository under the "preprocessed_data.csv" file.

This newly created dataset follows a Subject-Predicate-Object triplet structure to collect and stored in a convenient way the data contained in the selected StatLine CBS sources.

The dataset is used to answer the questions presented previously through a ranking function provided in the `Querying.ipynb` notebook.

This README.md was last updated: 23-June-2022
