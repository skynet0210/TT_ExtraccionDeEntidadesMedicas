import json
import xml.etree.ElementTree as ET

import re

from pprint import pprint

import pandas as pd

import os

import yaml as yaml
list_docs=os.listdir()

print(list_docs)
documento=list_docs[6]

root = ET.parse(documento).getroot()
print(root)
#print(type(root))
#print(len(root))

cadena1 = "Mention"
data={}
data2={}

for i in root:
    if i.tag.find(cadena1) != -1:
        #print(i.tag,":", i.attrib)
        data2[i] = i.attrib
    else:
        if i.tag == '{http:///org/apache/ctakes/typesystem/type/refsem.ecore}UmlsConcept':
            #print(i.tag, ":", i.attrib)
            data[i] = i.attrib

#print("---Diccionario")
#pprint(data)

print("------DATA 1------")
#print(yaml.dump(data, sort_keys=True, default_flow_style=False))


#print (data["0x00000241A01DDCC0"][0])

df = pd.DataFrame([key for key in data.keys()], columns=['key'])
df['Id'] = [value['{http://www.omg.org/XMI}id'] for value in data.values()]
df['codingScheme'] = [value['codingScheme'] for value in data.values()]
df['code'] = [value['code'] for value in data.values()]
df['cui'] = [value['cui'] for value in data.values()]
df['tui'] = [value['tui'] for value in data.values()]
df['preferredText'] = [value['preferredText'] for value in data.values()]
del(df['key'])
#print(df)
#df.to_csv("data2.csv", index = False)


print("------DATA 2------")

df2 = pd.DataFrame([key for key in data2.keys()], columns=['key'])
df2['Id'] = [value['ontologyConceptArr'] for value in data2.values()]
df2['begin'] = [value['begin'] for value in data2.values()]
df2['end'] = [value['end'] for value in data2.values()]
del(df2['key'])
#print(df2)
#print(data2)

print("--------antes UNION---------")
#print(df)


print("------DATA 4 UNION------")
for ind1 in df.index:
    df.loc[ind1, 'Identificador'] = ', '.join(list(df2[df2['Id'].str.contains(df['Id'][ind1])]['Id']))
    df.loc[ind1, 'begin'] = ', '.join(list(df2[df2['Id'].str.contains(df['Id'][ind1])]['begin']))
    df.loc[ind1, 'end'] = ', '.join(list(df2[df2['Id'].str.contains(df['Id'][ind1])]['end']))

print(df)

def juntar_entidades(df):
  t1 = ", ".join(f"{value:s}" for value in set(df.codingScheme.dropna()))
  t2 = ", ".join(f"{value:s}" for value in set(df.preferredText.dropna()))
  t3 = ", ".join(f"{value:s}" for value in set(df.tui.dropna()))
  return pd.DataFrame({"tui": [t3], "Entidad": [t2], "Vocabulario": [t1]})

FinalData = df.groupby(["begin", "cui"]).apply(juntar_entidades).droplevel(-1).reset_index()
FinalData.sort_values(by=['begin'], inplace=True, kind="quicksort")
print("-----Final Data-------")
print(FinalData)
FinalData.to_csv(f"finalData.csv", index = False)

