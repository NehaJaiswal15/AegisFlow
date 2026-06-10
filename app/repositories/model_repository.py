from transformers import pipeline


class ModelRepository:
    """
    Loads and runs the toxicity classification model.
    This is the ONLY file that touches HuggingFace directly.
    """

    def __init__(self):
        self._model = None
        self._model_version = None

    def load_model(self, model_name: str, version: str = "v1"):
        """Load the HuggingFace model into memory. Called once at startup."""
        print(f"Loading model: {model_name} ...")
        self._model = pipeline(
            "text-classification",
            model=model_name,
            device=-1, 
        )
        self._model_version = version
        print(f"Model loaded successfully! Version: {version}")

    def predict(self, text: str) -> dict:
        """Run toxicity prediction on the given text."""
        if self._model is None:
            raise RuntimeError("Model not loaded! Call load_model() first.")

        result = self._model(text, truncation=True, max_length=512)
        print(f"DEBUG raw model output: {result}")

        return {
            "label": result[0]["label"],
            "score": result[0]["score"],
            "model_version": self._model_version,
        }

    def is_loaded(self) -> bool:
        return self._model is not None


# Single global instance — shared across the entire app
model_repo = ModelRepository()
