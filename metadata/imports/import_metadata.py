from metadata.imports import import_sessions, \
    import_files, import_participants, import_monitor, import_corpus


def _import_metadata(files):
    if 'corpus_file' in files:
        corpus_file = files['corpus_file']
        import_corpus.import_corpus(corpus_file)

    if 'participants_file' in files:
        participants_file = files['participants_file']
        import_participants.import_participants(participants_file)

    if 'sessions_file' in files:
        sessions_file = files['sessions_file']
        import_sessions.import_sessions(sessions_file)

    if 'monitor_file' in files:
        monitor_file = files['monitor_file']
        import_monitor.import_monitor(monitor_file)

    if 'files_file' in files:
        files_file = files['files_file']
        import_files.import_files(files_file)


def import_metadata(files):
    files_str = {f: files[f].read().decode() for f in files}
    _import_metadata(files_str)
