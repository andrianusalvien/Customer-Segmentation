# 📊 Customer Segmentation Dashboard (RFM Analysis)

Dashboard interaktif berbasis **Streamlit** untuk melakukan **Customer Segmentation** menggunakan metode **RFM (Recency, Frequency, Monetary)** pada dataset Superstore.  

Dengan dashboard ini, kita bisa mengetahui:
- Segmentasi pelanggan seperti **Champion, At Risk, Potential Loyalist, Loyal Customer**, dll.
- Distribusi pelanggan per segmen
- Profit per segmen
- Persebaran pelanggan per waktu
- Distribusi sales per kategori
- Filter berdasarkan **waktu** dan **state**

---

## 🚀 Fitur Utama
- **Summary Info**: Total Customers & Total Profit
- **Filter Waktu**: Pilih range tanggal order
- **Filter State**: Lihat distribusi pelanggan per state
- **Filter Segmentasi**: Tampilkan hanya segmen tertentu
- **Visualisasi**:
  - Pie chart distribusi segmen
  - Profit by Segment
  - Distribusi kategori produk
  - Customer over time (line chart)
- **Tabel RFM**: Detail customer dengan nilai Recency, Frequency, Monetary, Profit, dan Segmen

---

## 📂 Dataset
Dataset yang digunakan: [Superstore Dataset](https://raw.githubusercontent.com/andrianusalvien/Customer-Satisfaction-and-Sentiment-Analysis/refs/heads/main/superstore_dataset%20-%20segmentation%20-%20superstore.csv)  
Berisi data transaksi penjualan dengan kolom seperti:
- `order_id`, `order_date`, `customer_id`, `state`, `sales`, `profit`, dll.


## Link Dashboard
>>>>> https://customersegmentation8.streamlit.app/
>>>>> 
<img width="1355" height="644" alt="Cuplikan layar 2025-10-02 122948" src="https://github.com/user-attachments/assets/ba743b71-0730-4f06-aaaf-4ebc4068d8df" />
