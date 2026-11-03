from tensorflow.keras.models import load_model

for name in ["brain_tumor_cnn.keras", "brain_tumor_mobilenet.keras"]:
    m = load_model(name)
    cfg = m.optimizer.get_config()
    print("\n==", name, "==")
    print("Optimizer     :", m.optimizer.__class__.__name__)
    print("Learning rate :", cfg.get("learning_rate"))
    print("Weight decay  :", cfg.get("weight_decay"))
    print("Loss          :", m.loss)