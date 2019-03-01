import pandas as pd
import os


class Aggregation:

    def __init__(self):
        # reads shapefile and data
        pass

    def aggregate_regions(self):
        # aggregates data with different methods
        pass

    def derive_shapefiles(self):
        # derive buses, transmission etc. from input shapefile
        pass


def getData():
    cwd = os.getcwd()
    inputDataPath = os.path.join(cwd, "InputData")
    data = {}

    # Onshore data
    on_path = 'onshoreProd_2015_operating_rate.xlsx'  # 'maxOperationRateOnshore_el.xlsx'
    on_max_path = 'onshoreProd_2015_GW_aggregated_max.xlsx'  # 'maxCapacityOnshore_GW_el.xlsx'

    capacityMax = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'Wind', on_max_path),
                                index_col=0, squeeze=True)
    operationRateMax = pd.read_excel(os.path.join(inputDataPath,
                                                  'SpatialData', 'Wind', on_path))
    data.update({'Wind (onshore), capacityMax': capacityMax})
    data.update({'Wind (onshore), operationRateMax': operationRateMax})

    # Offshore data
    off_path = 'offshoreProd_2015_operating_rate.xlsx'  # 'maxOperationRateOffshore_el.xlsx'
    off_max_path = 'offshoreProd_2015_GW_aggregated_max.xlsx'  # 'maxCapacityOffshore_GW_el.xlsx'

    capacityMax = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'Wind', off_max_path),
                                index_col=0, squeeze=True)
    operationRateMax = pd.read_excel(
        os.path.join(inputDataPath, 'SpatialData', 'Wind', off_path))
    data.update({'Wind (offshore), capacityMax': capacityMax})
    data.update({'Wind (offshore), operationRateMax': operationRateMax})

    # PV data
    pv_path = 'PVProd_2015_operating_rate.xlsx'  # 'maxOperationRatePV_el.xlsx'
    pv_max_path = 'PVProd_2015_GW_aggregated_max.xlsx'  # 'maxCapacityPV_GW_el.xlsx'
    capacityMax = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'PV', pv_max_path),
                                index_col=0, squeeze=True)
    operationRateMax = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'PV', pv_path))

    data.update({'PV, capacityMax': capacityMax})
    data.update({'PV, operationRateMax': operationRateMax})

    # Run of river data
    ror_path = 'rorProd_2015_operating_rate.xlsx'  # 'fixOperationRateROR_GW_el.xlsx'
    ror_max_path = 'rorProd_2015_GW_aggregated_max.xlsx'  # 'fixCapacityROR_GW_el.xlsx'

    operationRateFix = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'HydroPower',
                                                  ror_path))
    capacityFix = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'HydroPower', ror_max_path),
                                index_col=0, squeeze=True)
    #
    data.update({'Existing run-of-river plants, capacityFix': capacityFix})
    data.update({'Existing run-of-river plants, operationRateFix': operationRateFix})

    # # Biogas data
    # operationRateMax = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'Biogas',
    #                                               'biogasPotential_GWh_biogas.xlsx'))
    #
    # data.update({'Biogas, operationRateMax': operationRateMax})

    # Natural gas plant data
    # capacityMax = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'NaturalGasPlants',
    #                                          'existingCombinedCycleGasTurbinePlantsCapacity_GW_el.xlsx'),
    #                             index_col=0, squeeze=True)
    #
    # data.update({'Existing CCGT plants (methane), capacityMax': capacityMax})

    # Hydrogen salt cavern data
    # capacityMax = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'GeologicalStorage',
    #                                          'existingSaltCavernsCapacity_GWh_methane.xlsx'),
    #                             index_col=0, squeeze=True) * 3 / 10
    #
    # data.update({'Salt caverns (hydrogen), capacityMax': capacityMax})

    # Methane salt cavern data
    # capacityMax = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'GeologicalStorage',
    #                                          'existingSaltCavernsCapacity_GWh_methane.xlsx'),
    #                             index_col=0, squeeze=True)
    #
    # data.update({'Salt caverns (methane), capacityMax': capacityMax})

    # Pumped hydro storage data
    # capacityFix = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'HydroPower',
    #                                          'fixCapacityPHS_storage_GWh_energyPHS.xlsx'),
    #                             index_col=0, squeeze=True)
    #
    # data.update({'Pumped hydro storage, capacityFix': capacityFix})

    # AC cables data
    capacityFix = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'ElectricGrid',
                                             'cableCapacity_GW_aggregated.xlsx'),
                                index_col=0, header=0)
    data.update({'AC cables, capacityFix': capacityFix})

    reactances = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'ElectricGrid', 'cableReactance_dummy.xlsx'),
                                index_col=0, header=0)

    data.update({'AC cables, reactances': reactances})

    # DC cables data
    # capacityFix = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'ElectricGrid',
    #                                         'cableCapacity_GW_aggregated.xlsx'),
    #                             index_col=0, header=0)
    # distances = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'ElectricGrid',
    #                                        'cableLength_aggregated.xlsx'),
    #                           index_col=0, header=0)

    # losses = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'ElectricGrid',
    #                                     'DCcableLosses.xlsx'),
    #                        index_col=0, header=0)

    # data.update({'DC cables, capacityFix': capacityFix})
    # data.update({'DC cables, distances': distances})
    # data.update({'DC cables, losses': losses})

    # Pipelines data
    eligibility = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'Pipelines',
                                             'PipelineIncidence_aggregated.xlsx'), index_col=0, header=0)
    distances = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'Pipelines',
                                           'PipelineDistance_13times_aggregated.xlsx'),
                              index_col=0, header=0)

    data.update({'Pipelines, eligibility': eligibility})
    data.update({'Pipelines, distances': distances})

    # Electricity demand data
    operationRateFix = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'Demands',
                                                  'load_p_set_aggregated.xlsx'))

    data.update({'Electricity demand, operationRateFix': operationRateFix})

    # Hydrogen demand data
    operationRateFix = pd.read_excel(os.path.join(inputDataPath, 'SpatialData', 'Demands',
                                                  'hydrogenDemand_GW_aggregated.xlsx'))

    data.update({'Hydrogen demand, operationRateFix': operationRateFix})



    return data
