# !pip install pycaret
# Pycaret Install kr lena and pandas too




import pandas as pd
from pycaret.classification import *
from pycaret.regression import *
import os, csv, json
module_dir = os.path.dirname(__file__)
file_path = os.path.join(module_dir, 'blood.csv')

# data_file = open(file_path , 'rb')
# data = data_file.read()



# dataset.drop_duplicates()
# path of the file ^

def run_me(reg, clas, file):
    res = {}
    dataset = pd.read_csv('http://127.0.0.1:8000/static/upload/'+file)


    if(reg!="" and reg!=None):
        columnNameReg = reg.split(',')[0]

        # dataset.dropna(subset=[columnNameReg])

        exp_reg101 = pycaret.regression.setup(data = dataset, target = columnNameReg, train_size = 0.7, categorical_features = None, categorical_imputation = 'constant', ordinal_features = None, high_cardinality_features = None, high_cardinality_method = 'frequency', numeric_features = None, numeric_imputation = 'mean', date_features = None, ignore_features = None, normalize = True, normalize_method = 'zscore', transformation = False, transformation_method = 'yeo-johnson', handle_unknown_categorical = True, unknown_categorical_method = 'least_frequent', pca = False, pca_method = 'linear', pca_components = None, ignore_low_variance = False, combine_rare_levels = False, rare_level_threshold = 0.10, bin_numeric_features = None, remove_outliers = False, outliers_threshold = 0.05, remove_multicollinearity = False, multicollinearity_threshold = 0.9, remove_perfect_collinearity = False, create_clusters = False, cluster_iter = 20, polynomial_features = False, polynomial_degree = 2, trigonometry_features = False, polynomial_threshold = 0.1, group_features = None, group_names = None, feature_selection = False, feature_selection_threshold = 0.8, feature_interaction = False, feature_ratio = False, interaction_threshold = 0.01, transform_target = False, transform_target_method = 'box-cox', data_split_shuffle = True, n_jobs = -1, html = True, session_id = None, log_experiment = False, experiment_name = None, log_plots = False, log_profile = False, log_data = False, silent=False, verbose = True, profile = False)
        cmp = pycaret.regression.compare_models()
        storecmp = pull()
        #print(storecmp)
        # storecmp is the pandas DataFrame containing all the R2, MAE, MSE, etc. values for 17 reg models

        cmplist = storecmp.values.tolist()
        # print(cmplist)
        cols = [col for col in storecmp.columns]
        jlist = list()

        shortform = list()

        for row in cmplist:
            data_entry = dict()
            for i,value in enumerate(row):
                if i == 0:
                    short = ""
                    for ch in value.split():
                        short += ch[0]
                    shortform.append(short)
                    value = short
                data_entry[cols[i]] = value
            jlist.append(data_entry)
        jlist = json.dumps(jlist)
        print(jlist)
        res['reg'] = jlist

    if(clas!="" and clas!=None):
        columnNameClass = clas.split(',')[0]
        # dataset.dropna(subset=[columnNameClass])
        clf1 = pycaret.classification.setup(data = dataset, target = columnNameClass, train_size = 0.7, categorical_features = None, categorical_imputation = 'constant', ordinal_features = None, high_cardinality_features = None, high_cardinality_method = 'frequency', numeric_features = None, numeric_imputation = 'mean', date_features = None, ignore_features = None, normalize = True, normalize_method = 'zscore', transformation = False, transformation_method = 'yeo-johnson', handle_unknown_categorical = True, unknown_categorical_method = 'least_frequent', pca = False, pca_method = 'linear', pca_components = None, ignore_low_variance = False, combine_rare_levels = False, rare_level_threshold = 0.10, bin_numeric_features = None, remove_outliers = False, outliers_threshold = 0.05, remove_multicollinearity = False, multicollinearity_threshold = 0.9, remove_perfect_collinearity = False, create_clusters = False, cluster_iter = 20, polynomial_features = False, polynomial_degree = 2, trigonometry_features = False, polynomial_threshold = 0.1, group_features = None, group_names = None, feature_selection = False, feature_selection_threshold = 0.8, feature_interaction = False, feature_ratio = False, interaction_threshold = 0.01, data_split_shuffle = True, n_jobs = -1, html = True, session_id = None, log_experiment = False, experiment_name = None, log_plots = False, log_profile = False, log_data = False, silent=False, verbose=True, profile = False)
        cmp2 = pycaret.classification.compare_models()
        storecmp2 = pull()
        #print(storecmp2)
        # storecmp is the pandas DataFrame containing all the R2, MAE, MSE, etc. values for 14 classification models

        cmplist2 = storecmp2.values.tolist()
        # print(cmplist2)
                
        cols2 = [col for col in storecmp2.columns]
        jlist2 = list()

        shortform2 = []

        for row in cmplist2:
            data_entry2 = dict()
            for i,value in enumerate(row):
                if i == 0:
                    short = ""
                    for ch in value.split():
                        short += ch[0]
                    shortform2.append(short)
                    value = short
                data_entry2[cols2[i]] = value
            jlist2.append(data_entry2)
        jlist2 = json.dumps(jlist2)
        print(jlist2)
        res['clas'] = jlist2
        # cmplist contains the above df in list format please view the dataframe once to get to know which value in the list are which ones
        return res

def get_cols(file):
    df = pd.read_csv('http://127.0.0.1:8000/static/upload/'+file)
    cols = list(df.columns)
    str = ""
    for i in cols:
        str+=i+","
    # print(str)
    return str[:-1]
    
def handle_db(file, username): 
    

    with open('core/static/upload/'+username+"_"+file.name, 'wb+') as destination:  
        for chunk in file.chunks():
            destination.write(chunk)
    return username+'_'+file.name