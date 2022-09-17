from dash import html
import re
import pandas as pd

#LOCAL MODULES
from processing.read_from_metadata_table import read_from_metadata_table
from processing.collect_stats_samples import collect_stats_samples
from processing.feature_dicts_creation import feature_dicts_creation



############
#INPUT TESTING
############

def assert_peaktable_format(peaktable, filename):
    """Test peaktable columns for correct headers (i.e. format)
    
    Parameters
    ----------
    peaktable : `pandas.core.frame.DataFrame`
    filename : `str`
    """
    
    if peaktable.filter(regex="^id$").columns.empty:
        return return_error_peaktable_div(filename, 'id')
    elif peaktable.filter(regex="^mz$").columns.empty:
        return return_error_peaktable_div(filename, 'mz')
    elif peaktable.filter(regex="^rt$").columns.empty:
        return return_error_peaktable_div(filename, 'rt')
    elif peaktable.filter(regex="^datafile:").columns.empty:
        return return_error_peaktable_div(filename, 'datafile: ...')
    elif peaktable.filter(regex=":intensity_range:max$").columns.empty:
        return return_error_peaktable_div(filename, '... :intensity_range:max')
    elif peaktable.filter(regex=":feature_state$").columns.empty:
        return return_error_peaktable_div(filename, '... :feature_state')
    elif peaktable.filter(regex=":fwhm$").columns.empty:
        return return_error_peaktable_div(filename, '... :fwhm')
    elif peaktable.filter(regex=":rt$").columns.empty:
        return return_error_peaktable_div(filename, '... :rt')
    elif peaktable.filter(regex=":rt_range:min$").columns.empty:
        return return_error_peaktable_div(filename, '... :rt_range:min')
    elif peaktable.filter(regex=":rt_range:max$").columns.empty:
        return return_error_peaktable_div(filename, '... :rt_range:min')
    else:
        return None


def assert_bioactivity_format(bioactiv_table, filename):
    """Test bioact table for col headers, empty values and trailing spaces
        
    Parameters
    ----------
    bioactiv_table : `pandas.core.frame.DataFrame`
    filename : `str`
    """
    if len(bioactiv_table.columns) > 2:
        return html.Div(
        f'''❌ Error: More than 2 columns in file "{filename}" detected.
        Is there maybe any hidden whitespace?'''
            )
    elif bioactiv_table.filter(regex="^sample_name$").columns.empty:
        return html.Div(
        f'❌ Error: "{filename}" is missing a column titled "sample_name".'
            )
    elif bioactiv_table.filter(regex="^bioactivity$").columns.empty:
        return html.Div(
        f'❌ Error: "{filename}" is missing a column titled "bioactivity".'
            )
    elif bioactiv_table.loc[:,'sample_name'].isnull().any():
        return html.Div(
        f'''
        ❌ Error: Empty field(s) in file 
        "{filename}" detected. This is not allowed.
        Please correct and try again.'''
            )
    elif bioactiv_table.loc[:,'bioactivity'].isnull().any():
        return html.Div(
        f'''
        ❌ Error: Empty field in column "bioactivity" of file 
        "{filename}" detected. This is not allowed.
        Please correct and try again.'''
            )
    elif bioactiv_table.loc[:,'sample_name'].astype(str).str.contains('^\s+$').any():
        return html.Div(
        f'''
        ❌ Error: Field containing only whitespace in column 
        'sample_name' in file {filename} detected. This is forbidden.'''
            )
    elif bioactiv_table.loc[:,'bioactivity'].dtypes == "object": 
        return html.Div(
        f'''
        ❌ Error: Field containing text values (strings) in column 
        'bioactivity' in file {filename} detected.
        This might be also whitespace at the bottom of the column.
        This is forbidden.'''
            )
    else:
        return None


def assert_metadata_format(metadata, filename):
    """Test metadata table for col headers, false values and trailing spaces
    
    Parameters
    ----------
    metadata : `pandas.core.frame.DataFrame`
    filename : `str`
    """
    if len(metadata.columns) > 2:
        return html.Div(
        f'''❌ Error: More than 2 columns in file "{filename}" detected.
        Is there maybe any hidden whitespace?'''
            )
    elif metadata.filter(regex="^sample_name$").columns.empty:
        return html.Div(
        f'❌ Error: "{filename}" is missing a column titled "sample_name".'
            )
    elif metadata.filter(regex="^attribute$").columns.empty:
        return html.Div(
        f'❌ Error: "{filename}" is missing a column titled "attribute".'
            )
    elif metadata.loc[:,'sample_name'].isnull().any():
        return html.Div(
        f'''
        ❌ Error: Empty field(s) in column 'sample_name' of file 
        "{filename}" detected. This is not allowed.
        Please correct and try again.'''
            )
    elif metadata.loc[:,'attribute'].str.contains('^GENERAL$').any():
        return html.Div(
        f'''
        ❌ Error: Signal word "GENERAL" used in file {filename}.
        This is forbidden.'''
            )
    elif metadata.loc[:,'sample_name'].str.contains('^\s+$').any():
        return html.Div(
        f'''
        ❌ Error: Field containing only whitespace in column 
        'sample_name' in file {filename} detected. This is forbidden.'''
            )
    elif metadata.loc[:,'attribute'].str.contains('^\s+$').any():
        return html.Div(
        f'''
        ❌ Error: Field containing only whitespace in column 
        'attribute' in file {filename} detected. This is forbidden.'''
            )
    elif metadata.loc[:,'sample_name'].duplicated().any():
        return html.Div(
        f'''
        ❌ Error: Duplicate values in column 'sample_name'
        in file {filename} detected. This is forbidden.'''
            )
    else:
        return None


def return_error_peaktable_div(filename, header):
    '''Helper function to report where error lay.'''
    return html.Div(
        f'''
        ❌ Error: "{filename}" is missing column(s) titled {header}.
        Is this peaktable in the MZmine3 ALL format? If yes, contact the
        FERMO developers.
        ''')


def assert_mgf_format(ms2_dict):
    """Test mgf file for format and content"""
    assert ms2_dict


############
#PARSING
############


def parse_bioactiv_conc(bioactiv_table, value):
    """Parses bioactivity table and converts values depending on value
        
    Parameters
    ----------
    bioactiv_table : `pandas.core.frame.DataFrame`
    value : `str`
    
    Returns
    --------
    converted_df : `pandas.core.frame.DataFrame`
    
    Notes
    ------
    For reference to 'normalization#, refer to:
    Normalization calculation:
    #Stephan Kolassa 
    #(https://stats.stackexchange.com/users/1352/stephan-kolassa),
    #"scale a number between a range", 
    #URL (version: 2018-04-19): https://stats.stackexchange.com/q/281164
    """
    #scale to 0.1-1.0, lowest becomes highest (0 reserved for inactive)
    if value == 'conc':
        normalized = ""
        
        #test if all values equal (prevents division through 0)
        if (bioactiv_table['bioactivity'] == bioactiv_table['bioactivity'][0]).all():
            normalized = bioactiv_table.loc[:,'bioactivity'].apply(
            lambda x: 1)
        else:
            normalized = bioactiv_table.loc[:,'bioactivity'].apply(
                lambda x: (1 / x))
            normalized = normalized.apply(
                lambda x: round((
                    (((x - normalized.min()) /
                    (normalized.max() - 
                    normalized.min())) *
                    (1 - 0.1) + 0.1)
                ), 2)
            )
        
        converted_df = pd.concat(
            [bioactiv_table.loc[:,'sample_name'], normalized], axis=1)
        return converted_df

    #scale to 0.1-1 (for reference, see above)
    elif value == 'perc':
        normalized = ""
        
        #test if all values equal (prevents division through 0)
        if (bioactiv_table['bioactivity'] == bioactiv_table['bioactivity'][0]).all():
            normalized = bioactiv_table.loc[:,'bioactivity'].apply(
            lambda x: 1)
        else:
            normalized = bioactiv_table.loc[:,'bioactivity'].apply(
                lambda x: x)
            normalized = normalized.apply(
                lambda x: round((
                    (((x - normalized.min()) /
                    (normalized.max() - 
                    normalized.min())) *
                    (1 - 0.1) + 0.1)
                ), 2)
            )
        
        converted_df = pd.concat(
            [bioactiv_table.loc[:,'sample_name'], normalized], axis=1)
        return converted_df






##########
#DATA PROCESSING
##########




def peaktable_processing(input_file_store, params_df):
    """FERMO: peaktable processing
    
    Parameters
    ----------
    input_file_store : `dict`
        contains parsed user-provided input data
        'peaktable'
        'peaktable_name'
        'mgf'
        'mgf_name'
        'metadata'
        'metadata_name'
        'bioactivity'
        'bioactivity_name'
    params_df : `pandas.core.frame.DataFrame`
        contains user-provided parameters
    
    Returns
    --------
    FERMO_data : `dict`
        contains data to feed into dashboard visualization
    
    Notes
    ------
    """
    # ~ print(input_file_store['peaktable'])
    
    #concept: helfer function that serves as intermediate to 
    #launch separate functions that are in the 'processing' folder
    #Collects data, assembles dict, and returns to app for dashboard
    #visualization
    
    #TO DO:
    #samples = get_samplespecific_features()
    #determine_blank_features()
    #determine_bioactive_features()
    #calculate_similarity_cliques()
    #library_search()
    #run_ms2query()
    #samples = calculate_feature_overlap()
    #samples = calculate_metrics()
    #samples = calculate_pseudochrom_traces()
    
    #parse metadata file into a dict of sets
    groups = read_from_metadata_table(
        input_file_store['metadata'],
        input_file_store['metadata_name'],
        )
    
    #collect general sample stats into a dict
    sample_stats = collect_stats_samples(
        input_file_store['peaktable'],
        groups,
        input_file_store['bioactivity'],
        )
    
    #generate nested dict with feature information
    feature_dicts = feature_dicts_creation(
        input_file_store['peaktable'],
        input_file_store['mgf'],
        params_df.loc[1,'Values'],
        sample_stats
        )
    
    
    
    return 'dummy'
    





