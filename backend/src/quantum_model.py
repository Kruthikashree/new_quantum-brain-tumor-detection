"""
quantum_model.py

Improved Hybrid Quantum Neural Network
"""

import torch
import torch.nn as nn
import pennylane as qml

# ---------------------------------------------------
# Quantum Device
# ---------------------------------------------------

NUM_QUBITS = 4

dev = qml.device("lightning.qubit", wires=NUM_QUBITS)

# ---------------------------------------------------
# Quantum Circuit
# ---------------------------------------------------

@qml.qnode(dev, interface="torch")
def quantum_circuit(inputs, weights):

    # Encode learned features
    qml.AngleEmbedding(inputs, wires=range(NUM_QUBITS))

    # Quantum trainable circuit
    qml.StronglyEntanglingLayers(weights, wires=range(NUM_QUBITS))

    return [qml.expval(qml.PauliZ(i)) for i in range(NUM_QUBITS)]

# ---------------------------------------------------
# Quantum Layer
# ---------------------------------------------------

weight_shapes = {
    "weights": (6, NUM_QUBITS, 3)
}

quantum_layer = qml.qnn.TorchLayer(
    quantum_circuit,
    weight_shapes
)

# ---------------------------------------------------
# Hybrid Network
# ---------------------------------------------------

class HybridQuantumClassifier(nn.Module):

    def __init__(self):

        super().__init__()

        # -------------------------
        # Learn feature reduction
        # -------------------------

        self.feature_network = nn.Sequential(

            nn.Linear(1280, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.30),

            nn.Linear(512, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.30),

            nn.Linear(128, 32),
            nn.ReLU(),

            nn.Linear(32, 4)

        )

        # -------------------------
        # Quantum Layer
        # -------------------------

        self.quantum = quantum_layer

        # -------------------------
        # Classifier
        # -------------------------

        self.classifier = nn.Sequential(

            nn.Linear(4, 32),
            nn.ReLU(),

            nn.Dropout(0.20),

            nn.Linear(32, 16),
            nn.ReLU(),

            nn.Linear(16, 4)

        )

    def forward(self, x):

        # Learn feature compression
        x = self.feature_network(x)

        # Quantum processing
        x = self.quantum(x)

        # Classification
        x = self.classifier(x)

        return x


# ---------------------------------------------------
# Test
# ---------------------------------------------------

if __name__ == "__main__":

    model = HybridQuantumClassifier()

    sample = torch.rand(8, 1280)

    output = model(sample)

    print(model)

    print("\nInput Shape :", sample.shape)

    print("Output Shape:", output.shape)