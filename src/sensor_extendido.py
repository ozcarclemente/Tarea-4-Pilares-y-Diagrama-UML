from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from statistics import mean
from typing import Protocol, List, Dict



class Notificador(Protocol):
    def enviar(self, mensaje: str) -> None: ...


class NotificadorEmail:
    def __init__(self, destinatario: str) -> None:
        self._destinatario = destinatario # encapsulado

    def enviar(self, mensaje: str) -> None:
        print(f"[EMAIL a {self._destinatario}] {mensaje}")


class NotificadorWebhook:
    def __init__(self, url: str) -> None:
         self._url = url
    
    def enviar(self, mensaje: str) -> None:
        print(f"[WEBHOOK {self._url}] {mensaje}")



@dataclass
class Sensor(ABC):
    id: str
    ventana: int = 5
    _calibracion: float = field(default=0.0, repr=False) # encapsulado
    _buffer: list[float] = field(default_factory=list, repr=False)

    def leer(self, valor: float) -> None:
        """Agrega lectura aplicando calibración y mantiene ventana móvil."""
        v = valor + self._calibracion
        self._buffer.append(v)
        if len(self._buffer) > self.ventana:
            self._buffer.pop(0)

    @property
    def promedio(self) -> float:
        return mean(self._buffer) if self._buffer else 0.0 # Encapsulamiento

    @abstractmethod
    def en_alerta(self) -> bool: ...


@dataclass
class SensorTemperatura(Sensor):
    umbral: float = 80.0
    def en_alerta(self) -> bool:
        # Polimorfismo: cada sensor define su propia condición
        return self.promedio >= self.umbral


@dataclass
class SensorVibracion(Sensor):
    rms_umbral: float = 2.5
    def en_alerta(self) -> bool:
    # Ejemplo tonto de RMS ~ promedio absoluto
        return abs(self.promedio) >= self.rms_umbral



# ========================
# Elementos agregados
# ========================

class NotificadorSMS:
    def __init__(self, numeroTelefono: str) -> None:
        self._numeroTelefono = numeroTelefono

    def enviar(self, mensaje: str) -> None:
        print(f"[SMS a {self._numeroTelefono}] {mensaje}")


@dataclass
class SensorPresion(Sensor):
    umbral_presion: float = 100.0
    def en_alerta(self) -> bool:
        return self.promedio >= self.umbral_presion


class Configuracion:
    def __init__(self, parametros: Dict[str, object]) -> None:
        self.parametros = parametros

    def get(self, clave: str, default=None):
        return self.parametros.get(clave, default)

    def set(self, clave: str, valor: object) -> None:
        self.parametros[clave] = valor

    def mostrar(self) -> None:
        print("=== Configuración actual ===")
        for k, v in self.parametros.items():
            print(f"{k}: {v}")


class ReporteAlertas:
    def __init__(self) -> None:
        self.eventos: list[str] = []

    def agregar_evento(self, evento: str) -> None:
        self.eventos.append(evento)

    def gen_reporte(self) -> str:
        return "\n".join(self.eventos)


class FabricaSensores:
    @staticmethod
    def crear_sensor(tipo: str, id: str) -> Sensor:
        if tipo == "temperatura":
            return SensorTemperatura(id=id)
        elif tipo == "vibracion":
            return SensorVibracion(id=id)
        elif tipo == "presion":
            return SensorPresion(id=id)
        else:
            raise ValueError(f"Tipo de sensor desconocido: {tipo}")


# ========================
# Gestor de Alertas Modificado
# ========================

class GestorAlertas:
    def __init__(self,
                 sensores: List[Sensor],
                 notificadores: List[Notificador],
                 configuracion: Configuracion,
                 fabrica: FabricaSensores) -> None:
        self._sensores = sensores
        self._notificadores = notificadores
        self._configuracion = configuracion  # dependencia
        self._fabrica = fabrica              # dependencia
        self._reporte = ReporteAlertas()     # asociación

    def evaluar_y_notificar(self) -> None:
        print("\n=== NOTIFICACIONES ===")
        for s in self._sensores:
            if s.en_alerta():
                msg = f"ALERTA: Sensor {s.id} en umbral (avg={s.promedio:.2f})"
                for n in self._notificadores:
                    n.enviar(msg)
                print("")
                self._reporte.agregar_evento(msg)

    def generar_reporte(self) -> str:
        return self._reporte.gen_reporte()



