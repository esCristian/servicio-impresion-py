from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import subprocess
import PyPDF2
import sys
import threading

app = Flask(__name__)
CORS(app)

if getattr(sys, 'frozen', False):
    DIRECTORIO_PDFS = os.path.dirname(sys.executable)
else:
    DIRECTORIO_PDFS = os.path.dirname(os.path.abspath(__file__))

os.makedirs(DIRECTORIO_PDFS, exist_ok=True)

@app.route('/imprimir_pdf', methods=['POST'])
def imprimir_pdf():
    try:
        # Obtener el archivo remito y el nombre de la impresora de la solicitud
        remito = request.files.get('remito')
        nombre_impresora = request.form.get('nombre_impresora')

        if remito:
            # Guardar y validar el remito
            ruta_remito = guardar_pdf(remito, 'remito.pdf')
            if es_pdf_valido(ruta_remito):
                # Crear un hilo para manejar la impresión en segundo plano
                threading.Thread(target=imprimir_documento, args=(ruta_remito, nombre_impresora)).start()
            else:
                print(f"El archivo {ruta_remito} no es un PDF válido. Omite la impresión.")
            return jsonify({'mensaje': 'Remito procesado correctamente'}), 200
        else:
            return jsonify({'error': 'No se proporcionó el archivo remito'}), 400

    except Exception as e:
        print(f"Error al imprimir: {e}")
        return jsonify({'error': 'Error al imprimir'}), 500

def guardar_pdf(file, nombre_archivo):
    """ Guarda el PDF en el servidor y devuelve la ruta """
    ruta_completa = os.path.join(DIRECTORIO_PDFS, nombre_archivo)
    file.save(ruta_completa)
    print(f"Archivo guardado en: {ruta_completa}")
    return ruta_completa

def es_pdf_valido(ruta_pdf):
    """ Verifica si el PDF es válido """
    try:
        with open(ruta_pdf, "rb") as f:
            PyPDF2.PdfReader(f)
        return True
    except Exception:
        return False

def imprimir_documento(ruta_pdf, nombre_impresora):
    """ Imprime el documento PDF usando pdftoprinter """
    try:
        comando = [
            'pdftoprinter.exe',
            ruta_pdf,
            nombre_impresora
        ]
        subprocess.run(comando, check=True)
        print(f"Impresión enviada a {nombre_impresora}: {ruta_pdf}")
    except subprocess.CalledProcessError as e:
        print(f"Error al imprimir: {e}")

@app.route('/', methods=['GET'])
def index():
    return "Servidor de impresión en ejecución", 200

if __name__ == '__main__':
    app.run(debug=True, port=3000)




# Funciona pero sin hilos
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# import subprocess
# import PyPDF2
# import sys

# app = Flask(__name__)
# CORS(app)

# # Obtiene la ruta del directorio actual o del ejecutable si está compilado
# if getattr(sys, 'frozen', False):
#     DIRECTORIO_PDFS = os.path.dirname(sys.executable)  # En el ejecutable compilado
# else:
#     DIRECTORIO_PDFS = os.path.dirname(os.path.abspath(__file__))  # En entorno de desarrollo

# # Asegúrate de que el directorio exista
# os.makedirs(DIRECTORIO_PDFS, exist_ok=True)

# # Imprime la ruta del directorio donde se guardarán los PDFs para verificar
# print(f"Directorio de almacenamiento de PDFs: {DIRECTORIO_PDFS}")

# @app.route('/imprimir_pdf', methods=['POST'])
# def imprimir_pdf():
#     try:
#         # Obtener el archivo remito y el nombre de la impresora de la solicitud
#         remito = request.files.get('remito')
#         nombre_impresora = request.form.get('nombre_impresora')  # Obtener el nombre de la impresora

#         if remito:
#             # Guardar y validar el remito
#             ruta_remito = guardar_pdf(remito, 'remito.pdf')
#             if es_pdf_valido(ruta_remito):
#                 # Imprimir utilizando el nombre de la impresora proporcionado
#                 imprimir_documento(ruta_remito, nombre_impresora)  # Usa el nombre de la impresora enviado
#             else:
#                 print(f"El archivo {ruta_remito} no es un PDF válido. Omite la impresión.")
#             return jsonify({'mensaje': 'Remito procesado correctamente'}), 200
#         else:
#             return jsonify({'error': 'No se proporcionó el archivo remito'}), 400

#     except Exception as e:
#         print(f"Error al imprimir: {e}")
#         return jsonify({'error': 'Error al imprimir'}), 500

# def guardar_pdf(file, nombre_archivo):
#     """ Guarda el PDF en el servidor y devuelve la ruta """
#     ruta_completa = os.path.join(DIRECTORIO_PDFS, nombre_archivo)
#     file.save(ruta_completa)
#     # Confirmación de guardado
#     print(f"Archivo guardado en: {ruta_completa}")
#     return ruta_completa

# def es_pdf_valido(ruta_pdf):
#     """ Verifica si el PDF es válido """
#     try:
#         with open(ruta_pdf, "rb") as f:
#             PyPDF2.PdfReader(f)
#         return True
#     except Exception:
#         return False

# def imprimir_documento(ruta_pdf, nombre_impresora):
#     """ Imprime el documento PDF usando pdftoprinter """
#     try:
#         # Comando de impresión
#         comando = [
#             'pdftoprinter.exe',  # Asegúrate de que este ejecutable esté en el PATH o en la misma carpeta que este script
#             ruta_pdf,
#             nombre_impresora
#         ]
#         # Mensaje de depuración antes de ejecutar el comando
#         print(f"Ejecutando comando de impresión: {' '.join(comando)}")
#         subprocess.run(comando, check=True)
#         print(f"Impresión enviada a {nombre_impresora}: {ruta_pdf}")
#     except subprocess.CalledProcessError as e:
#         print(f"Error al imprimir: {e}")

# @app.route('/', methods=['GET'])
# def index():
#     return "Servidor de impresión en ejecución", 200

# if __name__ == '__main__':
#     app.run(debug=True, port=3000)

# funciona
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import os
# import subprocess
# import PyPDF2  # Para validar PDF

# app = Flask(__name__)
# CORS(app)

# # Directorio donde se guardarán los PDFs
# DIRECTORIO_PDFS = 'C:\\Users\\Administrador\\Documents\\print-service'  # Cambia esta ruta a donde quieras guardar los PDFs

# # Asegúrate de que el directorio exista
# os.makedirs(DIRECTORIO_PDFS, exist_ok=True)

# @app.route('/imprimir_pdf', methods=['POST'])
# def imprimir_pdf():
#     try:
#         # Obtener los archivos de la solicitud
#         etiqueta = request.files.get('etiqueta')
#         remito = request.files.get('remito')

#         # Imprimir etiqueta si se proporciona
#         if etiqueta:
#             ruta_etiqueta = guardar_pdf(etiqueta, 'etiqueta.pdf')  # Guarda como etiqueta.pdf
#             if es_pdf_valido(ruta_etiqueta):
#                 imprimir_documento(ruta_etiqueta, 'L3150-Red')  # Cambia el nombre de la impresora según sea necesario
#             else:
#                 print(f"El archivo {ruta_etiqueta} no es un PDF válido. Omite la impresión.")

#         # Imprimir remito si se proporciona
#         if remito:
#             ruta_remito = guardar_pdf(remito, 'remito.pdf')  # Guarda como remito.pdf
#             if es_pdf_valido(ruta_remito):
#                 imprimir_documento(ruta_remito, 'L375-Red')  # Cambia el nombre de la impresora según sea necesario
#             else:
#                 print(f"El archivo {ruta_remito} no es un PDF válido. Omite la impresión.")

#         return jsonify({'mensaje': 'Documentos procesados correctamente'}), 200

#     except Exception as e:
#         print(f"Error al imprimir: {e}")
#         return jsonify({'error': 'Error al imprimir'}), 500

# def guardar_pdf(file, nombre_archivo):
#     """ Guarda el PDF en el servidor y devuelve la ruta """
#     ruta_completa = os.path.join(DIRECTORIO_PDFS, nombre_archivo)
#     file.save(ruta_completa)  # Guarda el archivo en el servidor
#     print(f"Archivo guardado en: {ruta_completa}")  # Para depuración
#     return ruta_completa

# def es_pdf_valido(ruta_pdf):
#     """ Verifica si el PDF es válido """
#     try:
#         with open(ruta_pdf, "rb") as f:
#             PyPDF2.PdfReader(f)  # Intenta leer el PDF
#         return True
#     except Exception:
#         return False

# def imprimir_documento(ruta_pdf, nombre_impresora):
#     """ Imprime el documento PDF usando pdftoprinter """
#     try:
#         # Comando para imprimir el PDF
#         comando = [
#             'pdftoprinter.exe',  # Asegúrate de que este ejecutable esté en tu PATH
#             ruta_pdf,
#             nombre_impresora
#         ]

#         # Ejecutar el comando
#         subprocess.run(comando, check=True)
#         print(f"Impresión enviada a {nombre_impresora}: {ruta_pdf}")

#     except subprocess.CalledProcessError as e:
#         print(f"Error al imprimir: {e}")

# @app.route('/', methods=['GET'])
# def index():
#     return "Servidor de impresión en ejecución", 200

# if __name__ == '__main__':
#     app.run(debug=True, port=3000)


# Este codigo funciona pero solo puede recibir dos pdf
# import os
# import subprocess
# from flask import Flask, request, jsonify
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# # Directorio donde se guardarán los PDFs
# DIRECTORIO_PDFS = 'C:\\Users\\Administrador\\Documents\\print-service'  # Cambia esta ruta a donde quieras guardar los PDFs

# # Asegúrate de que el directorio exista
# os.makedirs(DIRECTORIO_PDFS, exist_ok=True)

# @app.route('/imprimir_pdf', methods=['POST'])
# def imprimir_pdf():
#     try:
#         # Obtener los archivos de la solicitud
#         etiqueta = request.files.get('etiqueta')
#         remito = request.files.get('remito')

#         if etiqueta:
#             ruta_etiqueta = guardar_pdf(etiqueta, 'etiqueta.pdf')  # Guarda como etiqueta.pdf
#             imprimir_documento(ruta_etiqueta, 'L3150-Red')  # Cambia el nombre de la impresora según sea necesario

#         if remito:
#             ruta_remito = guardar_pdf(remito, 'remito.pdf')  # Guarda como remito.pdf
#             imprimir_documento(ruta_remito, 'L375-Red')  # Cambia el nombre de la impresora según sea necesario

#         return jsonify({'mensaje': 'Documentos impresos correctamente'}), 200

#     except Exception as e:
#         print(f"Error al imprimir: {e}")
#         return jsonify({'error': 'Error al imprimir'}), 500

# def guardar_pdf(file, nombre_archivo):
#     """ Guarda el PDF en el servidor y devuelve la ruta """
#     ruta_completa = os.path.join(DIRECTORIO_PDFS, nombre_archivo)
#     file.save(ruta_completa)  # Guarda el archivo en el servidor
#     print(f"Archivo guardado en: {ruta_completa}")  # Para depuración
#     return ruta_completa

# def imprimir_documento(ruta_pdf, nombre_impresora):
#     try:
#         # Ruta del ejecutable de PDFtoPrinter
#         pdftoprinter_path = "C:\\Users\\Administrador\\Documents\\print-service\\PDFtoPrinter.exe"  # Cambia esto a la ruta de tu PDFtoPrinter.exe

#         # Comando para imprimir usando PDFtoPrinter
#         comando = [pdftoprinter_path, ruta_pdf, nombre_impresora]
        
#         # Ejecutar el comando
#         subprocess.run(comando, check=True)
#         print(f"Impresión enviada a {nombre_impresora}: {ruta_pdf}")

#     except subprocess.CalledProcessError as e:
#         print(f"Error al imprimir: {e}")

# @app.route('/', methods=['GET'])
# def index():
#     return "Servidor de impresión en ejecución", 200

# if __name__ == '__main__':
#     app.run(debug=True, port=3000)














