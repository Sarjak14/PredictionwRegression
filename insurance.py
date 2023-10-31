import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
import tkinter as tk

def smoker(dataframe,cst,smoke):
    correlation = np.corrcoef(dataframe['charges'], dataframe['smoker'])[0, 1]
    regression = LinearRegression().fit(dataframe[['smoker']], dataframe['charges'])
    regression_slope = regression.coef_[0]
    regression_intercept = regression.intercept_
    y_charge = [x*regression_slope+regression_intercept for x in dataframe['smoker']]
    if(smoke==1):
        return (regression_slope+cst)
    return cst
def number_analysis(dataframe,age,bmi,children,smoke,sex,region):
    enc = OneHotEncoder(sparse=False)
    encoded_regions = enc.fit_transform(dataframe[['region']])
    region_columns = enc.get_feature_names_out(['region'])
    encoded_df = pd.DataFrame(encoded_regions, columns=region_columns)
    dataframe = pd.concat([dataframe, encoded_df], axis=1)
    x = dataframe[['age','bmi','children']+list(region_columns)].loc[(dataframe['smoker']==0) & (dataframe['sex']=='female')]
    y = dataframe['charges'].loc[(dataframe['smoker']==0) & (dataframe['sex']=='female')]
    l1 = LinearRegression()
    l1.fit(x,y) 
    c1 = l1.coef_
    i = l1.intercept_
    input_data = {'age': age, 'bmi': bmi, 'children': children}
    for column in region_columns:
        input_data[column] = 0
    input_data['region_'+region] = 1
    cst = sum(c1[i]*input_data[x.columns[i]] for i in range(len(x.columns))) + i
    if sex=='male':
        cst=cst+1500
    return smoker(dataframe,cst,smoke)
def calculate_charge():
    dataframe=pd.read_csv('insurance.csv')
    dataframe['smoker'].replace({'yes':1,'no':0},inplace=True)
    dataframe['smoker'].astype(int,copy=False)
    age = int(age_entry.get())
    bmi = float(bmi_entry.get())
    children = int(children_entry.get())
    smoke = int(smoke_var.get())
    sex = sex_var.get()
    region = region_var.get()
    charge = number_analysis(dataframe, age, bmi, children, smoke, sex, region)
    result_label.config(text=f"Estimated Charge: {charge}")

root = tk.Tk()
age_label = tk.Label(root, text="Age:")
age_label.pack()
age_entry = tk.Entry(root)
age_entry.pack()
bmi_label = tk.Label(root, text="BMI:")
bmi_label.pack()
bmi_entry = tk.Entry(root)
bmi_entry.pack()
children_label = tk.Label(root, text="Children:")
children_label.pack()
children_entry = tk.Entry(root)
children_entry.pack()
smoke_var = tk.IntVar()
smoke_check = tk.Checkbutton(root, text="Smoker", variable=smoke_var)
smoke_check.pack()
sex_var = tk.StringVar()
sex_option = tk.OptionMenu(root, sex_var, "male", "female")
sex_option.pack()
region_var = tk.StringVar()
region_option = tk.OptionMenu(root, region_var, "northeast", "northwest", "southeast", "southwest")
region_option.pack()
calculate_button = tk.Button(root, text="Calculate Charge", command=calculate_charge)
calculate_button.pack()
result_label = tk.Label(root)
result_label.pack()
root.mainloop()
calculate_charge()