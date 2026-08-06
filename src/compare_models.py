"""
compare_models.py

Compare CNN, MobileNetV2 and Hybrid Quantum Model
"""

import matplotlib.pyplot as plt

# --------------------------------------------------
# Model Names
# --------------------------------------------------

models = [
    "CNN",
    "MobileNetV2",
    "Hybrid Quantum"
]

# --------------------------------------------------
# Final Accuracies
# --------------------------------------------------

accuracies = [
    69.31,
    89.94,
    93.06
]

# --------------------------------------------------
# Print Results
# --------------------------------------------------

print("\n==============================")
print("MODEL COMPARISON")
print("==============================\n")

for model, acc in zip(models, accuracies):
    print(f"{model:20s} : {acc:.2f}%")

best = models[accuracies.index(max(accuracies))]

print("\nBest Model :", best)
print("Accuracy   : {:.2f}%".format(max(accuracies)))

# --------------------------------------------------
# Plot
# --------------------------------------------------

plt.figure(figsize=(8,5))

bars = plt.bar(models, accuracies)

plt.title("Model Accuracy Comparison")

plt.xlabel("Models")

plt.ylabel("Accuracy (%)")

plt.ylim(0,100)

# Add values on bars
for bar in bars:

    height = bar.get_height()

    plt.text(
        bar.get_x()+bar.get_width()/2,
        height+1,
        f"{height:.2f}%",
        ha="center",
        fontsize=11
    )

plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()

plt.savefig(
    "model_comparison.png",
    dpi=300
)

plt.show()

print("\nComparison Graph Saved Successfully!")