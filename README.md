Dự đoán Kết quả Học tập bằng Học Máy
Mô tả
Dự án này phát triển một ứng dụng dự đoán kết quả học tập của học sinh bằng cách sử dụng các thuật toán học máy khác nhau, bao gồm:

Hồi quy tuyến tính (Linear Regression)
Lasso Regression
Mạng nơ-ron nhân tạo (Neural Network - MLPRegressor)
Stacking (kết hợp nhiều mô hình)
Các mô hình được xây dựng và triển khai trên framework Streamlit để tạo giao diện người dùng thân thiện, cho phép nhập liệu và xem kết quả dự đoán.

Mục tiêu
Mục tiêu chính của dự án là dự đoán kết quả học tập của học sinh dựa trên các đặc trưng như:

Giới tính (sex)
Thời gian học (studytime)
Số lần thất bại (failures)
Thời gian rảnh (freetime)
Số lần nghỉ học (absences)
Tham gia học thêm (nursery)
Công nghệ sử dụng
Python: ngôn ngữ lập trình chính
Streamlit: framework giúp phát triển giao diện web đơn giản cho mô hình
Scikit-learn: thư viện cung cấp các thuật toán hồi quy và mạng nơ-ron
Pandas & NumPy: xử lý và thao tác dữ liệu
Matplotlib & Seaborn: vẽ biểu đồ trực quan hóa dữ liệu
Mô hình thuật toán
Hồi quy tuyến tính (Linear Regression): Mô hình đơn giản để tìm mối quan hệ tuyến tính giữa các đặc trưng và kết quả.
Lasso Regression: Phiên bản của hồi quy tuyến tính có thêm phạt (regularization) để giảm thiểu overfitting.
Neural Network (MLPRegressor): Mô hình học sâu với các lớp ẩn, có khả năng học được những quan hệ phi tuyến tính.
Stacking: Kết hợp các mô hình trên nhằm nâng cao hiệu quả dự đoán.
Các chỉ số đánh giá mô hình
Mô hình được đánh giá dựa trên các tham số sau:

RMSE (Root Mean Squared Error): Căn bậc hai của trung bình bình phương sai số, phản ánh độ lệch của dự đoán so với giá trị thực tế.
MSE (Mean Squared Error): Trung bình bình phương sai số.
MAE (Mean Absolute Error): Trung bình sai số tuyệt đối.
R² (R-squared): Hệ số xác định, phản ánh mức độ mô hình giải thích được sự biến thiên của dữ liệu.
Cách chạy ứng dụng
Cài đặt các thư viện cần thiết:

bash
Sao chép mã
pip install -r requirements.txt
Chạy ứng dụng Streamlit:

bash
Sao chép mã
streamlit run app.py
Truy cập vào địa chỉ [http://localhost:8501](https://nhom3--64ktpm5.streamlit.app/) để sử dụng ứng dụng.

Tham khảo
Scikit-learn Documentation: https://scikit-learn.org/stable/documentation.html
Streamlit Documentation: https://docs.streamlit.io/
Marchine Learning cơ bản: https://machinelearningcoban.com/
