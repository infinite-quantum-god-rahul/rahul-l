#!/usr/bin/env python3
"""
Simple script to prepare files for Render.com deployment
"""
import os
import shutil
import zipfile
from pathlib import Path

def create_deployment_package():
    """Create a deployment package with essential files"""
    
    # Essential files for deployment
    essential_files = [
        'requirements.txt',
        'render.yaml', 
        'Procfile',
        'build.sh',
        'spoorthi_macs/settings_production.py',
        'RENDER_DEPLOYMENT_GUIDE.md',
        'DEPLOYMENT_COMPLETE_GUIDE.md',
        'companies/forms.py',
        'companies/forms_spec.py', 
        'companies/views.py',
        'companies/templates/companies/grid_list.html',
        'companies/templates/companies/single_grid.html',
        'companies/templates/companies/minimal_grid.html',
        'companies/templates/companies/simple_grid.html',
        'test_edit_fix.html',
        'EDIT_FIELDS_FIX_SUMMARY.md',
        'FORM_FIXES_SUMMARY.md'
    ]
    
    # Create deployment directory
    deploy_dir = Path('deployment_package')
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()
    
    print("🚀 Creating deployment package...")
    
    # Copy essential files
    for file_path in essential_files:
        src = Path(file_path)
        if src.exists():
            dst = deploy_dir / file_path
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"✅ Copied: {file_path}")
        else:
            print(f"⚠️  Missing: {file_path}")
    
    # Copy entire companies directory structure
    companies_src = Path('companies')
    companies_dst = deploy_dir / 'companies'
    if companies_src.exists():
        shutil.copytree(companies_src, companies_dst, dirs_exist_ok=True)
        print("✅ Copied: companies/ directory")
    
    # Copy spoorthi_macs directory
    spoorthi_src = Path('spoorthi_macs')
    spoorthi_dst = deploy_dir / 'spoorthi_macs'
    if spoorthi_src.exists():
        shutil.copytree(spoorthi_src, spoorthi_dst, dirs_exist_ok=True)
        print("✅ Copied: spoorthi_macs/ directory")
    
    # Copy templates directory
    templates_src = Path('templates')
    templates_dst = deploy_dir / 'templates'
    if templates_src.exists():
        shutil.copytree(templates_src, templates_dst, dirs_exist_ok=True)
        print("✅ Copied: templates/ directory")
    
    # Copy static files
    static_src = Path('staticfiles')
    static_dst = deploy_dir / 'staticfiles'
    if static_src.exists():
        shutil.copytree(static_src, static_dst, dirs_exist_ok=True)
        print("✅ Copied: staticfiles/ directory")
    
    # Create zip file
    zip_path = 'sml87_deployment_ready.zip'
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(deploy_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(deploy_dir)
                zipf.write(file_path, arcname)
    
    print(f"🎉 Deployment package created: {zip_path}")
    print(f"📁 Package size: {os.path.getsize(zip_path) / 1024 / 1024:.1f} MB")
    
    # Clean up
    shutil.rmtree(deploy_dir)
    
    return zip_path

if __name__ == "__main__":
    create_deployment_package()
