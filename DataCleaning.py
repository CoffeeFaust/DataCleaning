import chardet
import pandas as pd

# Replace '' with the path to your csv file
with open('/Users/sophiaavielleg/Documents/Data Analysis November Sprint 1/data cleaning test.csv', 'rb') as f:
    result = chardet.detect(f.read())

encoding = result['encoding']

# Replace '' with the path to your csv file
df = pd.read_csv('/Users/sophiaavielleg/Documents/Data Analysis November Sprint 1/data cleaning test.csv', encoding=encoding)

column_name = ['Question Id', 'Question', 'Answer', 'Is New Question', 'Reference', 'Analysis']  
selected_column = df[column_name]

new_df = pd.DataFrame(selected_column)

#Analysis - Separation of Columns such as Topics and Entities by the ] Delimiter 
split_columns = new_df['Analysis'].str.split(']', expand=True)
split_columns.columns = ['Topics', 'Entities', 'Temporary', 'Garbage']
new_df = pd.concat([new_df, split_columns], axis=1)

split_columns_again = new_df['Temporary'].str.split(':', expand=True)
split_columns_again.columns = ['Buffer1', 'Helpfulness', 'Tool Utilization', 'Concerned Department', 'Buffer2', 'Suggestions for Improvement', 'Actionable Steps if Tool not Available', 'Buffer3', 'Buffer4']
new_df = pd.concat([new_df, split_columns_again], axis=1)

new_df = new_df.drop(columns=['Garbage', 'Temporary', 'Buffer1', 'Buffer2', 'Buffer3', 'Buffer4', 'Analysis'])

#Removal of garbage for the topics column
new_df['Topics'] = new_df['Topics'].str.replace(r'content', '', regex=True)
new_df['Topics'] = new_df['Topics'].str.replace(r'topics', '', regex=True)

columns_to_clean = ['Topics', 'Entities', 'Helpfulness', 'Tool Utilization', 'Concerned Department', 'Suggestions for Improvement', 'Actionable Steps if Tool not Available']
for column in columns_to_clean:
    new_df[column] = new_df[column].str.replace(r':', '', regex=True)
    new_df[column] = new_df[column].str.replace(r'\{', '', regex=True)
    new_df[column] = new_df[column].str.replace(r'\"', '', regex=True)
    new_df[column] = new_df[column].str.replace(r"\\", '', regex=True)
    new_df[column] = new_df[column].str.replace(r"\'", '', regex=True)
    new_df[column] = new_df[column].str.replace(r"\[", '', regex=True)
    new_df[column] = new_df[column].apply(lambda x: x.lstrip(',') if isinstance(x, str) else x)
    new_df[column] = new_df[column].str.lstrip()

#Removal of garbage for the entities column
new_df['Entities'] = new_df['Entities'].str.replace(r'entities', '', regex=True)

#Removal of garbage for the helpfulness column
new_df['Helpfulness'] = new_df['Helpfulness'].str.replace(r'tool_utilization', '', regex=True)
new_df['Helpfulness'] = new_df['Helpfulness'].str.replace(r',', '', regex=True)

#Removal of garbage for the tool column
new_df['Tool Utilization'] = new_df['Tool Utilization'].str.replace(r'concerned_department', '', regex=True)
new_df['Tool Utilization'] = new_df['Tool Utilization'].str.replace(r',', '', regex=True)

#Removal of garbage for the department column
new_df['Concerned Department'] = new_df['Concerned Department'].str.replace(r'suggestions_for_improvement', '', regex=True)
new_df['Concerned Department'] = new_df['Concerned Department'].str.replace(r',', '', regex=True)

#Removal of garbage for the suggestions column
new_df['Suggestions for Improvement'] = new_df['Suggestions for Improvement'].str.replace(r'actionable_steps_if_tool_not_available', '', regex=True)
new_df['Suggestions for Improvement'] = new_df['Suggestions for Improvement'].str.replace(r',', '', regex=True)

new_csv_path = '/Users/sophiaavielleg/Documents/Data Analysis November Sprint 1/Results2.csv'
new_df.to_csv(new_csv_path, index=False)
#Note: In this portion, there is a permission error that happens when trying to edit the existing file. I think this is a trendmicro thing
#so just change this to create a new file instead
