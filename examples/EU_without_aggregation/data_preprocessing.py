from os.path import join
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# paths
cwd = os.getcwd()
data_path = 'c:\\Users\\r.beer\\code\\git_repos\\FINE\\examples\\EU_without_aggregation' + '\\InputData\\SpatialData\\'

path_e_highway_sev2 = join(data_path, 'ShapeFiles\\e-highway_sev2.shp')
path_e_highway_sev_full = join(data_path, 'ShapeFiles\\e-highway_sev-full.shp')


# read & visualize shapefiles
e_highway_sev2 = gpd.read_file(path_e_highway_sev2)
path_e_highway_sev_full = gpd.read_file(path_e_highway_sev_full)

# e_highway_sev2.plot()
# plt.title('sev2')
# path_e_highway_sev_full.plot()
# plt.title('sev-full')

# plt.show()

# define aggregation function
def spat_agg_region_connections(path, replace_type=None):
    df = pd.read_excel(path, index_col=0)

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
            if col_nation == row_nation:
                df_2.loc[col_nation[-2:], row_nation[-2:]] = 0

    df_2.fillna(0)
    df_2.to_excel(path[:-5] + '_aggregated' + '.xlsx')
    print('data aggregated for:')
    print(path)

def spat_agg_region_timeseries(path, replace_type=None):
    # derive save paths
    aggregated_path = path[:-5] + '_aggregated.xlsx'
    max_path = path[:-5] + '_aggregated_max.xlsx'

    # read data
    df = pd.read_excel(path, index_col=0)

    # spatial aggregation of time series within nations
    df_2 = pd.DataFrame(0, columns=df.columns.str[-2:].unique(), index=df.index)
    for str_nation in df.columns.str[-2:].unique():
        df_2.loc[:, str_nation] = df.loc[:, df.columns.str[-2:] == str_nation].sum(axis=1)

    df_2.fillna(0, inplace=True)

    df_2.to_excel(aggregated_path)

    # calculation of max values
    df_3 = pd.DataFrame(0, columns=df.columns.str[-2:].unique(), index=df.index)
    for str_nation in df.columns.str[-2:].unique():
        df_3.loc[:, str_nation] = df_2.loc[:, str_nation].max()

    df_3.to_excel(max_path)

    print('data aggregated for:')
    print(path)
    print('and saved in file:')
    print(max_path)
    print()

# spatial aggregation of time series
path_list = ['Wind\\offshoreProd_2015_GW.xlsx', 'Wind\\onshoreProd_2015_GW.xlsx',
             'PV\\PVProd_2015_GW.xlsx', 'PV\\PVProd_withCSPadded_2015.xlsx',
             'HydroPower\\rorProd_2015_GW.xlsx',
             'Demands\\hydrogenDemand_GW.xlsx',
             'Demands\\load_p_set.xlsx', 'Demands\\load_withoutBEV_MW.xlsx'
             ]

# for path in path_list:
    # spat_agg_region_timeseries(data_path + path)

print('spatial aggregation of time series completed')

# calculate operating rates (wind, pv, ror)
path_list = ['Wind\\offshoreProd_2015_GW.xlsx', 'Wind\\onshoreProd_2015_GW.xlsx',
             'PV\\PVProd_2015_GW.xlsx', 'PV\\PVProd_withCSPadded_2015.xlsx',
             'HydroPower\\rorProd_2015_GW.xlsx']

# for path in path_list:
#     path = data_path + path
#     df_aggregated_power = pd.read_excel(path[:-5] + '_aggregated' + '.xlsx', index_col=0)

#     max_path = path[:-5] + '_aggregated_max.xlsx'
#     df_max_capacity = pd.read_excel(max_path, index_col=0)

#     df_operating_rate = df_aggregated_power.div(df_max_capacity)
    
#     df_operating_rate.fillna(0, inplace=True)
#     df_operating_rate.to_excel(path[:-7] + 'operating_rate' + '.xlsx')

#     print('operating rate calculated for:')
#     print(path)

print('operating rates calculated')

# spatial aggregation of networks
path_list_2 = ['ElectricGrid\\cableCapacity_GW.xlsx',
               'ElectricGrid\\cableIncidence.xlsx',
               'Pipelines\\PipelineIncidence.xlsx',
               'ElectricGrid\\cableLength.xlsx',
               'Pipelines\\PipelineDistance_13times.xlsx']

bool_list = [None, 'bool', 'bool', 'mean', 'mean']

for i, path in enumerate(path_list_2):
    print(i)
    spat_agg_region_connections(data_path + path, replace_type=bool_list[i])

print('spatial aggregation of networks completed')

