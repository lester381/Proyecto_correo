from servidor.servidor_correo import ServidorCorreo
from funciones import funciones_usuario
from servidor.usuarios import usuarios
from servidor.servidor_correo import envio_automatico
class menu:
    def __init__(self, fu, servidores):
        self.fu = fu
        self.servidores = servidores
        self.usuario_actual = None

    def menu_sesion(self):
        while not self.usuario_actual:
            print("Bienvenido al sistema de correo, ¿que desea hacer?")
            print("1) Iniciar sesión")
            print("2) Crear usuario")
            print("3) Lista de usuario")
            print("0) Salir")

            opcion = input("Opción: ")

            if opcion == "1":
                if not self.fu.usuarios:
                    print("\nSin usuarios registrados, crea uno antes de continuar")
                    continue
                usuario = self.fu.inicio_sesion()
                if usuario:
                    self.usuario_actual = usuario
            elif opcion == "2":
                self.fu.creacion_usuario()
            elif opcion == "3":
                self.fu.listar_usuarios()
            elif opcion == "0":
                exit()
            else:
                print("\nOpción inválida")

    def menu_principal(self):
        while True:
            if not self.usuario_actual:
                self.menu_sesion()

            print("1) Enviar mensaje")
            print("2) Ver bandeja")
            print("3) Crear subcarpeta")
            print("4) Mover mensaje a subcarpeta")
            print("5) Buscar bandeja")
            print("6) Ver mensajes de la carpeta")
            print("7) Cerrar sesión")
            print("8) reglas de ordenamiento")
            print("9) mensajes prioritarios")
            print("0) Salir\n")

            opcion = input("opcion: ")

            if opcion == "1":
                self.fu.enviar_desde_usuario(self.usuario_actual)
            elif opcion == "2":
                self.fu.ver_bandeja_completa(self.usuario_actual)
            elif opcion == "3":
                self.fu.crear_subcarpeta(self.usuario_actual)
            elif opcion == "4":
                self.fu.mover_mensaje(self.usuario_actual)
            elif opcion == "5":
                self.fu.buscar_mensajes(self.usuario_actual)
            elif opcion == "6":
                self.fu.ver_raiz(self.usuario_actual)
            elif opcion == "7":
                print(f"\nSesión de {self.usuario_actual.nombre} finalizada.")
                self.usuario_actual = self.fu.cerrar_sesion(self.usuario_actual)
            elif opcion == "8":
                self.menu_reglas()
            elif opcion == "9":
                self.menu_cola()
            elif opcion == "0":
                break
    
    def menu_reglas(self):
        if not self.usuario_actual:
            print("\nPrimero inicia sesion.");return
        
        while True:
            print("\n--- Reglas ---")
            print("1)Crear")
            print("2)listar")
            print("3)eliminar")
            print("0)volver")
            op =input("> ").strip()
        
            if op == "1":
                asunto = input("asunto contiene(enter omite) ").strip()
                remitente = input("remitente contiene (Enter omite): ").strip()
                tag    = input("tiene etiqueta (Enter omite): ").strip()
                mover  = input("mover a carpeta (Enter omite): ").strip()
                addt   = input("agregar etiqueta(s) (coma-sep, Enter omite): ").strip()
                prio   = input("prioridad (0-3, Enter omite): ").strip()
                leido  = input("marcar leído? (s/n, Enter omite): ").strip().lower()
                nombre = input("nombre de la regla (opcional): ").strip() or None
                stop   = input("detener tras aplicar? (s/n, default s): ").strip().lower() != "n"
            
                cond, acc = {}, {}
                if asunto: cond["asunto_contiene"] = asunto
                if remitente: cond["remitente_contiene"] = remitente
                if tag: cond["tiene_etiqueta"] = tag
                if mover: acc["mover"] = mover
                if addt:
                    tags = [t.strip()for t in addt.split(",")if t.strip()]
                    acc["agregar_etiqueta"] = tags if len(tags) >  1 else tags[0]
                if prio.isdigit() and int(prio) in (0,1,2,3): acc["prioridad"] = int(prio)
                if leido in ("s", "n"): acc["marcar_leido"] = (leido == "s")
            
                self.usuario_actual.agregar_regla(cond, acc, stop=stop, nombre=nombre)
            
            elif op == "2":
                reglas = self.usuario_actual.listar_reglas()
                if not reglas: print ("No hay reglas."); continue
                for i, r in enumerate(reglas):
                    print(f"[{i}] {r.get('nombre') or 'sin nombre'} | cond={r.get('accion')} | stop={r.get('stop')}")
            elif op == "3":
                idx = input("indice a eliminar: ").strip()
                print("✔ Eliminada." if (idx.isdigit() and self.usuario_actual.eliminar_regla(int(idx))) else "✖ Índice inválido.")
            elif op == "0":
                break
            else:
                print("opcion invalida.")
    def menu_cola(self):
        while True:
            print("\n---mensajes prioritarios---")
            print("1) Atender siguiente")
            print("2) Ver próximo")
            print("3) Tamaño de la cola")
            print("4) Vaciar cola")
            print("0) Volver")
            op = input("> ").strip()
            
            if op == "1":
                self.cola_atender()
            elif op == "2":
                self.cola_ver_proximo()
            elif op == "3":
                self.cola_tamaño()
            elif op == "4":
                self.cola_vaciar()
            elif op == "0":
                break
            else:
                print("Opcion invalida.")
    def cola_atender(self):
        msg = self.usuario_actual.siguiente()
        if not msg:
            print("\nNo hay mensaje en prioridad.")
            return
        print("\n== SIGUIENTE MENSAJE ==")
        print(msg.resumen() if hasattr(msg, "resumen") else f"{msg.asunto} (de {msg.remitente})")
        if hasattr(msg, "marcar_leido"):
            msg.marcar_leido()

    def cola_ver_proximo(self):
        msg = self.usuario_actual.ver_proximo()
        if not msg:
            print("\nNo hay mensajes en la cola.")
            return
        print("\n== PRÓXIMO EN COLA ==")
        print(msg.resumen() if hasattr(msg, "resumen") else f"{msg.asunto} (de {msg.remitente})")

    def cola_tamaño(self):
        print(f"\nMensajes en cola: {self.usuario_actual.tamaño_cola()}")

    def cola_vaciar(self):
        self.usuario_actual.vaciar_cola()
        print("\nCola vaciada.")

if __name__ == "__main__":
    servidores = {
        "s1": ServidorCorreo(),
        "s2": ServidorCorreo(),
        "s3": ServidorCorreo(),
        "s4": ServidorCorreo()
    }
    fu = funciones_usuario(servidores)  # pasa servidores al constructor
    u1 = usuarios("lean", "lean", "lean")
    u2 = usuarios("ian", "ian", "ian")
    u3 = usuarios("marcos", "marcos", "marcos")
    
    fu.usuarios.extend([u1,u2,u3])
    servidores["s1"].agregar_usuario(u1)
    servidores["s2"].agregar_usuario(u2)
    servidores["s3"].agregar_usuario(u3)
    
    envio_automatico(u1, "marcos", "Reunion", "Revisar", servidores)
    envio_automatico(u3, "marcos", "info",  "Agenda", servidores)
    envio_automatico(u2, "marcos", "Server", "notas", servidores)
    
    men = menu(fu, servidores)          # definí menu ANTES de instanciar
    men.menu_principal()
