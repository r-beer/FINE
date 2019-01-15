from os.path import join
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# visualize shapefiles
path_e_highway_sev2 = join('C:\\Users\\r.beer\\code\\FINE\\examples\\EU_without_aggregation\\InputData\\SpatialData\\'
                           'ShapeFiles\\e-highway_sev2.shp')
path_e_highway_sev_full = join('C:\\Users\\r.beer\\code\\FINE\\examples\\EU_without_aggregation\\InputData\\'
                               'SpatialData\\ShapeFiles\\e-highway_sev-full.shp')

e_highway_sev2 = gpd.read_file(path_e_highway_sev2)
path_e_highway_sev_full = gpd.read_file(path_e_highway_sev_full)

e_highway_sev2.plot()
plt.title('sev2')
path_e_highway_sev_full.plot()
plt.title('sev-full')


plt.show()


def aggregateRegions(path, col_and_index=False, replace_type=None):
    df = pd.read_excel(path)

    if col_and_index:
        df_2 = pd.DataFrame(0, columns=df.columns.str[-2:].unique(), index=df.columns.str[-2:].unique())
        for col_nation in df.columns:
            for row_nation in df.columns:
                if replace_type is None:
                    df_2.loc[col_nation[-2:], row_nation[-2:]] += df.loc[col_nation, row_nation].sum().sum()
                elif replace_type == 'bool':
                    if df.loc[col_nation, row_nation].sum().sum() > 0:
                        df_2.loc[col_nation[-2:], row_nation[-2:]] = 1
                elif replace_type == 'mean':
                    df_2.loc[col_nation[-2:], row_nation[-2:]] += df.loc[col_nation, row_nation].mean().mean()

        df_2.to_excel(path[:-5] + '_aggregated' + '.xlsx')

    else:
        df_2 = pd.DataFrame(0, columns=df.columns.str[-2:].unique(), index=np.arange(0, 8760))
        for str_nation in df.columns.str[-2:].unique():
            df_2[str_nation] = df.loc[:, df.columns.str[-2:] == str_nation].sum(axis=1)

        df_2.to_excel(path[:-5] + '_aggregated' + '.xlsx')

        max_path = path[:-5] + '_aggregated_max.xlsx'
        df_2.max().to_excel(max_path)

    print('data aggregated for:')
    print(path)


data_path = 'C:\\Users\\r.beer\\code\\FINE\\examples\\EU_without_aggregation\\InputData\\SpatialData\\'

# time series aggregation
path_list = ['Wind\\offshoreProd_2015_GW.xlsx', 'Wind\\onshoreProd_2015_GW.xlsx',
             'PV\\PVProd_2015_GW.xlsx', 'PV\\PVProd_withCSPadded_2015.xlsx',
             'HydroPower\\rorProd_2015_GW.xlsx',
             'Demands\\hydrogenDemand_GW.xlsx',
             'Demands\\load_p_set.xlsx', 'Demands\\load_withoutBEV_MW.xlsx'
             ]

for path in path_list:
    aggregateRegions(data_path + path)

# calculate operating rates (wind, pv, ror)
path_list = ['Wind\\offshoreProd_2015_GW.xlsx', 'Wind\\onshoreProd_2015_GW.xlsx',
             'PV\\PVProd_2015_GW.xlsx', 'PV\\PVProd_withCSPadded_2015.xlsx',
             'HydroPower\\rorProd_2015_GW.xlsx']

for path in path_list:
    path = data_path + path
    df_aggregated_power = pd.read_excel(path[:-5] + '_aggregated' + '.xlsx')

    max_path = path[:-5] + '_aggregated_max.xlsx'
    df_max_capacity = pd.read_excel(max_path)

    df_operating_rate = pd.DataFrame()
    for nation in df_max_capacity.index:
        df_operating_rate[nation] = df_aggregated_power[nation] / df_max_capacity.loc[nation, 0]
    df_operating_rate.to_excel(path[:-5] + '_operating_rate' + '.xlsx')

# network aggregation
path_list_2 = ['ElectricGrid\\cableCapacity_GW.xlsx',
               'ElectricGrid\\cableIncidence.xlsx',
               'Pipelines\\PipelineIncidence.xlsx',
               'ElectricGrid\\cableLength.xlsx',
               'Pipelines\\PipelineDistance_13times.xlsx']

bool_list = [None, 'bool', 'bool', 'mean', 'mean']

for i, path in enumerate(path_list_2):
    print(i)
    aggregateRegions(data_path + path, col_and_index=True, replace_type=bool_list[i])

