from servidor.usuarios import usuarios

class ServidorCorreo:
    def __init__(self):
        self.usuarios = {}

    def agregar_usuario(self, usuario: usuarios):
        self.usuarios[usuario.email] = usuario

RED = {
    "s1": ["s2", "s4"],
    "s2": ["s1", "s3"],
    "s3": ["s2"],
    "s4": ["s1"],
}

def camino_simple(origen, destino, visit=None):
    #usando recursividad ve cual es el mejor camino entre los 4 servidores
    if visit is None:
        visit = set()
    if origen == destino:
        return [destino]
    visit.add(origen)
    for v in RED.get(origen, []):
        if v not in visit:
            c = camino_simple(v, destino, visit)
            if c:
                return [origen] + c
    return None


def envio_mensaje(remitente, destinatario_email, asunto, cuerpo, srv_origen, srv_destino, servidores):
    from servidor.mensaje import mensaje
    ruta = camino_simple(srv_origen, srv_destino)
    if not ruta:
        print("Sin ruta en la red entre servidores")
        return
    print("Ruta:".join(ruta))

    dest_srv = servidores[srv_destino]
    u = dest_srv.usuarios.get(destinatario_email)
    if u:
        msg = mensaje(remitente.email, destinatario_email, asunto, cuerpo)
        u.recibir(msg)
        print("Mensaje entregado correctamente.")
    else:
        print("El destinatario no existe en el servidor destino.")


def envio_automatico(remitente, destinatario_email, asunto, cuerpo, servidores):
    srv_origen = next((nombre for nombre, srv in servidores.items()
                       if remitente.email in srv.usuarios), None)
    srv_destino = next((nombre for nombre, srv in servidores.items()
                        if destinatario_email in srv.usuarios), None)

    if not srv_origen or not srv_destino:
        print("No se encontró servidor de origen o destino")
        return

    envio_mensaje(remitente, destinatario_email, asunto, cuerpo,
                  srv_origen, srv_destino, servidores)
