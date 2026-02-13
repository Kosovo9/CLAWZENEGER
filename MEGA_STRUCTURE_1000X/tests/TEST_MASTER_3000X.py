# tests/TEST_MASTER_3000X.py

import asyncio
import subprocess
import os
import sys

TESTS = [
    "TEST_CEREBRO_3000.py",
    "TEST_MEMORIA_RAG.py",
    "TEST_VOZ_JOANNA.py",
    "TEST_SEGURIDAD_JWT.py"
]

async def run_master_suite():
    print("INICIANDO SUITE MAESTRA SYNAPTIC 3000X")
    print("="*50)
    
    results = {}
    
    for test in TESTS:
        print(f"EJECUTANDO: {test}")
        try:
            # Ejecutar el script y capturar salida
            process = subprocess.run([sys.executable, f"tests/{test}"], capture_output=True, text=True, timeout=60)
            
            if process.returncode == 0:
                print(f"OK: {test} COMPLETADO CON EXITO")
                results[test] = "PASSED"
            else:
                print(f"FALLO: {test}")
                print(process.stderr)
                results[test] = "FAILED"
        except Exception as e:
            print(f"ERROR EJECUTANDO {test}: {e}")
            results[test] = "ERROR"

    print("\n" + "="*50)
    print("REPORTE FINAL DE CALIBRE 3000")
    print("="*50)
    for test, status in results.items():
        icon = "[OK]" if status == "PASSED" else "[FAIL]"
        print(f"{icon} {test:25} : {status}")
    print("="*50)
    
    if all(s == "PASSED" for s in results.values()):
        print("SISTEMA JOANNA 3000 LISTO PARA DESPLIEGUE GLOBAL")
    else:
        print("REVISAR MODULOS FALLIDOS ANTES DE LA ENTREGA AL SOCIO")

if __name__ == "__main__":
    asyncio.run(run_master_suite())
