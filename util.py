from IPython.display import Javascript

def download_notebook():
    display(Javascript("""
    var notebook = Jupyter.notebook.toJSON();
    var blob = new Blob([JSON.stringify(notebook, null, 2)], 
                        {type: 'application/json'});
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = Jupyter.notebook.notebook_name;
    a.click();
    URL.revokeObjectURL(url);
    """))

# download_notebook()
