from colabfit.tools.database import MongoDatabase, load_data
from colabfit.tools.property_settings import PropertySettings
from colabfit.tools.configuration import AtomicConfiguration

# call database using its name
# drop_database=True means to start with fresh database
client = MongoDatabase('new_data_test_alexander', configuration_type=AtomicConfiguration, nprocs=4, drop_database=True)


# Loads data, specify reader function if not "usual" file format


configurations = load_data(
    file_path='/large_data/new_raw_datasets_2.0/flexible_molecules/Datasets/Datasets/Azobenzene_inversion_reformat.xyz',
    file_format='xyz',
    name_field=None,
    elements=['C', 'N', 'H', 'O'],
    default_name='Azobenzene_inversion',
    verbose=True,
    generator=False
)

configurations = load_data(
    file_path='/large_data/new_raw_datasets_2.0/flexible_molecules/Datasets/Datasets/Azobenzene_rotation_and_inversion_reformat.xyz',
    file_format='xyz',
    name_field=None,
    elements=['C', 'N', 'H', 'O'],
    default_name='Azobenzene_rotation_and_inversion',
    verbose=True,
    generator=False
)

configurations = load_data(
    file_path='/large_data/new_raw_datasets_2.0/flexible_molecules/Datasets/Datasets/Azobenzene_rotation_reformat.xyz',
    file_format='xyz',
    name_field=None,
    elements=['C', 'N', 'H', 'O'],
    default_name='Azobenzene_rotation',
    verbose=True,
    generator=False
)

configurations = load_data(
    file_path='/large_data/new_raw_datasets_2.0/flexible_molecules/Datasets/Datasets/Glycine_reformat.xyz',
    file_format='xyz',
    name_field=None,
    elements=['C', 'N', 'H', 'O'],
    default_name='Glycine',
    verbose=True,
    generator=False
)


'''


cs_list = set()
for c in configurations:
    cs_list.add(*c.info['_name'])
print(cs_list)
'''
# In[ ]:

client.insert_property_definition('/home/ubuntu/notebooks/potential-energy.json')
# client.insert_property_definition('/home/ubuntu/notebooks/atomic-forces.json')
#client.insert_property_definition('/home/ubuntu/notebooks/cauchy-stress.json')
'''
free_property_definition = {
    'property-id': 'free-energy',
    'property-name': 'free-energy',
    'property-title': 'molecular reference energy',
    'property-description': 'enthalpy of formation',
    'energy': {'type': 'float', 'has-unit': True, 'extent': [], 'required': True,
               'description': 'enthalpy of formation'}}

client.insert_property_definition(free_property_definition)
'''

property_map = {
        'potential-energy': [{
            'energy':   {'field': 'energy',  'units': 'Kcal/Mol'},
            'per-atom': {'field': 'per-atom', 'units': None},
     #For metadata want: software, method (DFT-XC Functional), basis information, more generic parameters
            '_metadata': {
                'software': {'value':'FHI-aims'},
                'method':{'value':'DFT-PBE'},
                #'ecut':{'value':'700 eV for GPAW, 900 eV for VASP'},
            }
        }],

#    'atomic-forces': [{
#        'forces':   {'field': 'forces',  'units': 'eV/Ang'},
#            '_metadata': {
#            'software': {'value':'VASP'},
#        }
#    }],

#     'cauchy-stress': [{
#         'stress':   {'field': 'virials',  'units': 'GPa'}, #need to check unit for stress
#
#         '_metadata': {
#             'software': {'value':'GPAW and VASP'},
#             'method':{'value':'DFT'},
#             'ecut':{'value':'700 eV for GPAW, 900 eV for VASP'},
#         }
#
#}],

}

def tform(c):
    c.info['per-atom'] = False

ids = list(client.insert_data(
    configurations,
    property_map=property_map,
    generator=False,
    transform=tform,
    verbose=True
))

all_co_ids, all_pr_ids = list(zip(*ids))
'''
#matches to data CO "name" field
cs_regexes = {
    '.*':
        'Silica datasets. For DFT computations, the GPAW (in combination with ASE) and VASP codes employing '\
        'the projector augmented-wave method were used. Early versions of the GAP were based '\
        'on reference data computed using the PBEsol functional. For GPAW, an energy cut-off '\
        'of 700 eV and a k-spacing of 0.279 Å−1 were used, for VASP, a higher energy cut-off '\
        'of 900 eV and a denser k-spacing of 0.23 Å−1 were used.',
        }
cs_names=['all']
for i in cs_list:
    cs_regexes[i]='Configurations with the %s structure.' %i
    cs_names.append(i)
#print (cs_regexes)


cs_ids = []


for i, (regex, desc) in enumerate(cs_regexes.items()):
    co_ids = client.get_data(
        'configurations',
        fields='hash',
        query={'hash': {'$in': all_co_ids}, 'names': {'$regex': regex}},
        ravel=True
    ).tolist()

    print(f'Configuration set {i}', f'({regex}):'.rjust(22), f'{len(co_ids)}'.rjust(7))

    cs_id = client.insert_configuration_set(co_ids, description=desc,name=cs_names[i])

    cs_ids.append(cs_id)
'''

ds_id = client.insert_dataset(
    #cs_ids=cs_ids,
    do_hashes=all_pr_ids,
    name='flexible_molecules_JCP2021',
    authors=[
        'Valentin Vassilev-Galindo', 'Gregory Fonseca', 'Igor Poltavsky', 'Alexandre Tkatchenko'
    ],
    links=[
        'https://pubs.aip.org/aip/jcp/article/154/9/094119/313847/Challenges-for-machine-learning-force-fields-in',
    ],
    description='All calculations were performed in FHI-aims software using the Perdew–Burke–Ernzerhof (PBE) '\
                'exchange–correlation functional with tight settings and the Tkatchenko–Scheffler (TS) method to '\
                'account for van der Waals (vdW) interactions.',
    resync=True,
    verbose=True,
)
