/**
 * CarePulse Frontend Controller
 * Handles Chart.js visualization, dynamic filtering, routine toggles & alerts.
 */

document.addEventListener("DOMContentLoaded", () => {
    // 1. Auto-dismiss flash alerts after 4 seconds
    const alerts = document.querySelectorAll(".alert-toast");
    alerts.forEach((alert) => {
        setTimeout(() => {
            alert.style.transition = "opacity 0.4s ease, transform 0.4s ease";
            alert.style.opacity = "0";
            alert.style.transform = "translateY(-10px)";
            setTimeout(() => alert.remove(), 400);
        }, 4500);
    });

    // 2. Initialize Vitals Charts if canvas exists
    initVitalsCharts();

    // 3. Client-side quick filter for medicine list
    const searchInput = document.getElementById("clientSearchInput");
    if (searchInput) {
        searchInput.addEventListener("input", (e) => {
            const query = e.target.value.toLowerCase().trim();
            const rows = document.querySelectorAll(".medicine-row");

            rows.forEach((row) => {
                const text = row.innerText.toLowerCase();
                row.style.display = text.includes(query) ? "" : "none";
            });
        });
    }

    // 4. AJAX Toggle for Daily Routine Checkboxes
    const routineToggles = document.querySelectorAll(".routine-toggle-btn");
    routineToggles.forEach((btn) => {
        btn.addEventListener("click", async (e) => {
            e.preventDefault();
            const itemId = btn.getAttribute("data-id");
            const itemElement = document.getElementById(`routine-item-${itemId}`);

            try {
                const res = await fetch(`/routine/toggle/${itemId}`, {
                    method: "POST",
                    headers: { "X-Requested-With": "XMLHttpRequest" }
                });
                const data = await res.json();
                if (data.success) {
                    itemElement.classList.toggle("taken");
                    const statusText = itemElement.querySelector(".taken-status-text");
                    if (itemElement.classList.contains("taken")) {
                        btn.textContent = "Mark Pending ↺";
                        btn.className = "btn btn-outline btn-sm routine-toggle-btn";
                        if (statusText) statusText.textContent = "✅ Taken Today";
                    } else {
                        btn.textContent = "Mark as Taken ✓";
                        btn.className = "btn btn-primary btn-sm routine-toggle-btn";
                        if (statusText) statusText.textContent = "Pending";
                    }
                }
            } catch (err) {
                console.error("Failed to toggle routine state:", err);
            }
        });
    });
});

/**
 * Loads Vitals Data from /api/vitals-chart and renders Blood Pressure and Sugar charts.
 */
async function initVitalsCharts() {
    const bpCanvas = document.getElementById("bpChartCanvas");
    const sugarCanvas = document.getElementById("sugarChartCanvas");

    if (!bpCanvas && !sugarCanvas) return;

    try {
        const response = await fetch("/api/vitals-chart");
        const data = await response.json();

        // 1. Blood Pressure Line Chart
        if (bpCanvas && typeof Chart !== "undefined") {
            new Chart(bpCanvas, {
                type: "line",
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: "Systolic (Upper, mm Hg)",
                            data: data.systolic,
                            borderColor: "#dc2626",
                            backgroundColor: "rgba(220, 38, 38, 0.1)",
                            borderWidth: 2.5,
                            tension: 0.3,
                            fill: true,
                            pointRadius: 4
                        },
                        {
                            label: "Diastolic (Lower, mm Hg)",
                            data: data.diastolic,
                            borderColor: "#0284c7",
                            backgroundColor: "rgba(2, 132, 199, 0.1)",
                            borderWidth: 2.5,
                            tension: 0.3,
                            fill: true,
                            pointRadius: 4
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: "top" },
                        tooltip: { mode: "index", intersect: false }
                    },
                    scales: {
                        y: {
                            min: 60,
                            max: 180,
                            title: { display: true, text: "mm Hg" }
                        }
                    }
                }
            });
        }

        // 2. Blood Sugar Chart
        if (sugarCanvas && typeof Chart !== "undefined") {
            new Chart(sugarCanvas, {
                type: "bar",
                data: {
                    labels: data.labels,
                    datasets: [
                        {
                            label: "Blood Sugar (mg/dL)",
                            data: data.blood_sugar,
                            backgroundColor: data.blood_sugar.map((val) =>
                                val > 140 ? "rgba(239, 68, 68, 0.85)" : "rgba(13, 148, 136, 0.85)"
                            ),
                            borderRadius: 6
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: "top" }
                    },
                    scales: {
                        y: {
                            min: 50,
                            max: 200,
                            title: { display: true, text: "mg/dL" }
                        }
                    }
                }
            });
        }
    } catch (e) {
        console.error("Error initializing vitals charts:", e);
    }
}
