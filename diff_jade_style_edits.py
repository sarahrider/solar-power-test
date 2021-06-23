#!/usr/bin/env python
# coding: utf-8

# In[1]:


from difflib import SequenceMatcher
from difflib import Differ
import pandas as pd
from IPython.display import Markdown
import re


# # Read Excel cheet

# In[2]:


df = pd.read_excel("/Users/sarah/Downloads/TEST Jade Text Punctuation.xlsx").fillna("")


# # New code to make the markdown

# In[3]:


markdown_for_all_rows = []

row_counter = 0

for row in df.iterrows():
    
    row_counter += 1
    
    text1 = row[1][1]
    text2 = row[1][2]
    
    if text1 > '' and text2 > '':
    
        markdown_for_row = []
            
        #print()
        #print('text1', text1)
        #print()
        #print('text1', text2)
   
        comparison = SequenceMatcher(None, text1, text2)
        opcodes = comparison.get_opcodes()

        merged_c = []
        
        for s in opcodes:
            if s[0] == 'equal':
                for a in range(s[1], s[2]):
                    merged_c.append([text1[a], ''])
            if s[0] == 'insert':
                for a in range(s[3], s[4]):
                    merged_c.append([text2[a], 'insert'])
            if s[0] == 'delete':
                for a in range(s[1], s[2]):
                    merged_c.append([text1[a], 'delete'])
            if s[0] == 'replace':
                for a in range(s[1], s[2]):
                    merged_c.append([text1[a], 'delete'])
                for a in range(s[3], s[4]):
                    merged_c.append([text2[a], 'insert'])
        
        #print()
        #print('merged_c', merged_c)
                    
        parent_open = False
        for a in range(0, len(merged_c)):
            if merged_c[a][0] == '(':
                parent_open = True
                merged_c[a][1] = 'parenthesis'
            elif merged_c[a][0] == ')':
                parent_open = False
                merged_c[a][1] = 'parenthesis'
            elif parent_open == True:
                merged_c[a][1] = 'parenthesis'
                
        for a in range(0, len(merged_c)):
            if merged_c[a][0] in [' ', '.', ','] and merged_c[a][1] != 'parenthesis':
                merged_c[a][1] = ''
        
        #print()
        #print('merged_c', merged_c)
        
        last_class = None
        
        for c in merged_c:
            
            if c[1] != last_class:
            
                if last_class != None and last_class != '':
                    markdown_for_row.append('</span>')
                
                if c[1].strip() > '':
                    markdown_for_row.append('<span class="' + c[1] + '">')
            
            markdown_for_row.append(c[0])
            last_class = c[1]
            
        if last_class != None and last_class > '':
            markdown_for_row.append('</span>')
            
        #print()
        #print('markdown_for_row', markdown_for_row)
        
        markdown_for_all_rows.append(''.join(markdown_for_row))
            
        print()
        print('markdown_for_all_rows[-1]', markdown_for_all_rows[-1])


# In[4]:


styleblock = """<style>                           
    span.delete {color: #32a852; 
                 background-color: lavender;
                 font-size: 150%; 
                 margin: 0 3px; 
                 border: 1px solid #808080; 
                 line-height: 1.5;
                 padding: 2px;}
    span.insert {color: #e02427;
                 background-color: lavender;
                 font-size: 150%; 
                 margin: 0 3px; 
                 border: 1px solid #808080; 
                 line-height: 1.5;
                 padding: 2px;}
    span.parenthesis {color: #324ea8;
                    font-size: 100%;
                    margin: 0 3px;}
    </style>"""

Markdown(styleblock + '\n\n'.join(markdown_for_all_rows))


# In[ ]:





# In[ ]:




