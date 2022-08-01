import xml.etree.ElementTree as ET
import pandas as pd
import os


num = 6
list_docs = os.listdir()
print(list_docs)

cadena1 = "Mention"

for j in range(199):
    documento = list_docs[(j+num)]
    root = ET.parse(documento).getroot()

    data = {}
    data2 = {}
    for i in root:
        if i.tag.find(cadena1) != -1:
            data2[i] = i.attrib
        else:
            if i.tag == '{http:///org/apache/ctakes/typesystem/type/refsem.ecore}UmlsConcept':
                data[i] = i.attrib

    print("----Diccionarios----")
    print(data)
    print(data2)

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

    df2 = pd.DataFrame([key for key in data2.keys()], columns=['key'])
    df2['Id'] = [value['ontologyConceptArr'] for value in data2.values()]
    df2['begin'] = [value['begin'] for value in data2.values()]
    df2['end'] = [value['end'] for value in data2.values()]
    del (df2['key'])
    #print(df2)

    for ind1 in df.index:
        df.loc[ind1, 'Id Palabra'] = ', '.join(list(df2[df2['Id'].str.contains(df['Id'][ind1])]['Id']))
        df.loc[ind1, 'Inicio'] = ', '.join(list(df2[df2['Id'].str.contains(df['Id'][ind1])]['begin']))
        df.loc[ind1, 'Fin'] = ', '.join(list(df2[df2['Id'].str.contains(df['Id'][ind1])]['end']))


    def juntar_entidades(df):
        t1 = ", ".join(f"{value:s}" for value in set(df.codingScheme.dropna()))
        t2 = ", ".join(f"{value:s}" for value in set(df.preferredText.dropna()))
        t3 = ", ".join(f"{value:s}" for value in set(df.tui.dropna()))
        return pd.DataFrame({"tui": [t3], "Entidad": [t2], "Vocabulario": [t1]})


    new = df.groupby(["Inicio", "cui"]).apply(juntar_entidades).droplevel(-1).reset_index()
    new.sort_values(by=['Inicio'], inplace=True, kind="quicksort")

    new.to_csv(f"cleanDataCombinated/clean({list_docs[j+num]}).csv", index=False)



