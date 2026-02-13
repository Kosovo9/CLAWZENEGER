import requests
from bs4 import BeautifulSoup
import time
import json
import sys
import socket
from urllib.parse import urlparse

# 🦁 SEO GOD MODE - AUDITORÍA 1000X
# Autor: Huzeneger Omni-OS

def audit_seo(url):
    print(f"🦁 [SEO GOD] INICIANDO ESCANEO DE OBJETIVO: {url}...")
    start_time = time.time()
    
    try:
        # 1. CONEXIÓN Y VELOCIDAD
        response = requests.get(url, timeout=10)
        load_time = round(time.time() - start_time, 2)
        status_code = response.status_code
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 2. METADATOS CLAVE
        title = soup.title.string if soup.title else "❌ NO TITLE FOUND"
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc['content'] if meta_desc else "❌ NO META DESCRIPTION FOUND"
        
        # 3. ESTRUCTURA DE ENCABEZADOS
        h1_tags = [h1.get_text(strip=True) for h1 in soup.find_all('h1')]
        h2_count = len(soup.find_all('h2'))
        h3_count = len(soup.find_all('h3'))
        
        # 4. IMÁGENES Y ALT TEXT
        images = soup.find_all('img')
        images_missing_alt = [img['src'] for img in images if not img.get('alt')]
        
        # 5. ANÁLISIS DE SEGURIDAD BÁSICO (SSL)
        is_ssl = url.startswith('https')
        
        # 6. PALABRAS CLAVE (DENSIDAD SIMPLE)
        text = soup.get_text().lower()
        words = text.split()
        word_count = len(words)
        
        # 7. GENERAR REPORTE JSON
        report = {
            "target": url,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "performance": {
                "load_time_sec": load_time,
                "status_code": status_code,
                "server": response.headers.get('Server', 'Unknown')
            },
            "on_page_seo": {
                "title": title,
                "title_length": len(title),
                "meta_description": description,
                "meta_desc_length": len(description) if description != "❌ NO META DESCRIPTION FOUND" else 0,
                "h1_tags": h1_tags,
                "h1_status": "✅ OPTIMAL" if len(h1_tags) == 1 else "⚠️ CRITICAL: MULTIPLE OR MISSING H1",
                "h2_count": h2_count,
                "word_count": word_count
            },
            "technical_seo": {
                "ssl_secure": is_ssl,
                "images_total": len(images),
                "images_missing_alt": len(images_missing_alt),
                "robots_txt": f"{url.rstrip('/')}/robots.txt"
            },
            "god_mode_verdict": "🔥 SITE NEEDS OPTIMIZATION" if len(images_missing_alt) > 0 or len(h1_tags) != 1 else "💎 SOLID SEO FOUNDATION"
        }
        
        print("\n📊 REPORTE GENERADO:")
        print(json.dumps(report, indent=4, ensure_ascii=False))
        
        # GUARDAR EN DISCO
        filename = f"seo_report_{urlparse(url).netloc}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4, ensure_ascii=False)
        print(f"✅ Reporte guardado en: {filename}")
        
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {str(e)}")

# EJECUTAR SI SE LLAMA DESDE CONSOLA
if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_url = sys.argv[1]
    else:
        target_url = input("🔗 INGRESA URL OBJETIVO (ej: https://example.com): ")
    
    if not target_url.startswith('http'):
        target_url = 'https://' + target_url
        
    audit_seo(target_url)
