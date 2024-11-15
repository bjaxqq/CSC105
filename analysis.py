import re
import pandas as pd

pattern = re.compile(r'^\d+, [\w\s]+, \d+, [\w\s]+, (True|False)$')

def valid_record(line):
    return bool(pattern.match(line))

def read_patient_data(file_name):
    records = []
    invalid = []
    
    try:
        with open(file_name, 'r') as file:
            for line in file:
                line = line.strip()
                if valid_record(line):
                    records.append(line.split(', '))
                else:
                    invalid.append(line)

        df = pd.DataFrame(records, columns=['ID', 'Name', 'Age', 'Condition', 'Insurance'])
        df['ID'] = df['ID'].astype(int)
        df['Age'] = df['Age'].astype(int)
        df['Insurance'] = df['Insurance'].apply(lambda x: x.strip() == 'True')

        return df, invalid

    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
        return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def check_immediate_attention(df):
    conditions_needing_attention = ['critical', 'emergency', 'urgent']
    df_attention = df[df['Condition'].str.lower().isin(conditions_needing_attention)]
    total_count = df_attention.shape[0]
    attention_list = df_attention[['Name', 'Condition']].values.tolist()
    return total_count, attention_list

def search_patient(df, search_term):
    search_term = search_term.lower()
    results = df[(df['ID'].astype(str) == search_term) | (df['Name'].str.lower() == search_term)]
    if not results.empty:
        return results
    else:
        return None

files = [
    'patient_data_1.txt',
    'patient_data_2.txt',
    'patient_data_3.txt'
]

all_records = []
all_invalid = []

for data in files:
    df, invalid = read_patient_data(data)
    
    if df is not None:
        print()
        print(data)
        print("\nValid records:")
        print(df)
        
        if invalid:
            print("\nInvalid records:")
            for record in invalid:
                print(record)
        else:
            print("\nNo invalid records.")
        
        total_count, attention_list = check_immediate_attention(df)
        print(f"\nPatients needing immediate attention: {total_count}")
        
        if attention_list:
            for name, condition in attention_list:
                print(f"{name}, {condition}")
        else:
            print(f"\nNo patients need immediate attention.")
        
        all_records.append(df)
    else:
        print("\nNo valid records found.")

if all_records:
    combined_df = pd.concat(all_records, ignore_index=True)
    
    while True:
        search_term = input("\nSearch (or type 'quit' to exit): ")
        if search_term.lower() == 'quit':
            print("Quitting.")
            break
        
        search_results = search_patient(combined_df, search_term)
        
        if search_results is not None:
            print("\nSearch Results:")
            print(search_results)
        else:
            print("\nNo matching patient found.")
else:
    print("No valid records found across all files.")