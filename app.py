from flask import Flask, render_template, request, redirect, url_for
import math

app = Flask(__name__)

def calculate_queue(arrival_time, service_time):
    """
    Menghitung parameter antrian M/M/2.
    """
    arrival_rate = 1 / arrival_time  # λ (Laju kedatangan)
    service_rate = 1 / service_time  # μ (Laju pelayanan)
    c = 2  # Jumlah pelayan

    # Tingkat pemanfaatan sistem (ρ)
    rho = arrival_rate / (c * service_rate)
    if rho >= 1:
        return {"error": "Sistem tidak stabil (ρ ≥ 1). Tingkat kedatangan terlalu tinggi."}

    # Probabilitas tidak ada pelanggan dalam sistem (P0)
    sum_p0 = sum((arrival_rate / service_rate) ** n / math.factorial(n) for n in range(c))
    p0_denom = sum_p0 + ((arrival_rate / service_rate) ** c / (math.factorial(c) * (1 - rho)))
    P0 = 1 / p0_denom

    # Jumlah rata-rata pelanggan dalam antrian (Lq)
    Lq = (((arrival_rate / service_rate) ** c) * rho / (math.factorial(c) * (1 - rho) ** 2)) * P0

    # Waktu tunggu rata-rata dalam antrian (Wq)
    Wq = Lq / arrival_rate

    # Waktu rata-rata dalam sistem (W)
    W = Wq + (1 / service_rate)

    # Jumlah rata-rata pelanggan dalam sistem (L)
    L = arrival_rate * W

    return {
        "arrival_rate": round(arrival_rate, 3),
        "service_rate": round(service_rate, 3),
        "utilization": round(rho, 3),
        "p0": round(P0, 3),
        "average_queue_length": round(Lq, 3),
        "average_wait_time_queue": round(Wq, 3),
        "average_wait_time_system": round(W, 3),
        "average_customers_system": round(L, 3)
    }

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            arrival_time = float(request.form["arrival_time"])
            service_time = float(request.form["service_time"])
            result = calculate_queue(arrival_time, service_time)
            return redirect(url_for('result', **result))  # Mengarahkan ke halaman hasil
        except ValueError:
            return render_template("index.html", error_message="Input tidak valid. Masukkan angka yang benar.")
    return render_template("index.html")

@app.route("/result")
def result():
    # Mengambil hasil dari query string
    arrival_rate = request.args.get('arrival_rate')
    service_rate = request.args.get('service_rate')
    utilization = request.args.get('utilization')
    p0 = request.args.get('p0')
    average_queue_length = request.args.get('average_queue_length')
    average_wait_time_queue = request.args.get('average_wait_time_queue')
    average_wait_time_system = request.args.get('average_wait_time_system')
    average_customers_system = request.args.get('average_customers_system')
    error_message = request.args.get('error')

    result = {
        "arrival_rate": arrival_rate,
        "service_rate": service_rate,
        "utilization": utilization,
        "p0": p0,
        "average_queue_length": average_queue_length,
        "average_wait_time_queue": average_wait_time_queue,
        "average_wait_time_system": average_wait_time_system,
        "average_customers_system": average_customers_system
    }
    
    return render_template("result.html", result=result, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True)
