# Data-Miner-for-crime-rate   

This project involves everything from collection to all the way till the regression analysis and the evaluation of the model that could be created using collected data. Data is collected from wikipedia and is mainly focused around counties their crime rates and their relation with poverty rate.  

Start the project by creating a directory for it, inside it you will create your virtual environment using ` pythom -m venv [name of your environment]`, make sure you have added python to path while installing. You can activate this environment using `<your directory>\[name of environment]\Scripts\activate`. 

Once you are done with environment setup, you can then start installing all required libraries mentioned in requirements.txt file using command `pip install -r requirements.txt`.  

You are now ready to run the program and test it. We have a few options given to run the file as listed below:  
1. <strong>Data scraping:</strong> This is the default mode and does not need additional arguments. Simply type `python data_miner.py` and you will get all the data. You should see something like this on your screen when it starts running:  
  ![image](https://user-images.githubusercontent.com/110823714/211819591-286ca6e9-2ec0-4b66-b971-c2145b3bb9c5.png)
  ![image](https://user-images.githubusercontent.com/110823714/211820296-030751db-452c-49b2-a98c-5843b3777571.png) 
                  <br/><i>Example dataset that was extracted.</i>
2. <strong>Displaying data:</strong> To check the data we downloaded we use the command `python data_miner.py --data_show "path to csv file"`. This will show the dataset's first five rows and statistical summary:
![image](https://user-images.githubusercontent.com/110823714/211823702-09aeb830-8bfa-419f-b83f-95b1cf3c0dd2.png)


3. Analysis: This mode does an extensive analysis on the dataset collected and can be only appied once you are done scraping the data. This process can be started by typing `python data_miner.py --analysis`. This will show data description, relation bewteen all the features with the target, based on the relations it will also give insights, plot out graphs for all the features, develop a predctive model and show the metrics of it, and finally plot a regression line through data points for all features to show if any predictive model could created or not.
 ![image](https://user-images.githubusercontent.com/110823714/211826647-08e5233a-3023-4918-9615-b280147f6336.png)


Hope you enjoy it !!!
