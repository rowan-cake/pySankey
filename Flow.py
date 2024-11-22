import pandas as pd
import re

class Convert:
    def __init__(self,csv):
        self.df = pd.read_csv(csv)
        self.amount = 0
    
    def extractVendor(self,description):
        # Regex to match the vendor name before the town name
        match = re.match(r'^(.*?)(?: [A-Z][A-Z]{2,}|\d{1,2}(?: [A-Z][A-Z]{2})?)$', description)
        if match:
            return match.group(1).strip()
        return description
    
    def processData(self):
        # Convert "Transaction Date" to datetime datatype
        self.df['Transaction date'] = pd.to_datetime(self.df['Transaction date'])
        # Only look at "debits" no payments to the credit card counted in analsysis
        self.df = self.df.query('Transaction != "CREDIT"')
        # Change "Amount" to numeric datatype
        self.df['Amount'] = pd.to_numeric(self.df['Amount'])
        # Make a new column called "Category" that takes the String after "~ Category: ". Then also strip it of Whitespace
        self.df['Category'] = self.df['Memo'].str.split('~ Category: ').str[1]
        self.df['Category'].str.strip()
        # Make all the values in amount positive.
        self.df['Amount'] = self.df['Amount']*-1
        # Total amount spent in a month
        self.amount =  self.df['Amount'].sum()
        # Attempt to Extract the vendor of the purchase using a regex expression.
        self.df['Vendor'] = self.df['Name'].apply(self.extractVendor)
    
    def csvTotxt(self):
        # Handle some non valid input
        if self.df is None:
            print("No valid DataFrame to process.")
            return
        
        output_path = "data.txt"  # Predefined output path
        expenses = "Expenses"
        
        # Initialize an empty dict to store category:sums
        categoryAmounts = {}
        
        #===================================
        # Iterate over the DataFrame rows 
        for _, row in self.df.iterrows():
            category = row["Category"]
            amount = row["Amount"]
            # If the category is already in the dictionary, add the amount to it
            if category in categoryAmounts:
                categoryAmounts[category] += amount
            else:
                # If the category is not yet in the dictionary, initialize it with 0 and then add the amount(do these steps at the same time)
                categoryAmounts[category] = amount
        #================================================

        # Make the txt file
        with open(output_path, "w") as file:
           for category, total in categoryAmounts.items():
                # Ensure the required columns exist in the DataFrame                    
                file.write(f"{expenses}[{total}]{category}\n")
        print(f"Data successfully saved to {output_path}")

    
if __name__ == "__main__":

    csv = input("Enter a path to a csv file from Tangerine:")
    data = Convert(csv)
    data.processData()
    data.csvTotxt()
    data.df.to_csv("data.csv", index=False)  # 'index=False' prevents writing row indices to the CSV
    print("DONE")
    

