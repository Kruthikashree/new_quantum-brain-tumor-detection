"""
plot_accuracy_bar.py

Bar chart comparing final test accuracy across all three models
(CNN, MobileNetV2, Hybrid Quantum), using the official numbers
already produced by evaluate_cnn.py / evaluate_mobilenet.py /
evaluate_quantum.py. No retraining needed -- instant.
"""

import os
import matplotlib.pyplot as plt

SAVE_FOLDER = "results"
os.makedirs(SAVE_FOLDER, exist_ok=True)

models = ["CNN\n(from scratch)", "MobileNetV2\n(transfer learning)", "Hybrid Quantum\nNeural Network"]
accuracies = [67.56, 89.94, 93.06]
colors = ["#94a3b8", "#f59e0b", "#2563eb"]

plt.figure(figsize=(8, 6))

bars = plt.bar(models, accuracies, color=colors, width=0.55)

for bar, acc in zip(bars, accuracies):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 1,
        f"{acc:.2f}%",
        ha="center",
        fontsize=13,
        fontweight="bold"
    )

plt.ylabel("Test Accuracy (%)", fontsize=12)
plt.title("Model Comparison: Test Accuracy", fontsize=14, fontweight="bold")
plt.ylim(0, 105)
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

save_path = os.path.join(SAVE_FOLDER, "quantum_vs_classical_curves.png")
plt.savefig(save_path, dpi=300, bbox_inches="tight")
plt.show()

print(f"\nSaved: {save_path}")
