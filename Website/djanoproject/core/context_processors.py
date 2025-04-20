import os
import json
from django.conf import settings

def vue_manifest(request):
    """
    Context processor to load Vue.js manifest file for templates
    """
    manifest_data = None
    manifest_path = os.path.join(settings.BASE_DIR, 'vue_dist', 'manifest.json')
    
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, 'r') as f:
                manifest_json = json.load(f)
                
            # Extract CSS and JS files
            css_files = []
            js_files = []
            
            for key, asset in manifest_json.items():
                if key.endswith('.css'):
                    css_files.append(asset['file'])
                elif key.endswith('.js'):
                    js_files.append(asset['file'])
            
            manifest_data = {
                'css': css_files,
                'js': js_files
            }
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading Vue manifest: {e}")
    
    return {
        'manifest': manifest_data
    } 