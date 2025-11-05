class carpeta:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mensajes = []
        self.subcarpetas = []

    def agregar_subcarpeta(self, nombre): 
        nombre_normal = nombre.strip()
        if not nombre_normal:
            print("Nombre de subcarpeta vacío")
            return None
        for sub in self.subcarpetas:
            if sub.nombre.lower() == nombre_normal.lower():
                return sub
        nueva = carpeta(nombre_normal)
        self.subcarpetas.append(nueva)
        return nueva

    def obtener_subcarpeta(self, nombre):
        nombre_normal = nombre.strip()
        for sub in self.subcarpetas:
            if sub.nombre.lower() == nombre_normal.lower():
                return sub
        return None

    def eliminar_subcarpeta(self, nombre):
        nombre_normal = nombre.strip()
        for i, sub in enumerate(self.subcarpetas):
            if sub.nombre.lower() == nombre_normal.lower():
                self.subcarpetas.pop(i)
                return True
        return False

    def agregar_mensaje(self, msg):
        self.mensajes.append(msg)

    def eliminar_mensaje(self, msg):
        if msg in self.mensajes:
            self.mensajes.remove(msg)
            return True
        return False

    def mover_mensaje(self, msg, destino):
        if self.eliminar_mensaje(msg):
            destino.agregar_mensaje(msg)
            return True
        return False

    def buscar(self, asunto=None, remitente=None):
        resultados = []
        asun = asunto.lower() if asunto else None
        rem = remitente.lower() if remitente else None
        for msg in self.mensajes:
            coincide = True
            if asun is not None and asun not in msg.asunto.lower():
                coincide = False
            if rem is not None and rem not in msg.remitente.lower():
                coincide = False
            if coincide:
                resultados.append(msg)
        for sub in self.subcarpetas:
            resultados.extend(sub.buscar(asunto, remitente))
        return resultados

    def listar(self, nivel=0):
        print((" " * nivel) + self.nombre)
        for sub in self.subcarpetas:
            sub.listar(nivel + 1)

    def orden_prioridad(self):
        prioridad_1 = ["urgente", "emergencia", "server"]
        prioridad_2 = ["reunion", "aviso", "cliente"]
        prioridad_3 = ["info", "recordatorio", "cuando puedas"]

        for msg in self.mensajes:
            asunto = msg.asunto.lower()
            prioridad = 0

            for palabra in prioridad_1:
                if palabra in asunto:
                    prioridad = 3
                    break;
            for palabra in prioridad_2:
                if palabra in asunto:
                    prioridad = 2
                    break;
            for palabra in prioridad_3:
                if palabra in asunto:
                    prioridad = 1
                    break;
            msg.prioridad = prioridad
        self.mensajes.sort(key=lambda m: m.prioridad, reverse=True)
        print("\n--- Después de ordenar ---")
        for m in self.mensajes:
            print(m.asunto, m.prioridad)

    
        
        


        





    