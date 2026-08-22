from nemo_curator.stages.text.deduplication.semantic import (
    TextSemanticDeduplicationWorkflow,
)


def run_nemo_analysis(file_path: str):
  print('--- STARTE NVIDIA NEMO CURATOR SEMANTISCHE ANALYSE ---')

  # Offizieller Workflow von NVIDIA NeMo Curator
  workflow = TextSemanticDeduplicationWorkflow(
      input_path=file_path,
      output_path='./nemo_analysis_output',
      cache_path='./nemo_sem_cache',
      text_field='text',
      input_filetype='jsonl',
      n_clusters=50,
      eps=0.85,  # Ähnlichkeitsschwelle für semantische Duplikate
      perform_removal=False,  # WICHTIG: Es wird absolut nichts gelöscht!
      assign_id=True,
  )

  # Startet die Ausführung im Container (nutzt cuDF und vLLM auf der GPU)
  result = workflow.run()

  print('\n--- NVIDIA ANALYSE-ERGEBNIS AUF DER KONSOLE ---')
  if hasattr(result, 'metadata') and result.metadata:
    for key, value in result.metadata.items():
      print(f' {key}: {value}')
  else:
    print('Analyse erfolgreich auf der GPU durchgelaufen.')
    print(
        'Detaillierte Reports wurden im Verzeichnis "./nemo_analysis_output"'
        ' hinterlegt.'
    )


if __name__ == '__main__':
  # Passe den Pfad zu deiner JSONL-Datei an
  run_nemo_analysis('/data/nemo-fraud-detection/notebooks/01_Data_Generation/data/transcripts.jsonl')