import pandas as pd
from rdkit import Chem
from rdkit.Chem.Descriptors import ExactMolWt
import numpy as np
import json 

extra_df = pd.read_csv("extra_data.csv")
extra_df = extra_df[list(extra_df.keys()[1:])]

df_fetched = pd.read_csv("scaped_vp.csv")
df_fetched = df_fetched[["fetched_name","vapour_pressure","url","vapour_pressure2"]]

df_pine = pd.read_csv("src/smiles_pine.csv")[["name","cas","composition"]]

smiles_df = pd.read_csv("src/activity_coeff.csv")[["smiles","basic_smiles","activity_coeff"]]

df = pd.concat([df_pine,df_fetched,extra_df, smiles_df], axis=1)

molar_weight = []
for smiles in df["smiles"]:
    molar_weight.append(ExactMolWt(Chem.MolFromSmiles(smiles)))

df["molar_weight"]=molar_weight

def odt(psat, kow, cw, M, T=298, R=8.314):
    """
    Calculate the odor detection threshold.
    p_sat   [Pa]
    kow     [-]
    cw      [mg/L] or [g/m^3]
    M       [g/mol]
    T       [K]
    R       [J/(mol K)]
    """
    return 10**( 0.97 * np.log10(psat*M/(kow*cw*R*T))+4.2)

# mmHg to Pa
df["psat [Pa]"] = df["vapour_pressure2"]*133.322

# logP to Kow
df["kow [-]"] = 10**df["logP_value"]

df["cw [mg/L]"] = df["water_sol_from_logP"]

df["M [g/mol]"] = df["molar_weight"]

df["y [-]"] = df["activity_coeff"]

df["x [-]"] = df["composition"]

for i,cw in enumerate(df["cw [mg/L]"] ):

    if df["kow [-]"][i]==0:
        print(f"kow {i}")
    if cw==0:
        print(f"cw {i}")

df["ODT [-]"]=odt(df["psat [Pa]"], df["kow [-]"], df["cw [mg/L]"], df["M [g/mol]"], T=298, R=8.314)

def c_gi(x,y,psat,M,R=8.314,T=298):
    """ 
    x       [-]
    y       [-]
    psat    [Pa]
    M       [g/mol]
    R       [J/molK]
    T       [K]

    return OV [g/m^3]
    """
    return (x*y*psat*M)/(R*T)


df["OV [g/m^3]"] = c_gi(df["x [-]"],df["y [-]"],df["psat [Pa]"],df["M [g/mol]"])

top_5 = df.nlargest(5, 'OV [g/m^3]')

savedict= {}
savelst = []
for i, cas in enumerate(df["cas"]):
    vals = []
 
    while True:
        
        prompt = f"{cas:<{13}} {df['name'][i]:<{15}}: "

        user_input = input(prompt).strip()
        if user_input.lower() == "no":
            print("\nStopping data entry.")
            print("-" * 40)
            break
        try:
            # Try to convert the input into a float
            number = float(user_input)
            vals.append(number)

        except ValueError:
            print("Invalid input. Please enter a valid number.")
    savedict[i]=vals
    if len(vals) > 0:
        savelst.append(np.median(np.array(vals)))
    else:
         savelst.append(np.nan)



# Convert and write JSON object to file
with open("opt_teory.json", "w") as outfile: 
    json.dump(savedict, outfile)

# Convert and write JSON object to file
with open("opt_teory_list.json", "w") as outfile: 
    json.dump(savelst, outfile)

print(savedict)
print(savelst)
