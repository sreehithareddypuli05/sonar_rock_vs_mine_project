import json
import pickle
import numpy as np
from django.shortcuts import render

MODEL_PATH = 'sonar_model.pkl'

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    HAS_PROBA = hasattr(model, 'predict_proba')
except Exception as e:
    model = None
    HAS_PROBA = False
    print(f"[ERROR] Could not load model: {e}")


def home(request):
    context = {
        'feature_range': range(60),
        'prediction': None,
        'rock_pct': None,
        'mine_pct': None,
        'input_values_json': '{}',
        'error': None,
    }

    if request.method == 'POST':
        if model is None:
            context['error'] = 'Model not loaded. Place sonar_model.pkl in the project root.'
            return render(request, 'sonar_app/home.html', context)

        try:
            features = []
            input_values = {}
            for i in range(60):
                raw = request.POST.get(f'f{i}', '').strip()
                val = float(raw)
                features.append(val)
                input_values[f'f{i}'] = val

            # Pass as JSON string so JS can parse it safely
            context['input_values_json'] = json.dumps(input_values)

            data = np.array(features).reshape(1, 60)
            result = model.predict(data)[0]

            result_str = str(result).strip().upper()
            if result_str in ('R', 'ROCK', '1'):
                context['prediction'] = 'Rock'
            else:
                context['prediction'] = 'Mine'

            if HAS_PROBA:
                proba = model.predict_proba(data)[0]
                classes = [str(c).upper() for c in model.classes_]
                mine_idx = next((i for i, c in enumerate(classes) if c in ('M', 'MINE', '0')), 0)
                rock_idx = next((i for i, c in enumerate(classes) if c in ('R', 'ROCK', '1')), 1)
                context['mine_pct'] = round(proba[mine_idx] * 100, 1)
                context['rock_pct'] = round(proba[rock_idx] * 100, 1)

        except ValueError:
            context['error'] = 'Invalid input — all 60 fields must be numbers between 0 and 1.'
        except Exception as e:
            context['error'] = f'Prediction error: {str(e)}'

    return render(request, 'sonar_app/home.html', context)