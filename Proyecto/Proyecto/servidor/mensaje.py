from datetime import datetime

class mensaje:
    def __init__(self, remitente: str, destinatario: str, asunto: str, cuerpo: str,etiquetas=None, leido=False, timestamp=None, prioridad=0):
        self.remitente = remitente
        self.destinatario = destinatario
        self.asunto = asunto
        self.cuerpo = cuerpo
        self.etiquetas = etiquetas if etiquetas is not None else[]
        self.leido = leido
        self.timestamp = timestamp or datetime.now()
        self.traza_ruta = []
        self.prioridad = prioridad if prioridad is not None else 0
    def agregar_etiqueta(self, tag):
        t = tag.strip()
        if t and t.lower() not in [e.lower() for e in self.etiquetas]:
            self.etiquetas.append(t)
    def marcar_urgente(self):
        self.prioridad = 3
    def set_prioridad(self, n):
        if n in (0,1,2,3):
            self.prioridad = n
    def quitar_etiqueta(self, tag):
        self.etiquetas = [e for e in self.etiquetas if e.lower() != tag.lower()]
    def marcar_leido(self):
        self.leido = True
    def marcar_no_leido(self):
        self.leido = False
    def registrar_hop(self, servidor):
        self.traza_ruta.append(servidor)
    def resumen(self):
        return f"[prio {self.prioridad}] {self.asunto} (de {self.remitente})"