####This is the coding file for mapping codes from https://www.mass.gov/info-details/trial-court-codes-numerical-listing with court json files.
####coded in Jupyter Notebook.

#!/usr/bin/env python
# coding: utf-8

# In[54]:


#open court json file
import json
import pandas as pd

with open('superior_courts.json') as f:
  courts = json.load(f)
courts


# In[55]:


#json--dataframe
df_courts=pd.DataFrame(courts)
df_courts


# In[20]:


#get the code list from mass.gov website
#court-codes is scrached from the website
import json

data = []
dict_court={}
i=0
with open('court-codes.json') as f:
    for line in f:
        dict_court[i]=line
        i=i+1


# In[104]:


#code test: get code from court-codes file
l1=dict_court[1][3:-3].split(":")
l2=dict_court[2][3:-3].split(":")
id=l1[1].split(",")[0].replace(' ', '')
id


# In[106]:


#name test: get name from court-codes file
l31=dict_court[31][3:-3].split(":")
x=l31[2].replace('"', '')
x[1:-1]


# In[56]:


# define the function to get code and name and store in dataframe
def getid_name(dict_court):
    l=dict_court[3:-3].split(":")
    id=l[1].split(",")[0].replace(' ', '')
    name=l[2].replace('"', '')[1:-1]
    id_name={"code":id,"name":name}
    return id_name
    
#function test
getid_name(dict_court[174])


# In[57]:


#append all id and name into list and transfer to df
id_name_dict=[]
for i in range(1,175):
        id_name_dict.append(getid_name(dict_court[i]))
df_idname=pd.DataFrame(id_name_dict)
df_idname


# In[110]:


#map court data with associated codes
df_addid=df_courts.merge(df_idname, how='left',left_on='name', right_on='name')
df_addid=df_addid[['fax','code', 'name', 'phone', 'has_po_box', 'location', 'address',
       'description']]
df_addid


# ### Files with specific map processing

# In[112]:


#Juvenile courts
#only manually add suffolk county Juvenile Court to Juvenile courts data (all others could be applied general map above)
df_addid.loc[3,'code']=71


# In[80]:


#Housing_courts 
##Housing courts documents
#Housing courts start at H. Boston (boston housing court) is now Eastern Housing Court
#Springfield is Western Housing Court
#Worcester is now Central Housing Court.
df_addid.loc[4,'code']='H84' # boston housing court
df_addid.loc[5,'code']='H84' # boston housing court
df_addid.loc[18,'code']='H79' # springfiled housing court
df_addid.loc[19,'code']='H79' # springfiled housing court
df_addid.loc[20,'code']='H79' # springfiled housing court
df_addid.loc[21,'code']='H79' # springfiled housing court
df_addid.loc[0,'code']='H85' # worcester housing court
df_addid.loc[1,'code']='H85' # worcester housing court
df_addid.loc[2,'code']='H85' # worcester housing court
df_addid.loc[3,'code']='H85' # worcester housing court
df_addid.loc[8,'code']='H77' # northeast housing court
df_addid.loc[9,'code']='H77' # northeast housing court
df_addid.loc[10,'code']='H77' # northeast housing court
df_addid.loc[11,'code']='H77' # northeast housing court
df_addid.loc[12,'code']='H77' # northeast housing court
df_addid.loc[13,'code']='H77' # northeast housing court
df_addid.loc[14,'code']='H83' # sourtheast housing court
df_addid.loc[15,'code']='H83' # sourtheast housing court
df_addid.loc[16,'code']='H83' # sourtheast housing court
df_addid.loc[17,'code']='H83' # sourtheast housing court
df_addid.loc[6,'code']='H82'#Metro South Housing Court
df_addid.loc[7,'code']='H82'#Metro South Housing Court


# In[96]:


#bmc courts
df_addid=df_courts
df_addid['code']='NaN'
df_addid.loc[0,'code']='8'
df_addid.loc[1,'code']='1'
df_addid.loc[2,'code']='4'
df_addid.loc[3,'code']='7'
df_addid.loc[4,'code']='5'
df_addid.loc[5,'code']='2'
df_addid.loc[6,'code']='6'
df_addid.loc[7,'code']='3'

#adjust column order
df_addid=df_addid[['fax', 'code','name', 'phone', 'has_po_box', 'location', 'address',
       'description']]


# In[41]:


#family courts
#create map_index which is exactly the same terms shown in mass.gov
def f(x,delm=' '):
     return x.split(delm)[0]+' '+x.split(delm)[1]+' '+x.split(delm)[4]

df_courts['map_index'] = df_courts.name.map(lambda x: f(x))

#map with codes
df_addid=df_courts.merge(df_idname, how='left',left_on='map_index', right_on='name')
df_addid=df_addid[['fax','code', 'name_x', 'phone', 'has_po_box', 'location', 'address',
       'description']]
df_addid.columns=['fax','code', 'name', 'phone', 'has_po_box', 'location', 'address',
       'description']
df_addid


# In[61]:


#supreme courts
#create map_index which is exactly the same terms shown in mass.gov
def f(x,delm=' '):
     return x.split(delm)[0]+' '+x.split(delm)[2]+' '+x.split(delm)[3]

df_courts['map_index'] = df_courts.name.map(lambda x: f(x))

#map with codes
df_addid=df_courts.merge(df_idname, how='left',left_on='map_index', right_on='name')
df_addid=df_addid[['fax','code', 'name_x', 'phone', 'has_po_box', 'location', 'address',
       'description']]
df_addid.columns=['fax','code', 'name', 'phone', 'has_po_box', 'location', 'address',
       'description']
df_addid


# ### write into json

# In[63]:


#write into json: dataframe --dict ---json
df_addid_dict=df_addid.to_dict('records')
with open('superior_courts_addcode.json', 'w') as fp:
    json.dump(df_addid_dict, fp)

