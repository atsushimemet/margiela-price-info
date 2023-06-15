#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
from pathlib import Path


# In[2]:


brand = "margiela"
yyyymmdd = "20230614"


# In[3]:


file_list = [f for f in os.listdir(f"./data/output/{brand}") if yyyymmdd in f]


# In[6]:


price_list = []
for file in file_list:
    with open(Path(f"data/output/{brand}") / file, "r") as f:
        price_list.append(int(f.read().split("価格: ")[1].split("\n")[0]))


# In[7]:


round(sum(price_list) / len(price_list))


# In[8]:


min(price_list)


# In[9]:


max(price_list)

