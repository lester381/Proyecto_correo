from servidor.carpeta import carpeta
from servidor.mensaje import mensaje

class usuarios:
    def __init__(self, nombre: str, contraseña: str, email: str):
        self.nombre = nombre
        self.__contraseña = contraseña
        self.email = email
        self.reglas = []
        self.cola = []
        self.bandeja = carpeta("Bandeja de entrada")
    def clave_prioridad(self, msg):
        prio = getattr(msg, "prioridad", 0)
        ts = getattr(msg, "timestamp", None)
        if ts is not None:
            try:
                ts = ts.timestamp()
            except AttributeError:
                pass
        if ts is None:
            ts = 0
        return (-prio, -ts)
    def encolar(self,msg):
        import heapq
        k1, k2 = self.clave_prioridad(msg)
        heapq.heappush(self.cola, (k1, k2, msg))
    def siguiente(self):
        import heapq
        if not self.cola:
            return None
        _, _, msg = heapq.heappop(self.cola)
        return msg
    def ver_proximo(self):
        if not self.cola:
            return None
        _, _, msg =self.cola[0]
        return msg
    def tamaño_cola(self):
        return len(self.cola)
    def vaciar_cola(self):
        self.cola.clear()
    def agregar_regla(self, condicion, accion, stop = True, nombre: str | None = None):
        self.reglas.append({"nombre": nombre, "condicion":condicion or {}, "accion": accion or {}, "stop": stop})
    def listar_reglas(self):
        return self.reglas
    def eliminar_regla(self, idx):
        if 0<=idx < len(self.reglas):
            self.reglas.pop(idx)
            return True
        return False
    
    def existente(self, contraseña: str):
        return self.__contraseña == contraseña

    def recibir(self, msg: mensaje):
        destino = self.bandeja
        def set_destino(carpeta_nueva):
            nonlocal destino
            destino = carpeta_nueva
        for regla in self.reglas:
            if self._matchea(msg, regla.get("condicion",{})):
                self._ejecutar_accion(msg, regla.get("accion", {}),out_destino = set_destino)
                if regla.get("stop",True):
                    break
        self.bandeja.agregar_mensaje(msg)
        self.encolar(msg)
    def _matchea(self, msg: mensaje, condicion):
        if not condicion:
            return True
        asunto = (getattr(msg, "asunto", "")or "").lower()
        remitente = (getattr(msg, "remitente", "")or "").lower()
        etiquetas = [e.lower() for e in getattr(msg, "etiquetas", [])]
        valor = condicion.get("asunto_contiene")
        if valor is not None and (valor.strip().lower() not in asunto):
            return False
        valor = condicion.get("remitente_contiene")
        if valor is not None and(valor.strip().lower() not in remitente):
            return False
        valor == condicion.get("tiene_etiqueta")
        if valor is not None and (valor.strip().lower() not in etiquetas):
            return False
        return True
    def ejecutar_accion(self, msg : mensaje, accion, out_destino):
        if not accion:
            return
        nombre_carpeta = accion.get("mover")
        if nombre_carpeta:
            sub = self.obtener_o_crear_subcarpeta(self.bandeja, nombre_carpeta)
            out_destino(sub)
        add_tag= accion.get("agregar_etiqueta")
        if add_tag:
            if (add_tag):
                msg.agregar_etiqueta(add_tag)
            else:
                for t in add_tag:
                    msg.agregar_etiqueta(t)
        rm_tag = accion.get("quitar_etiqueta")
        if rm_tag:
            if (rm_tag):
                msg.quitar_etiqueta(rm_tag)
            else:
                for t in rm_tag:
                    msg.quitar_etiqueta(t)
        if "prioridad" in accion:
            prio = accion.get("prioridad")
            if hasattr(msg, "set_prioridad"):
                msg.set_prioridad(prio)
            else:
                if prio in (0, 1, 2, 3):
                    msg.prioridad = prio
        if "marcar_leido" in accion:
            if accion["marcar_leido"]:
                msg.marcar_leido()
            else:
                msg.marcar_no_leido()
    def obtener_o_crear_subcarpeta(self, raiz: carpeta, nombre) -> carpeta:
        nom = (nombre or "").strip()
        sub = raiz.obtener_subcarpeta(nom)
        if not sub:
            sub = raiz.agregar_subcarpeta(nom)
        return sub
    def listar(self):
        return self.bandeja
