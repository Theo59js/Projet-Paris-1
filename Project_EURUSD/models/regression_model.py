import statsmodels.api as sm


def train_model(merged_df):
    var_ex = merged_df.iloc[:, [2, 3]]
    var_dep = merged_df.iloc[:, 1]

    var_ex = sm.add_constant(var_ex)

    regeurusd = sm.OLS(var_dep, var_ex).fit()
    return regeurusd, var_ex


def make_predictions(model, predict_datas_const):
    return model.predict(predict_datas_const)