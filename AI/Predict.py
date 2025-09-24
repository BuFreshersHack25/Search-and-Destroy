import sys
from pathlib import Path
from PIL import Image
import torch
from transformers import ViTForImageClassification, ViTImageProcessor


def load_model(model_name: str):
    print(f"Loading model: {model_name}")
    model = ViTForImageClassification.from_pretrained(model_name)
    processor = ViTImageProcessor.from_pretrained(model_name)
    model.eval()
    return model, processor


def parse_scientific_name(label: str):
    parts = label.split("_")
    if len(parts) >= 2:
        genus, species = parts[-2], parts[-1]
        return f"{genus} {species}"
    return label  # fallback


def predict_top(image_path: str, model, processor):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = torch.nn.functional.softmax(logits, dim=-1)

    top_prob, top_idx = torch.max(probs, dim=-1)
    raw_label = model.config.id2label[top_idx.item()]
    sci_name = parse_scientific_name(raw_label)
    return sci_name, float(top_prob)


def main():
    if len(sys.argv) < 2:
        print("Usage: python Predict.py path/to/image.jpg")
        sys.exit(1)

    image_path = sys.argv[1]
    if not Path(image_path).exists():
        print(f"Error: Image not found at {image_path}")
        sys.exit(1)

    model_name = "bryanzhou008/vit-base-patch16-224-in21k-finetuned-inaturalist"
    model, processor = load_model(model_name)

    sci_name, prob = predict_top(image_path, model, processor)

    print(f"Top prediction for {image_path}:")
    print(f"{sci_name}   {prob*100:.2f}% confidence")


if __name__ == "__main__":
    main()

