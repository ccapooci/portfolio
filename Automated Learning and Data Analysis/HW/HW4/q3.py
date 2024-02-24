# Import packages I may need.
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import LeaveOneOut

data_file = 'Data/adj_real_estate.csv'
all_data = pd.read_csv(data_file, header=1);

def solve_alphas(df):

    # variables for the system of equations
    lhs = np.zeros(4);
    rhs = np.zeros((4,4));

    # finding derivative in terms of alpha zero.
    lhs_vector = df['Y'];
    lhs[0] = lhs_vector.sum();

    rhs[0][0] = df.shape[0];

    rhs_alpha_1_vector = df['X1'];
    rhs[0][1] = rhs_alpha_1_vector.sum();

    rhs_alpha_2_vector = df['X2'];
    rhs[0][2] = rhs_alpha_2_vector.sum();

    rhs_alpha_3_vector = df['X3'];
    rhs[0][3] = rhs_alpha_3_vector.sum();

    # finding derivative in terms of alpha 1.
    lhs_vector = df['Y'] * df['X1'];
    lhs[1] = lhs_vector.sum();

    rhs[1][0] = df['X1'].sum();

    rhs_alpha_1_vector = df['X1'] * df['X1'];
    rhs[1][1] = rhs_alpha_1_vector.sum();

    rhs_alpha_2_vector = df['X2'] * df['X1'];
    rhs[1][2] = rhs_alpha_2_vector.sum();

    rhs_alpha_3_vector = df['X3'] * df['X1'];
    rhs[1][3] = rhs_alpha_3_vector.sum();

    # finding derivative in terms of alpha 2.
    lhs_vector = df['Y'] * df['X2'];
    lhs[2] = lhs_vector.sum();

    rhs[2][0] = df['X2'].sum();

    rhs_alpha_1_vector = df['X1'] * df['X2'];
    rhs[2][1] = rhs_alpha_1_vector.sum();

    rhs_alpha_2_vector = df['X2'] * df['X2'];
    rhs[2][2] = rhs_alpha_2_vector.sum();

    rhs_alpha_3_vector = df['X3'] * df['X2'];
    rhs[2][3] = rhs_alpha_3_vector.sum();

    # finding derivative in terms of alpha 3.
    lhs_vector = df['Y'] * df['X3'];
    lhs[3] = lhs_vector.sum();

    rhs[3][0] = df['X3'].sum();

    rhs_alpha_1_vector = df['X1'] * df['X3'];
    rhs[3][1] = rhs_alpha_1_vector.sum();

    rhs_alpha_2_vector = df['X2'] * df['X3'];
    rhs[3][2] = rhs_alpha_2_vector.sum();

    rhs_alpha_3_vector = df['X3'] * df['X3'];
    rhs[3][3] = rhs_alpha_3_vector.sum();

    alphas = np.linalg.solve(rhs, lhs)

    return alphas;

def solve_betas(df):

    lhs = np.zeros(4);
    rhs = np.zeros((4,4));

    # finding derivative in terms of beta zero.
    lhs_vector = df['Y'];
    lhs[0] = lhs_vector.sum();

    rhs[0][0] = df.shape[0];

    rhs_beta_1_vector = df['X1'] ** 1;
    rhs[0][1] = rhs_beta_1_vector.sum();

    rhs_beta_2_vector = df['X2'] ** 2; 
    rhs[0][2] = rhs_beta_2_vector.sum();

    rhs_beta_3_vector = df['X3'] ** 3;
    rhs[0][3] = rhs_beta_3_vector.sum();

    # finding derivative in terms of beta 1.
    lhs_vector = df['Y'] * df['X1'];
    lhs[1] = lhs_vector.sum();

    rhs[1][0] = df['X1'].sum();

    rhs_beta_1_vector = df['X1'] ** 1 * df['X1'];
    rhs[1][1] = rhs_beta_1_vector.sum();

    rhs_beta_2_vector = df['X2'] ** 2 * df['X1'];
    rhs[1][2] = rhs_beta_2_vector.sum();

    rhs_beta_3_vector = df['X3'] ** 3 * df['X1'];
    rhs[1][3] = rhs_beta_3_vector.sum();

    # finding derivative in terms of beta 2.
    lhs_vector = df['Y'] * df['X2'] ** 2;
    lhs[2] = lhs_vector.sum();

    rhs[2][0] = (df['X2'] ** 2).sum();

    rhs_beta_1_vector = df['X1'] ** 1 * df['X2'] ** 2;
    rhs[2][1] = rhs_beta_1_vector.sum();

    rhs_beta_2_vector = df['X2'] ** 2 * df['X2'] ** 2;
    rhs[2][2] = rhs_beta_2_vector.sum();

    rhs_beta_3_vector = df['X3'] ** 3 * df['X2'] ** 2;
    rhs[2][3] = rhs_beta_3_vector.sum();

    # finding derivative in terms of beta 3.
    lhs_vector = df['Y'] * (df['X3'] ** 3);
    lhs[3] = lhs_vector.sum();

    rhs[3][0] = (df['X3'] ** 3).sum();

    rhs_beta_1_vector = df['X1'] ** 1 * df['X3'] ** 3;
    rhs[3][1] = rhs_beta_1_vector.sum();

    rhs_beta_2_vector = df['X2'] ** 2 * df['X3'] ** 3;
    rhs[3][2] = rhs_beta_2_vector.sum();

    rhs_beta_3_vector = df['X3'] ** 3 * df['X3'] ** 3;
    rhs[3][3] = rhs_beta_3_vector.sum();

    betas = np.linalg.solve(rhs, lhs)

    return betas;

def solve_gammas(df):

    lhs = np.zeros(4);
    rhs = np.zeros((4,4));

    # finding derivative in terms of gamma zero.
    lhs_vector = df['Y'];
    lhs[0] = lhs_vector.sum();

    rhs[0][0] = df.shape[0];

    rhs_gamma_1_vector = df['X1'] ** 1;
    rhs[0][1] = rhs_gamma_1_vector.sum();

    rhs_gamma_2_vector = df['X2'] ** 2; 
    rhs[0][2] = rhs_gamma_2_vector.sum();

    rhs_gamma_3_vector = df['X3'] ** 1;
    rhs[0][3] = rhs_gamma_3_vector.sum();

    # finding derivative in terms of gamma 1.
    lhs_vector = df['Y'] * df['X1'];
    lhs[1] = lhs_vector.sum();

    rhs[1][0] = df['X1'].sum();

    rhs_gamma_1_vector = df['X1'] ** 1 * df['X1'];
    rhs[1][1] = rhs_gamma_1_vector.sum();

    rhs_gamma_2_vector = df['X2'] ** 2 * df['X1'];
    rhs[1][2] = rhs_gamma_2_vector.sum();

    rhs_gamma_3_vector = df['X3'] ** 3 * df['X1'];
    rhs[1][3] = rhs_gamma_3_vector.sum();

    # finding derivative in terms of gamma 2.
    lhs_vector = df['Y'] * df['X2'] ** 2;
    lhs[2] = lhs_vector.sum();

    rhs[2][0] = (df['X2'] ** 2).sum();

    rhs_gamma_1_vector = df['X1'] ** 1 * df['X2'] ** 2;
    rhs[2][1] = rhs_gamma_1_vector.sum();

    rhs_gamma_2_vector = df['X2'] ** 2 * df['X2'] ** 2;
    rhs[2][2] = rhs_gamma_2_vector.sum();

    rhs_gamma_3_vector = df['X3'] ** 1 * df['X2'] ** 2;
    rhs[2][3] = rhs_gamma_3_vector.sum();

    # finding derivative in terms of gamma 3.
    lhs_vector = df['Y'] * (df['X3'] ** 1);
    lhs[3] = lhs_vector.sum();

    rhs[3][0] = (df['X3'] ** 1).sum();

    rhs_gamma_1_vector = df['X1'] ** 1 * df['X3'] ** 1;
    rhs[3][1] = rhs_gamma_1_vector.sum();

    rhs_gamma_2_vector = df['X2'] ** 2 * df['X3'] ** 1;
    rhs[3][2] = rhs_gamma_2_vector.sum();

    rhs_gamma_3_vector = df['X3'] ** 1 * df['X3'] ** 1;
    rhs[3][3] = rhs_gamma_3_vector.sum();

    gammas = np.linalg.solve(rhs, lhs)

    return gammas;

def predict_alphas(alphas, xs):
    return alphas[1] * xs[1] + alphas[2] * xs[2] + alphas[3] * xs[3] + alphas[0]; 

def predict_betas(betas, xs):
    return betas[1] * xs[1] + betas[2] * xs[2] ** 2 + betas[3] * xs[3] ** 3 + betas[0]; 

def predict_gammas(gammas, xs):
    return gammas[1] * xs[1] + gammas[2] * xs[2] ** 2 + gammas[3] * xs[3] + gammas[0]; 


print(solve_alphas(all_data));
print(solve_betas(all_data));
print(solve_gammas(all_data));



#define cross-validation method to use
loo = LeaveOneOut()
loo.get_n_splits(all_data.drop(columns=['Y']));
predictions_alpha = pd.DataFrame(all_data['Y']);
predictions_beta = pd.DataFrame(all_data['Y']);
predictions_gamma = pd.DataFrame(all_data['Y']);
result = all_data['Y'];

y_alphas = np.zeros(all_data.shape[0]); 
y_betas = np.zeros(all_data.shape[0]); 
y_gammas = np.zeros(all_data.shape[0]);

for train_index, test_index in loo.split(all_data):
    train_data = all_data.drop(labels=test_index, axis=0)
    test_data = all_data.iloc[test_index];
    test_result = result.iloc[test_index];

    alphas = solve_alphas(train_data);
    betas = solve_betas(train_data);
    gammas = solve_gammas(train_data);

    xs = np.zeros(4);
    xs[0] = 0;
    xs[1] = test_data['X1'];
    xs[2] = test_data['X2'];
    xs[3] = test_data['X3'];

    y_alphas[test_index] = predict_alphas(alphas, xs);
    y_betas[test_index] = predict_betas(betas, xs);
    y_gammas[test_index] = predict_gammas(gammas, xs);
   

rms_alpha = mean_squared_error(all_data['Y'], y_alphas, squared=False)
rms_beta = mean_squared_error(all_data['Y'], y_betas, squared=False)
rms_gamma = mean_squared_error(all_data['Y'], y_gammas, squared=False)

print("RMSE for alphas is " + str(rms_alpha));
print("RMSE for betas is " + str(rms_beta));
print("RMSE for gammas is " + str(rms_gamma));