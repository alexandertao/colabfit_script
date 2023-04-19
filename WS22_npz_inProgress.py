from colabfit.tools.database import MongoDatabase, load_data
from colabfit.tools.property_settings import PropertySettings
from colabfit.tools.configuration import AtomicConfiguration
#from cfkit.database import MongoDatabase, load_data
#from cfkit.configuration import AtomicConfiguration

from tqdm import tqdm
import numpy as np
from ase import Atoms

#call database using its name
#drop_database=True means to start with fresh database
client = MongoDatabase('new_data_test_alexander', configuration_type=AtomicConfiguration, nprocs=4, drop_database=True)


# In[ ]:
#solvated_protein-check out README in data's directory
def reader_rmd(p):
    atoms=[]
    a=np.load(p)
    #na=a['N']
    z=a['nuclear_charges']
    e=a['energies']
    r=a['coords']
    f=a['forces']
    #d=a['D']
    #q=a['nuclear_charges']
    for i in tqdm(range(len(r))):
        #n=na[i]
        atom=Atoms(numbers=z,positions=r[i])
        #atom.info['energy']=e[i]
        atom.info['energy']=float(e[i])
        atom.arrays['forces']=f[i]
        #atom.info['dipole_moment']=d[i]
        #atom.info['charge']=float(q[i])
        #print(atom.info['charge'])
        atoms.append(atom)
        #print(type (atom.info['charge']))
    return atoms
    
 #Loads data, specify reader function if not "usual" file format
configurations = load_data(
    file_path='/large_data/new_raw_datasets/rmd17/rmd17/npz_data/',
    file_format='folder',
    name_field=None,
    elements=['C','N','O','H'],
    default_name='malonaldehyde',
    reader=reader_rmd,
    glob_string='rmd17_malonaldehyde.npz',
    verbose=True,
    generator=False
)


configurations += load_data(
    file_path='/large_data/new_raw_datasets/rmd17/rmd17/npz_data/',
    file_format='folder',
    name_field=None,
    elements=['C','N','O','H'],
    default_name='paracetamol',
    reader=reader_rmd,
    glob_string='rmd17_paracetamol.npz',
    verbose=True,
    generator=False
)


configurations += load_data(
    file_path='/large_data/new_raw_datasets/rmd17/rmd17/npz_data/',
    file_format='folder',
    name_field=None,
    elements=['C','O','H'],
    default_name='salicylic',
    reader=reader_rmd,
    glob_string='rmd17_salicylic.npz',
    verbose=True,
    generator=False
)



client.insert_property_definition('/home/ubuntu/notebooks/potential-energy.json')
client.insert_property_definition('/home/ubuntu/notebooks/atomic-forces.json')
#client.insert_property_definition('/home/ubuntu/notebooks/cauchy-stress.json')


# In[ ]:


property_map = {

    'potential-energy': [{
        'energy':   {'field': 'energy',  'units': 'kcal/mol'},
        'per-atom': {'field': 'per-atom', 'units': None},
# For metadata want: software, method (DFT-XC Functional), basis information, more generic parameters
        '_metadata': {
            'software': {'value':'ORCA 4.0.1'},
            'method':{'value':'PBE/def2-SVP'},
        }
    }],

    'atomic-forces': [{
        'forces':   {'field': 'forces',  'units': 'kcal/mol*Ang'},
        '_metadata': {
            'software': {'value':'ORCA 4.0.1'},
            'method':{'value':'PBE/def2-SVP'},

        }

    }],

#    'cauchy-stress': [{
#    'stress':   {'field': 'virial',  'units': 'GPa'},

#                '_metadata': {
#            'software': {'value':'VASP'},
#        }

#    }],

    }

# In[ ]:


def tform(c):
    c.info['per-atom'] = False


# In[ ]:


ids = list(client.insert_data(
    configurations,
    property_map=property_map,
    #generator=False,
    transform=tform,
    verbose=True
))

#all_co_ids, all_pr_ids = list(zip(*ids))
all_cos, all_dos = list(zip(*ids))

cs_info = [

    {"name":"malonaldehyde",
    "description": "Configurations with malonaldehyde structure)"},

    {"name": "paracetamol",
    "description": "Configurations with paracetamol structure"},

    {"name": "salicylic",
    "description": "Configurations with salicylic structure"},

    {"name": "uracil",
    "description": "Configurations with uracil structure"},

    {"name": "aspirin",
    "description": "Configurations with aspirin structure"},

    {"name":"benzene",
    "description": "Configurations with benzene structure"},

    {"name": "toluene",
    "description": "Configurations with toluene structure"},

    {"name": "azobenzene",
    "description": "Configurations with azobenzene structure"},

    {"name": "ethanol",
    "description": "Configurations with ethanol structure"},

    {"name": "naphthalene",
    "description": "Configurations with naphthalene structure"},
]

cs_ids = []


for i in cs_info:
    cs_id = client.query_and_insert_configuration_set(
        co_hashes=all_cos,
        query={'names':{'$regex':i['name']+'_*'}},
        name=i['name'],
        description=i['description']
    )

    cs_ids.append(cs_id)



# In[ ]:


ds_id = client.insert_dataset(
    #cs_ids=cs_ids,
    do_hashes=all_dos,
    name='RMD17',
    authors=['Anders S. Christensen', 'O. Anatole von Lilienfeld'],
    links=[
        'https://iopscience.iop.org/article/10.1088/2632-2153/abba6f',
        'https://figshare.com/articles/dataset/Revised_MD17_dataset_rMD17_/12672038/2',
    ],
    description =  'For each of the 10 molecules in the MD17 dataset (aspirin, benzene, ethanol, '\
    'salicylic acid, malonaldehyde, toluene, naphthalene, uracil, paracetamol, and '\
    'azobenzene), 100,000 structures were randomly selected from the available MD '\
    'trajectory data. For each of these structures, a single-point force andenergy '\
    'evaluation was carried out at the DFT level. All calculations were performed in '\
    'ORCA 4.0.1, using the PBE functional and the def2-SVP basis set with the '\
    'resolution-of-identity (RI) approximation for the Coulomb integrals.',
    resync=True,
    verbose=True,

)
