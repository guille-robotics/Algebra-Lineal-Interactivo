import cv2
import numpy as np
import math

# ============================================================
# ROTACIÓN DE IMAGEN USANDO 3 SHEARS (MISMA LÓGICA QUE MATLAB)
# Código equivalente a:
#   - loop pixel a pixel
#   - coordenadas relativas al centro
#   - shear(angle, x, y) con round() en cada paso
#   - forward mapping (puede dejar "huecos")
# ============================================================


def shear(angle_rad: float, x: float, y: float):
    """
    Equivalente directo a tu función MATLAB:

    function [new_y, new_x] = shear(angle, x, y)
        tangent = tan(angle/2);
        new_x = round(x - y*tangent);
        new_y = y;
        new_y = round(new_x*sin(angle) + new_y);
        new_x = round(new_x - new_y*tangent);
    end

    Retorna (new_y, new_x) en ese orden, tal como MATLAB.
    """

    tangent = math.tan(angle_rad / 2.0)

    # ------------------------
    # Shear 1
    # ------------------------
    new_x = round(x - y * tangent)  # round() en esta etapa (como MATLAB)
    new_y = y                       # aquí NO hay round(), igual que MATLAB

    # ------------------------
    # Shear 2
    # ------------------------
    new_y = round(new_x * math.sin(angle_rad) + new_y)  # round() aquí también

    # ------------------------
    # Shear 3
    # ------------------------
    new_x = round(new_x - new_y * tangent)  # round() final

    return new_y, new_x


# ============================================================
# 1) LEER IMAGEN
# ============================================================

img = cv2.imread("bros.jpg")

# Validación por si el archivo no existe / ruta incorrecta
if img is None:
    raise FileNotFoundError("No se encontró 'bros.png' en la carpeta actual.")

# MATLAB: image = double(image)
img = img.astype(np.float64)

# ============================================================
# 2) ÁNGULO
# ============================================================

angle_deg = 45                      # el mismo valor que pusiste
angle = math.radians(angle_deg)     # MATLAB: deg2rad(angle_deg)

cosine = math.cos(angle)
sine = math.sin(angle)

# Dimensiones: (alto, ancho, canales)
height, width, channels = img.shape

# ============================================================
# 3) NUEVAS DIMENSIONES (misma fórmula que MATLAB)
# ============================================================

# MATLAB:
# new_height = round(abs(height*cosine) + abs(width*sine)) + 1;
# new_width  = round(abs(width*cosine)  + abs(height*sine)) + 1;
new_height = round(abs(height * cosine) + abs(width * sine)) + 1
new_width  = round(abs(width  * cosine) + abs(height * sine)) + 1

# Imagen de salida en negro (float64 por ahora)
output = np.zeros((new_height, new_width, channels), dtype=np.float64)

# ============================================================
# 4) CENTROS (idéntico a MATLAB)
# ============================================================

# MATLAB:
# original_centre_height = round(((height + 1)/2) - 1);
# original_centre_width  = round(((width  + 1)/2) - 1);
original_centre_height = round(((height + 1) / 2) - 1)
original_centre_width  = round(((width  + 1) / 2) - 1)

# MATLAB:
# new_centre_height = round(((new_height + 1)/2) - 1);
# new_centre_width  = round(((new_width  + 1)/2) - 1);
new_centre_height = round(((new_height + 1) / 2) - 1)
new_centre_width  = round(((new_width  + 1) / 2) - 1)

# ============================================================
# 5) ROTACIÓN PIXEL A PIXEL (FORWARD MAPPING)
# ============================================================

# En MATLAB el loop es:
# for i = 1:height
#   for j = 1:width
#
# Python va de 0 a height-1, por eso usamos (i+1) para replicar fórmulas
for i in range(height):
    for j in range(width):

        # ----------------------------------------------------
        # Coordenadas relativas al centro de la imagen original
        # ----------------------------------------------------
        # MATLAB:
        # y = height - i - original_centre_height;
        # x = width  - j - original_centre_width;
        #
        # Como MATLAB indexa desde 1, usamos (i+1) y (j+1)
        y = height - (i + 1) - original_centre_height
        x = width  - (j + 1) - original_centre_width

        # ----------------------------------------------------
        # Aplicar la función shear (la tuya, igualita)
        # ----------------------------------------------------
        new_y, new_x = shear(angle, x, y)

        # ----------------------------------------------------
        # Llevar coordenadas al sistema de la nueva imagen
        # ----------------------------------------------------
        # MATLAB:
        # new_y = new_centre_height - new_y;
        # new_x = new_centre_width  - new_x;
        new_y = new_centre_height - new_y
        new_x = new_centre_width  - new_x

        # En MATLAB, new_y y new_x ya quedan redondeados dentro de shear()
        # pero igual aquí los convertimos a int por seguridad
        new_y = int(new_y)
        new_x = int(new_x)

        # ----------------------------------------------------
        # Bounds check (adaptado a indexado Python)
        # ----------------------------------------------------
        # MATLAB chequea 1..N
        # Python chequea 0..N-1
        if 0 <= new_y < new_height and 0 <= new_x < new_width:
            output[new_y, new_x, :] = img[i, j, :]

# ============================================================
# 6) GUARDAR RESULTADO
# ============================================================

# MATLAB: output = uint8(output);
output = np.clip(output, 0, 255).astype(np.uint8)

# MATLAB: imwrite(output, 'rotated_image.png');
cv2.imwrite("rotated_image_bros.png", output)

print("✅ Listo: rotated_image_bros.png guardada.")
