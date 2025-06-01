# Second Lab Assignment WUM 2025

---

## Dataset

You will work with an artificially generated dataset, consisting of 2000 samples, 400 input variables and two output variables called **class** and **output**.  
- All input variables are standard‐scaled real numbers.  
- The **class** variable is discrete and has two possible values: 0 and 1.  
- The **output** variable is a real number.  

Both output variables have non‐trivial dependency on some of the input variables. Your task is to build ML models predicting the output variables based on the input variables and analyze the dataset, your models, and the nature of the dependencies you uncover.

---

## Desired Output

You are supposed to submit a Jupyter Notebook with the solutions, commentary, and results via Moodle. Please make sure your notebook opens and works in Google Colab; it will not be graded otherwise. Your solutions will be graded by lab assistants of the respective groups.

Your notebook **must include** a function that can process a `validation_data.csv` file (with the same structure as your training data) and compute the following four metrics on those data for both your baseline and best models:

1. Classification accuracy (baseline model)  
2. Classification accuracy (best model)  
3. R² (coefficient of determination) for regression (baseline model)  
4. R² (coefficient of determination) for regression (best model)  

---

## Specific Tasks to Perform

### Task 1. Building Baseline Models (6 points: 3 for regression + 3 for classification)

1. Using the provided dataset, build **baseline models**:  
   - For the **output** variable (regression): a plain linear regression model using *all* input variables as predictors, **without** any pre‐processing (e.g., no dimensionality reduction).  
   - For the **class** variable (classification): a plain logistic regression model using *all* input variables as predictors, **without** any pre‐processing.  

2. Assess the performance of each baseline model on the **training data**.

3. Estimate each model’s ability to generalize beyond the training data by applying one of the methods covered in lectures (e.g., k‐fold cross‐validation, a hold‐out set, etc.).

4. Comment on the results:  
   - How well do these baseline models perform on the training set?  
   - What does your generalization estimate (e.g., cross‐validation score) suggest?  
   - Are there any obvious limitations/shortcomings?

---

### Task 2. More Advanced Classification (12 points: 3 for using a more advanced method, 3 for parameter optimization, 3 for feature selection, 3 for result analysis)

1. Choose one (or more) classification method(s) covered in lectures (e.g., decision trees, random forests, SVMs, k‐NN, etc.) to build an **improved** model that aims to outperform your baseline logistic regression.

2. You may implement more complex strategies such as:  
   - Resampling (e.g., bootstrap, SMOTE if needed)  
   - Cross‐validation for more robust model evaluation  
   - Automated model selection (e.g., `GridSearchCV`, `RandomizedSearchCV`)

3. Pre‐processing and feature engineering:  
   - You may apply dimensionality reduction (e.g., PCA) or other pre‐processing methods.  
   - If you decide to build a model based on a subset of features, perform **feature selection** and provide a **list of the selected features**.

4. Optimize hyperparameters for your chosen method(s).

5. Evaluate the performance of your improved classifier on the training set (and/or via cross‐validation). Compare this performance to the baseline logistic regression.

6. **Commentary** (3 points):  
   - Justify your choice of algorithm(s).  
   - Explain how you selected hyperparameters (e.g., search strategy, parameter grid).  
   - Describe your feature selection process (if used) and list the features you kept.  
   - Report the **relative improvement** in classification accuracy over the baseline model and discuss why you believe your method performed better (or if it did not, analyze why).

---

### Task 3. More Advanced Regression (12 points: 3 for using a more advanced method, 3 for parameter optimization, 3 for feature selection, 3 for result analysis)

1. Choose one regression approach covered in lectures (e.g., ridge regression, lasso, elastic net, support‐vector regression, random forest regression, etc.) to build an **improved** model that aims to outperform your baseline linear regression.

2. You may implement more complex strategies such as:  
   - Resampling or repeated cross‐validation for robust performance estimates  
   - Automated model selection pipelines

3. Pre‐processing and feature engineering:  
   - You may apply dimensionality reduction (e.g., PCA) or other pre‐processing methods.  
   - If you decide to build a model based on a subset of features, perform **feature selection** and provide a **list of the selected features**.

4. Optimize hyperparameters for your chosen regression method (e.g., using grid or randomized searches).

5. Evaluate the performance of your improved regressor on the training set (and/or via cross‐validation). Compare this performance to the baseline linear regression.

6. **Commentary** (3 points):  
   - Justify your choice of regression algorithm.  
   - Explain how you selected hyperparameters (e.g., search strategy, parameter grid).  
   - Describe your feature selection process (if used) and list the features you kept.  
   - Report the **relative improvement** in R² over the baseline model and discuss why you believe your method performed better (or if it did not, analyze why).


