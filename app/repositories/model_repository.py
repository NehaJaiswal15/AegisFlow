from transformers import pipeline


class ModelRepository:
    """
    Registry that can load and manage multiple model versions.
    Only ONE file in the entire app touches HuggingFace — this one.
    """

    def __init__(self):
        self._models: dict = {}          # {"v1": pipeline, "v2": pipeline}
        self._active_version: str = None  # Which version to use by default

    def load_model(self, model_name: str, version: str = "v1"):
        """Load a HuggingFace model and register it under a version tag."""
        print(f"Loading model '{model_name}' as version '{version}' ...")
        self._models[version] = pipeline(
            "text-classification",
            model=model_name,
            device=-1,
        )

        # First model loaded becomes the active version
        if self._active_version is None:
            self._active_version = version

        print(f"Model loaded successfully! Version: {version}")

    def predict(self, text: str, version: str = None) -> dict:
        """
        Run prediction using a specific model version.
        If no version specified, uses the active (default) version.
        """
        version = version or self._active_version

        if version not in self._models:
            raise RuntimeError(f"Model version '{version}' not found. "
                               f"Available: {list(self._models.keys())}")

        result = self._models[version](text, truncation=True, max_length=512)

        return {
            "label": result[0]["label"],
            "score": result[0]["score"],
            "model_version": version,
        }

    def set_active_version(self, version: str):
        """Switch which model version is used by default."""
        if version not in self._models:
            raise RuntimeError(f"Version '{version}' not loaded.")
        self._active_version = version

    def get_active_version(self) -> str:
        return self._active_version

    def get_loaded_versions(self) -> list:
        return list(self._models.keys())

    def is_loaded(self) -> bool:
        return len(self._models) > 0


# Single global instance
model_repo = ModelRepository()
