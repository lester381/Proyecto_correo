from servidor.mensaje import mensaje
from servidor.usuarios import usuarios
from servidor.servidor_correo import envio_automatico


class funciones_usuario:
    def __init__(self,servidores=None):
        self.usuarios = []
        self.servidores = servidores

    def inicio_sesion(self):
        correo = input("Ingresa tu correo: ")
        contraseña = input("Ingresa tu contraseña: ")

        for u in self.usuarios:
            if u.email == correo and u.existente(contraseña):
                print("\n¡Bienvenido al sistema de correos!\n")
                return u
        print("\nUsuario o contraseña incorrectos.\n")
        return None

    def creacion_usuario(self):
        nombre = input("Nombre de usuario: ")
        contraseña = input("Ingresa tu contraseña: ")
        email = input("Ingresa tu correo: ")

        servidor_destino = input("Servidor donde registrar (s1, s2, s3, s4): ").strip()
        if servidor_destino not in self.servidores:
            print("Servidor inexistente, se usará s1 por defecto.")
            servidor_destino = "s1"

        for u in self.usuarios:
            if u.nombre == nombre:
                print("\nUsuario ya existente, probá con otro correo\n")
                return

        nuevo_usuario = usuarios(nombre, contraseña, email)
        self.usuarios.append(nuevo_usuario)

        self.servidores[servidor_destino].agregar_usuario(nuevo_usuario)
        print(f"\n{nombre} fue registrado en el servidor {servidor_destino} correctamente.\n")

    def listar_usuarios(self):
        if not self.usuarios:
            print("\nSin usuarios registrados.\n")
        else:
            print("\nUsuarios registrados:")
            for u in self.usuarios:
                print(f"{u.nombre} ({u.email})")

    def enviar_desde_usuario(self, remitente):
        destinatario_email = input("Correo del destinatario: ")
        asunto = input("Asunto: ")
        cuerpo = input("Cuerpo del mensaje: ")

        destinatario = None
        for u in self.usuarios:
            if u.email == destinatario_email:
                destinatario = u
                break

        if destinatario:
            msg = mensaje(remitente.email, destinatario_email, asunto, cuerpo)
            destinatario.recibir(msg)
            print("\nMensaje enviado correctamente.")
        else:
            print("\nDestinatario inexistente.")

    def ver_bandeja_completa(self, usuario):
        def mostrar(carpeta, nivel=0):
            espacio = "  " * nivel
            print(f"\n{espacio} {carpeta.nombre}")
            if not carpeta.mensajes:
                print(f"{espacio}  (Sin mensajes)")
            else:
                for msg in carpeta.mensajes:
                    print(f"{espacio}     Asunto: {msg.asunto}")
                    print(f"{espacio}     De: {msg.remitente}")
                    print(f"{espacio}     Cuerpo: {msg.cuerpo}\n")
            for sub in carpeta.subcarpetas:
                mostrar(sub, nivel + 1)
        usuario.bandeja.orden_prioridad()
        print("\n Bandeja de entrada:")
        mostrar(usuario.bandeja)

    def crear_subcarpeta(self, usuario):
        nombre = input("Nombre de la nueva subcarpeta: ").strip()
        if not nombre:
            print("Nombre vacío")
        else:
            sub = usuario.bandeja.agregar_subcarpeta(nombre)
            if sub:
                print(f"Subcarpeta '{sub.nombre}' creada.")

    def mover_mensaje(self, usuario):
        mensajes = usuario.bandeja.mensajes
        if not mensajes:
            print("No hay mensajes en la carpeta.")
            return

        print("\nMensajes en carpeta:")
        for i, m in enumerate(mensajes, start=1):
            print(f"{i}) {m.asunto} (De: {m.remitente})")

        try:
            idx = int(input("Elegí el número de mensaje a mover: "))
            if idx < 1 or idx > len(mensajes):
                print("Índice inválido")
                return
            msg = mensajes[idx - 1]
            destino_nombre = input("Nombre de la subcarpeta destino: ").strip()
            destino = usuario.bandeja.obtener_subcarpeta(destino_nombre)
            if not destino:
                print("La subcarpeta no existe.")
            else:
                if usuario.bandeja.mover_mensaje(msg, destino):
                    print(f"Mensaje movido a '{destino.nombre}'.")
                else:
                    print("No se pudo mover el mensaje.")
        except ValueError:
            print("Debes ingresar un número.")

    def buscar_mensajes(self, usuario):
        asunto = input("Filtrar por asunto: ").strip()
        remit = input("Filtrar por remitente: ").strip()
        if asunto == "": asunto = None
        if remit == "": remit = None
        resultados = usuario.bandeja.buscar(asunto=asunto, remitente=remit)
        if not resultados:
            print("\nSin coincidencias.")
        else:
            print(f"\nResultados ({len(resultados)}):")
            for m in resultados:
                print(f"- {m.asunto}  (De: {m.remitente})")

    def ver_raiz(self, usuario):
        mensajes = usuario.bandeja.mensajes
        if not mensajes:
            print("\nBandeja (raíz) vacía.")
        else:
            print("\nMensajes en la carpeta raíz:")
            for m in mensajes:
                print(f"Asunto: {m.asunto}\nCuerpo: {m.cuerpo}\n")

    def cerrar_sesion(self, usuario):
        print(f"\nSesión de {usuario.nombre} finalizada.")
        return None
