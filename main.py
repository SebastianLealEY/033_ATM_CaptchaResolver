import sys
import os
import json
import numpy as np
import cv2
import onnxruntime as ort

IMG_W, IMG_H = 128, 48

def resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        base_path = sys._MEIPASS # type: ignore
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)


MODEL_PATH = resource_path("model/captcha_model.onnx")
VOCAB_PATH = resource_path("model/vocab.json")


def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Modelo no encontrado: {MODEL_PATH}")

    if not os.path.exists(VOCAB_PATH):
        raise FileNotFoundError(f"Vocabulario no encontrado: {VOCAB_PATH}")

    sess = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])

    with open(VOCAB_PATH, "r", encoding="utf-8") as f:
        vocab = json.load(f)

    return sess, vocab


def preprocess(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(f"No se pudo leer la imagen: {image_path}")

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = (hsv[:, :, 1] > 30).astype(np.uint8)
    clean = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)

    gray = cv2.cvtColor(clean, cv2.COLOR_BGR2GRAY)
    gray = cv2.resize(gray, (IMG_W, IMG_H), interpolation=cv2.INTER_CUBIC)

    return gray.astype(np.float32) / 255.0


def decode(logits, vocab):
    preds = np.argmax(logits[:, 0, :], axis=1)
    chars = []
    prev = -1

    for p in preds:
        if p != prev and p != 0:
            chars.append(vocab[int(p)])
        prev = p

    return "".join(chars)


def recognize(image_path, sess, vocab):
    img = preprocess(image_path)
    inp = img[None, None, :, :]
    logits = sess.run(["logits"], {"image": inp})[0]
    return decode(logits, vocab).upper()


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("USO: 033_ATM_CaptchaResolver.py <ruta_imagen>", file=sys.stderr)
        print("O como ejecutable: 033_ATM_CaptchaResolver.exe <ruta_imagen>", file=sys.stderr)
        sys.exit(1)

    image_path = sys.argv[1]

    try:
        sess, vocab = load_model()
        result = recognize(image_path, sess, vocab)
        print(result)
        sys.exit(0)

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)