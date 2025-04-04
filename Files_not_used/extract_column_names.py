
# DO NOT USE THIS, IT MASSACRES THE COMPUTER
# import xml.etree.ElementTree as ET


# # Parse XML file
# tree = ET.parse("datasets/Users.xml")
# root = tree.getroot()

# # Get column names from the first row element
# columns = root[0].attrib.keys() # Extract attribute names
# print(columns)



import pandas as pd

# Read just a subset of the XML file (limiting parsing to first 1000 rows)
users_df = pd.read_xml("datasets/Users.xml", parser="etree")  

# Display only column names
print(users_df.columns)