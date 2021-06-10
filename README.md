# ECE229Group7 Project
This project builds an informative interactive dashboard to predict, analyze and visualize how stressed employees in a company are, by looking at various metrics such as how long employees have been in the company, their work type, working hours, setups, benefits, etc. 


## Table of Contents  
1. [Prerequisite](#prerequisite)
2. [Folder Organization](#folder)
3. [How to Run Code](#run)
4. [About Dataset](#data)
5. [Testing](#test)
6. [Documentation](#doc)



<a  name="prerequisite"/></a>
## Prerequisite

To run any of the module in this codebase, ensure the newest version of [python3](https://www.python.org/downloads/) or the newest version of [Anaconda](https://docs.anaconda.com/anaconda/install/) is installed on the machine. Further, ensure the respective binary is in the list of PATH variables. 

Additonally, ensure the necessary [dataset](https://www.kaggle.com/blurredmachine/are-your-employees-burning-out/download) is downloaded and stored in the **data** directory. Refer to  [Folder Organization](#folder) for details on **data** directory. Note, the **data** directory is NOT part of this repository, it has to manually created. 

<a name="folder"/></a>
## Folder Organization
1. **Model** : contains all **.py** files for data analysis and machine learning models, and **.ipynb** for all visualization.
2. **Dashboard** : contains all files for building dashboard
3. **docs** : using Sphinx to create a documentation static website as an ongoing part of development.
4. **data**: contails all the data used for training and testing of the regerssion model. After unzipping the [dataset](https://www.kaggle.com/blurredmachine/are-your-employees-burning-out/download), there should be three csv files: sample_submission.csv, test.csv, and train.csv. 
5. **environment.yml**: environment and dependency files.
6. **requirements.txt**: dependencies for Python3 environment.

<a name="run"/></a>
## How to Run Code

1. Download or git clone this github repository. 
<pre>
git clone https://github.com/rpatel26/ECE229Group7.git
</pre>

2. Install the necessary dependencies:
#### Using Anaconda
<pre>
conda env create -f environment.yml
</pre>
#### Using Pip
<pre>
pip install -r requirements.txt
</pre>

3. Install the necessary [dataset](https://www.kaggle.com/blurredmachine/are-your-employees-burning-out/download) and place it into the **data** directory. 

4. To run the dashboard, you will need to navigate to ./Dashboard directory and type the following command
<pre>
streamlit run dashboard_setup.py
</pre>

<a name="data"/></a>
## About Dataset
[Link](https://www.kaggle.com/blurredmachine/are-your-employees-burning-out) to the dataset.
We use the "Are your Employees Burning out" dataset found on Kaggle. This dataset contains 3 files, a training file, a testing file, and a sample submission file. The training and test files, it provides a mental fatigue score, which is the main attribute that reflects the stress level of employees. Additionally, the dataset provides if the employee works from home or not, company types, employee designation, and resource allocation, as well as the gender of the employee. We will train our model based on the training data and use our test data to validate our model. The dataset consists of 22750 training and 12250 test instances.

<a name="test"/></a>
## Code Testing
We use pytest to create a test suite (coverage > 80%) for our project codes. To run pytest, you will need to navigate to ./Dashboard or ./Model and type the following command

<pre>
pytest
</pre>


<a name="doc"/></a>
## Documentation
We use Sphinx to create a documentation static website as an ongoing part of development. Open ./docs/_build/html/index.html file in web browser to see the docs.