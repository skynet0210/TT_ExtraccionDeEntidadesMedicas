import xml.etree.ElementTree as ET
import pandas as pd
import os


num = 6
list_docs = os.listdir()
print(list_docs)

for j in range(200):
    documento = list_docs[(j+num)]
    root = ET.parse(documento).getroot()
    print(root)
    print(type(root))
    #print(len(root))

    data = {}
    for i in root:
        if i.tag == '{http:///org/apache/ctakes/typesystem/type/refsem.ecore}UmlsConcept':
            print(i.tag, ":", i.attrib)
            data[i] = i.attrib

    print(f"------DATA Documento {j+1} ------")
    df = pd.DataFrame([key for key in data.keys()], columns=['key'])
    df['Id'] = [value['{http://www.omg.org/XMI}id'] for value in data.values()]
    df['codingScheme'] = [value['codingScheme'] for value in data.values()]
    df['code'] = [value['code'] for value in data.values()]
    df['cui'] = [value['cui'] for value in data.values()]
    df['tui'] = [value['tui'] for value in data.values()]
    df['preferredText'] = [value['preferredText'] for value in data.values()]
    del (df['key'])
    #print(df)
    #df.to_csv(f"cleanData/data({list_docs[j+num]}).csv", index=False)



