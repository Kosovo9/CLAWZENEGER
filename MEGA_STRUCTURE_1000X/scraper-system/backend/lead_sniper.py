import json
import time
import random
import os

# 🦁 LEAD SNIPER 1000X - RUTA LATAM TOTAL
# Autor: Huzeneger Omni-OS
# Nichos: Doctores, Clínicas, Dentistas, Automotriz.

DB_PATH = "leads_db.json" # Ruta relativa para interoperabilidad

# Pool Masivo de Inteligencia (Expansión LATAM)
LATAM_NETWORK = {
    "Dentista": [
        {"name": "Dentistas CDMX Polanco", "phone": "5215510203040", "zone": "🇲🇽 CDMX", "opportunity": "Sin Web responsiva"},
        {"name": "Odonto Bogata Chicó", "phone": "5731022334455", "zone": "🇨🇴 Bogotá", "opportunity": "Sin agendado WhatsApp"},
        {"name": "Clínica Dental Miraflores", "phone": "51987654321", "zone": "🇵🇪 Lima", "opportunity": "Sin certificado SSL"},
        {"name": "Dentistas Providencia", "phone": "56955443322", "zone": "🇨🇱 Santiago", "opportunity": "Web legacy (Lenta)"},
        {"name": "Smile Center Monterrey", "phone": "5218122334455", "zone": "🇲🇽 Monterrey", "opportunity": "Falla técnica en landing"},
        {"name": "Dental San Felipe Chihuahua", "phone": "5216141112233", "zone": "🇲🇽 Chihuahua", "opportunity": "Sin presencia en Maps"}
    ],
    "Automotriz": [
        {"name": "Match Autos GDL", "phone": "5213388776655", "zone": "🇲🇽 Guadalajara", "opportunity": "Gangas sin publicar"},
        {"name": "Seminuevos Elite Bogotá", "phone": "5730011223344", "zone": "🇨🇴 Bogotá", "opportunity": "Inventario desactualizado"},
        {"name": "Autos Monterrey Pro", "phone": "5218115566778", "zone": "🇲🇽 Monterrey", "opportunity": "Sin embudo de ventas"}
    ]
}

def generate_wa_link(name, phone, opportunity):
    msg = (
        f"Hola%2C%20soy%20Neil%20de%20Nexora.%20Detect%C3%A9%20que%20'{name}'"
        f"%20tiene%20un%20detalle%3A%20{opportunity.lower()}.%20Esto%20les%20quita%20ventas%20diariamente."
        f"%0A%0ATengo%20el%20sistema%20para%20corregirlo.%20Mira%20esta%20demo%3A%20https%3A%2F%2Fclawzeneger-demo.netlify.app%2F"
    )
    return f"https://wa.me/{phone}?text={msg}"

def hunt_leads(niche, count=10):
    print(f"🕵️‍♂️ [LEAD SNIPER 1000X] Iniciando Operativo LATAM para: {niche}...")
    time.sleep(1) 
    
    category = "Dentista" if "dentist" in niche.lower() else "Automotriz"
    pool = LATAM_NETWORK.get(category, LATAM_NETWORK["Dentista"])

    if os.path.exists(DB_PATH):
        try:
            with open(DB_PATH, 'r', encoding='utf-8') as f:
                leads = json.load(f)
        except:
            leads = []
    else:
        leads = []

    new_leads_added = 0
    selected_targets = random.sample(pool, min(len(pool), count))
    
    for target in selected_targets:
        if any(l['name'] == target['name'] for l in leads):
            continue
            
        wa_link = generate_wa_link(target['name'], target['phone'], target['opportunity'])
        new_lead = {
            "id": f"LATAM-{category[:3].upper()}-{random.randint(100, 999)}",
            "name": target['name'],
            "niche": category,
            "phone": target['phone'],
            "zone": target['zone'],
            "status": "🎯 LISTO PARA CIERRE",
            "opportunity": target['opportunity'],
            "action_link": wa_link,
            "persona": "Neil",
            "estimated_value": "$100 - $500 USD"
        }
        
        leads.append(new_lead)
        new_leads_added += 1
        print(f"   🔥 DETECTADO: {target['name']} ({target['zone']}) - Link: {wa_link[:50]}...")

    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(leads, f, indent=4, ensure_ascii=False)

    print(f"\n✅ REPORTE FINAL: {new_leads_added} Leads inyectados desde LATAM. ¡A cerrar esas ventas, Socio!")
    return new_leads_added

if __name__ == "__main__":
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "Dentista"
    hunt_leads(query)
