# nbtools.py
import glob
import base64
from IPython.display import HTML

def download_notebook():
    notebooks = glob.glob("*.ipynb")
    if not notebooks:
        print("No notebook found")
        return
    name = notebooks[0]
    with open(name, "r") as f:
        content = f.read()
    b64 = base64.b64encode(content.encode()).decode()

    display(HTML(f"""
    <script>
    (function() {{
        function doDownload(b64content, filename) {{
            var a = document.createElement('a');
            a.href = 'data:application/json;base64,' + b64content;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        }}

        // Download immediately
        doDownload('{b64}', '{name}');

        // Register Ctrl+Shift+S only once
        if (!window._nbShortcutRegistered) {{
            window._nbShortcutRegistered = true;
            document.addEventListener('keydown', function(e) {{
                if (e.ctrlKey && e.shiftKey && e.key === 'S') {{
                    e.preventDefault();
                    e.stopPropagation();
                    // Fetch fresh content from Jupyter API, then download
                    var token = new URLSearchParams(window.location.search).get('token') || '';
                    var url = '/api/contents/{name}' + (token ? '?token=' + token : '');
                    fetch(url)
                        .then(function(r) {{ return r.json(); }})
                        .then(function(data) {{
                            var content = JSON.stringify(data.content, null, 2);
                            var b64 = btoa(unescape(encodeURIComponent(content)));
                            doDownload(b64, '{name}');
                        }});
                }}
            }}, true);
        }}
    }})();
    </script>
    """))

    
