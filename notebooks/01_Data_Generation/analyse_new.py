import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


def analyze_variance(file_path: str):
  print(f'Lade Datensatz aus {file_path}...')
  texts = []

  with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
      if line.strip():
        data = json.loads(line)
        if 'text' in data:
          texts.append(data['text'])

  if not texts:
    print('Keine Texte im Feld "text" gefunden!')
    return

  print(f'{len(texts)} Dialoge erfolgreich geladen. Berechne Embeddings...')

  # Nutzt standardmäßig die GPU, falls PyTorch CUDA erkennt
  model = SentenceTransformer('all-MiniLM-L6-v2', device='cuda')
  embeddings = model.encode(texts, show_progress_bar=True, batch_size=64)

  print('Berechne semantische Ähnlichkeitsmatrix...')
  sim_matrix = cosine_similarity(embeddings)

  # Diagonale (Vergleich mit sich selbst) herausrechnen
  np.fill_diagonal(sim_matrix, np.nan)

  avg_sim = np.nanmean(sim_matrix)
  max_sim = np.nanmax(sim_matrix)
  min_sim = np.nanmin(sim_matrix)

  print('\n--- ERGEBNIS DER VARIANZ-ANALYSE ---')
  print(f'Analysierte Datensätze : {len(texts)}')
  print(f'Durchschnittl. Ähnlichkeit: {avg_sim:.4f} (je niedriger, desto besser)')
  print(f'Höchste Ähnlichkeit     : {max_sim:.4f} (Duplikat-Gefahr)')
  print(f'Geringste Ähnlichkeit   : {min_sim:.4f} (Maximale Bandbreite)')

  print('\nInterpretation:')
  if avg_sim < 0.65:
    print(
        '🌟 Hervorragend: Dein Datensatz hat eine sehr hohe semantische Vielfalt!'
    )
  elif avg_sim < 0.80:
    print('👍 Solider Wert: Gute Mischung aus roter Faden und Abwechslung.')
  else:
    print(
        '⚠️ Achtung: Die Dialoge ähneln sich thematisch stark (geringe'
        ' Varianz).'
    )


if __name__ == '__main__':
  # Passe den Dateinamen an deine generierte JSONL an
  analyze_variance('/data/nemo-fraud-detection/notebooks/01_Data_Generation/data/transcripts.jsonl')