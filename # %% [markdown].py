# %% [markdown]
# # Data Processes Assignment 2

# %% [markdown]
# EIT Digital Data Science: \
# Davis Siemens \
# Inés Simón del Collado \
# Xiya Sun

# %%
# libraries
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# %% [markdown]
# 

# %%
# Reading files
hospital1 = pd.read_excel('./hospital1.xlsx', index_col=None)
hospital2 = pd.read_excel('./hospital2.xlsx', index_col=None)



# %%
# Display the first few rows of each dataframe to confirm they were read correctly
hospital1.head()

# %%
hospital2.head()

# %%
hospital1.info()

# %%
# lets see if both dates have the same value for each row
mismatched_rows = hospital1[hospital1['date_of_first_symptoms'] != hospital1['BASVURUTARIHI']]
mismatched_rows #since we have the same values, we can drop one column


# %%
# we drop the column BASVURUTARIHI and we only keep the date of the date_of_symp
hospital1.drop(['BASVURUTARIHI'], axis=1, inplace=True)
hospital1['date_of_first_symptoms'] = hospital1['date_of_first_symptoms'].dt.date
hospital1.head()

# %%
hospital2.info()

# %%
# lets see if both dates have the same value for each row
mismatched_rows = hospital2[hospital2['date_of_first_symptoms'] != hospital2['admission_date']]
mismatched_rows #since we have the same values, we can drop one column


# %%
# we drop the column BASVURUTARIHI and we only keep the date of the date_of_symp
hospital2.drop(['admission_date'], axis=1, inplace=True)
hospital2['date_of_first_symptoms'] = hospital2['date_of_first_symptoms'].dt.date
hospital2.head()

# %%
# we make the names of the columns in the same format
hospital1.columns = hospital1.columns.str.lower().str.replace(' ', '_')
hospital2.columns = hospital2.columns.str.lower().str.replace(' ', '_')

# let's see if both dataframes have the same column names 
columns_hospital1 = set(hospital1.columns)
columns_hospital2 = set(hospital2.columns)
comparison_df = pd.DataFrame({
    'Column': list(columns_hospital1.union(columns_hospital2)),
    'In_Hospital1': [col in columns_hospital1 for col in columns_hospital1.union(columns_hospital2)],
    'In_Hospital2': [col in columns_hospital2 for col in columns_hospital1.union(columns_hospital2)]
})

# let's see which columns are different
comparison_df[comparison_df['In_Hospital1'] != comparison_df['In_Hospital2']]


# %%
# observing these columns, we can notice that gender=sex and country=nationality. 
# we keep the patient_id and admission_id
rename_hospital1 = {'nationality': 'nationality_country',
                    'gender_k=female_e=male': 'gender'}
rename_hospital2 = {'country_of_residence': 'nationality_country',
                    'sex': 'gender'}

hospital1.rename(columns=rename_hospital1, inplace=True)
hospital2.rename(columns=rename_hospital2, inplace=True)

# %%
# before merging, we make sure that all the types from both datasets are the same (it doesn't work well the upcasting that turns everything to object)
dtypes_hospital1 = hospital1.dtypes
dtypes_hospital2 = hospital2.dtypes

# Create a DataFrame to compare
dtype_comparison = pd.DataFrame({
    'Column': sorted(set(hospital1.columns).union(set(hospital2.columns))),
    'Hospital1_Dtype': [dtypes_hospital1[col] if col in hospital1.columns else None for col in sorted(set(hospital1.columns).union(set(hospital2.columns)))],
    'Hospital2_Dtype': [dtypes_hospital2[col] if col in hospital2.columns else None for col in sorted(set(hospital1.columns).union(set(hospital2.columns)))]
})

# Add a column to indicate if the dtypes are the same
dtype_comparison['Same_Dtype'] = dtype_comparison['Hospital1_Dtype'] == dtype_comparison['Hospital2_Dtype']
dtype_comparison


# %%
# for the upcasting when we have int and float we should make it float. But in our situation, the floats does not make sense, e.g age or binary cases. 
# therefore, in variables that we have int means that it is enough, so we make it int 
# the only variable that makes sense to be float is temperature, that is already in both
for column in hospital1.columns.intersection(hospital2.columns):
    if dtypes_hospital1[column] != dtypes_hospital2[column]:
        #hospital1[column] = pd.to_numeric(hospital1[column], downcast='integer', errors='coerce')
        #hospital2[column] = pd.to_numeric(hospital2[column], downcast='integer', errors='coerce')
        hospital1[column] = hospital1[column].astype('Int64')
        hospital2[column] = hospital2[column].astype('Int64')

# %%
hospital2.dtypes

# %%
#make sure if are the same now
dtypes_hospital1 = hospital1.dtypes
dtypes_hospital2 = hospital2.dtypes

dtype_comparison = pd.DataFrame({
    'Column': sorted(set(hospital1.columns).union(set(hospital2.columns))),
    'Hospital1_Dtype': [dtypes_hospital1[col] if col in hospital1.columns else None for col in sorted(set(hospital1.columns).union(set(hospital2.columns)))],
    'Hospital2_Dtype': [dtypes_hospital2[col] if col in hospital2.columns else None for col in sorted(set(hospital1.columns).union(set(hospital2.columns)))]
})

dtype_comparison['Same_Dtype'] = dtype_comparison['Hospital1_Dtype'] == dtype_comparison['Hospital2_Dtype']
dtype_comparison

# %%
# since we do the intersection between doth datasets, the columns that are not in both is going to be excluded directly
common_columns = sorted(set(hospital1.columns).intersection(set(hospital2.columns)))

all_patients = pd.concat([hospital1[common_columns], hospital2[common_columns]], ignore_index=True)
all_patients.drop(['patient_id'], axis=1, inplace=True) #this one is in both 
all_patients.head()

# %%
#check the dtypes
all_patients.info()

# %%
# Save the all_patients DataFrame to a CSV file
all_patients.to_excel('all_patients.xlsx', index=True, index_label='ID')
print("The all_patients dataset has been saved as 'all_patients.csv'.")


