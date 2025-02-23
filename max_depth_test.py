import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import StackingRegressor, RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import GridSearchCV

# 1. Đọc và tiền xử lý dữ liệu
df = pd.read_csv('student-mat.csv', sep=';')

# Chỉ lấy các cột cần thiết 
df = df[['sex', 'studytime', 'failures', 'absences', 'freetime', 'nursery', 'G1', 'G2', 'G3']]

# Biến đổi cột 'sex' thành nhãn số (Label Encoding)
le = LabelEncoder()
df['sex'] = le.fit_transform(df['sex'])
df['nursery'] = le.fit_transform(df['nursery'])  # Mã hóa nursery

# Tách biến đầu vào và biến mục tiêu
X = df[['sex', 'studytime', 'failures', 'absences', 'freetime', 'nursery', 'G1', 'G2']]  # Chỉ lấy 8 thuộc tính
y = df['G3']

# Chia dữ liệu thành tập train, validation, và test
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=42)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Chuẩn hóa dữ liệu
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)
X_test_scaled = scaler.transform(X_test)

# 2. Xây dựng các mô hình
# 2.1 Hồi quy tuyến tính
linear_model = LinearRegression()
linear_model.fit(X_train_scaled, y_train)

# 2.2 Lasso Regression
lasso_model = Lasso()
param_grid = {'alpha': [0.001, 0.01, 0.1, 1, 10]}
grid_search = GridSearchCV(lasso_model, param_grid, cv=5)
grid_search.fit(X_train_scaled, y_train)
best_lasso = grid_search.best_estimator_

# 2.3 Neural Network - MLPRegressor
mlp_model = MLPRegressor(hidden_layer_sizes=(50, 50, 50), max_iter=1000, random_state=42, learning_rate='adaptive', alpha=0.0001)
mlp_model.fit(X_train_scaled, y_train)

# Tạo mô hình Stacking từ các mô hình hồi quy trước đó (base models)
estimators = [
    ('linear', linear_model),
    ('lasso', best_lasso),
    ('mlp', mlp_model)
]

# Thử nhiều tham số cho max_depth
max_depth_list = [5, 10, 15, 20, 25, 30]
results = []

for max_depth in max_depth_list:
    stacking_model = StackingRegressor(
        estimators=estimators, 
        final_estimator=RandomForestRegressor(n_estimators=50, max_depth=max_depth, random_state=42)
    )
    stacking_model.fit(X_train_scaled, y_train)

    # Dự đoán cho tập kiểm tra
    y_pred_stacking_test = stacking_model.predict(X_test_scaled)

    # Tính toán các chỉ số cho Stacking
    mse_stacking_test = mean_squared_error(y_test, y_pred_stacking_test)
    rmse_stacking_test = np.sqrt(mse_stacking_test)
    mae_stacking_test = mean_absolute_error(y_test, y_pred_stacking_test)
    r2_stacking_test = r2_score(y_test, y_pred_stacking_test)

    # Lưu kết quả vào danh sách
    results.append({
        'max_depth': max_depth,
        'MSE': mse_stacking_test,
        'RMSE': rmse_stacking_test,
        'MAE': mae_stacking_test,
        'R2': r2_stacking_test
    })

# Chuyển kết quả thành DataFrame
results_df = pd.DataFrame(results)

# 3. Giao diện Streamlit
st.title("Dự đoán kết quả học tập")

# Hiển thị bảng kết quả
st.subheader("Kết quả cho các giá trị max_depth")
st.dataframe(results_df)

# Nhập thông tin từ người dùng
sex = st.selectbox("Giới tính", ("Nam", "Nữ"))
studytime = st.slider("Thời gian học tập (1-4)", 1, 4, 2)
failures = st.slider("Số lần trượt môn", 0, 3, 0)
absences = st.slider("Số % nghỉ học", 0, 93, 5)
freetime = st.slider("Thời gian rảnh (1-5)", 1, 5, 3)
nursery = st.selectbox("Có đi học thêm không", ("Có", "Không"))
g1 = st.slider("Điểm kiểm Tra lần 1", 0, 20)
g2 = st.slider("Điểm kiểm tra lần 2", 0, 20)

# Chuyển đổi giới tính và nursery
sex = 1 if sex == "Nam" else 0
nursery = 1 if nursery == "Có" else 0

# Khi người dùng nhấn nút "Dự đoán"
if st.button("Dự đoán"):
    # Chuẩn bị dữ liệu để dự đoán (chuẩn hóa dữ liệu)
    features = np.array([[sex, studytime, failures, absences, freetime, nursery, g1, g2]])
    features_scaled = scaler.transform(features)

    # Dự đoán với tất cả các mô hình
    prediction_linear = linear_model.predict(features_scaled)[0]
    prediction_lasso = best_lasso.predict(features_scaled)[0]
    prediction_mlp = mlp_model.predict(features_scaled)[0]

    # Dự đoán với mô hình Stacking tốt nhất
    best_stacking_model = StackingRegressor(
        estimators=estimators,
        final_estimator=RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)  # Sử dụng giá trị max_depth = 10
    )
    best_stacking_model.fit(X_train_scaled, y_train)
    prediction_stacking = best_stacking_model.predict(features_scaled)[0]

    # Hiển thị kết quả dự đoán
    st.subheader("Kết quả dự đoán:")
    st.write(f"**Linear Regression:** {prediction_linear:.2f}")
    st.write(f"**Lasso Regression:** {prediction_lasso:.2f}")
    st.write(f"**Neural Network (MLP):** {prediction_mlp:.2f}")
    st.write(f"**Stacking:** {prediction_stacking:.2f}")

    # Biểu đồ so sánh giá trị thực và dự đoán trên tập huấn luyện
    fig_train, ax_train = plt.subplots()
    ax_train.scatter(y_train, linear_model.predict(X_train_scaled), edgecolors=(0, 0, 0), label='Linear Regression')
    ax_train.scatter(y_train, best_lasso.predict(X_train_scaled), edgecolors=(0, 0, 0), label='Lasso Regression')
    ax_train.scatter(y_train, mlp_model.predict(X_train_scaled), edgecolors=(0, 0, 0), label='Neural Network')
    ax_train.scatter(y_train, stacking_model.predict(X_train_scaled), edgecolors=(0, 0, 0), label='Stacking')
    ax_train.plot([min(y_train), max(y_train)], [min(y_train), max(y_train)], 'k--', lw=2)
    ax_train.set_xlabel('Giá trị thực tế (Tập huấn luyện)')
    ax_train.set_ylabel('Giá trị dự đoán (Tập huấn luyện)')
    ax_train.set_title('So sánh giá trị thực tế và dự đoán - Tập huấn luyện')
    ax_train.legend()

    st.subheader("Biểu đồ Tập Huấn Luyện")
    plt.tight_layout()
    st.pyplot(fig_train)
    
    # Vẽ biểu đồ cho tập xác thực
    fig_val, ax_val = plt.subplots()
    ax_val.scatter(y_val, linear_model.predict(X_val_scaled), edgecolors=(0, 0, 0), label='Linear Regression')
    ax_val.scatter(y_val, best_lasso.predict(X_val_scaled), edgecolors=(0, 0, 0), label='Lasso Regression')
    ax_val.scatter(y_val, mlp_model.predict(X_val_scaled), edgecolors=(0, 0, 0), label='Neural Network')
    ax_val.scatter(y_val, stacking_model.predict(X_val_scaled), edgecolors=(0, 0, 0), label='Stacking')
    ax_val.plot([min(y_val), max(y_val)], [min(y_val), max(y_val)], 'k--', lw=2)
    ax_val.set_xlabel('Giá trị thực tế (Tập xác thực)')
    ax_val.set_ylabel('Giá trị dự đoán (Tập xác thực)')
    ax_val.set_title('So sánh giá trị thực tế và dự đoán - Tập xác thực')
    ax_val.legend()

    st.subheader("Biểu đồ Tập Xác Thực")
    plt.tight_layout()
    st.pyplot(fig_val)
