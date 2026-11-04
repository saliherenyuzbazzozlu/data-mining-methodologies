"""Execute the notebooks in isolated kernels, preserving results in each notebook."""
from pathlib import Path
import sys
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

root = Path(__file__).resolve().parent
for project in sys.argv[1:] or ['crisp_dm', 'semma', 'kdd']:
    if project not in ['crisp_dm', 'semma', 'kdd']:
        raise ValueError('Unknown project')
    path = root / project / 'analysis.ipynb'
    notebook = nbformat.read(path, as_version=4)
    manager = KernelManager(kernel_name='python3')
    manager.kernel_spec.argv[0] = sys.executable
    print('Running', project, flush=True)
    try:
        NotebookClient(notebook, km=manager, timeout=900,
                       resources={'metadata': {'path': str(path.parent)}},
                       allow_errors=False).execute()
    finally:
        nbformat.write(notebook, path)
        if manager.has_kernel:
            manager.shutdown_kernel(now=True)
    print('Completed', project, flush=True)
