from faulthandler import disable
import tkinter as tk
from tkinter import SEL, ttk, messagebox

class Cliente:
    def __init__(self, id, nombre, direccion, email, telefono):
        self.id = id
        self.nombre = nombre
        self.direccion = direccion
        self.email = email
        self.telefono = telefono

class Habitacion:
    def __init__(self, id, numero, estado="Libre"):
        self.id = id
        self.numero = numero
        self.estado = estado

class Reservacion:
    def __init__(self, id, cliente_id, habitacion_id, fecha_reservacion, fecha_salida, hora_reservacion,costo):
        self.id = id
        self.cliente_id = cliente_id
        self.habitacion_id = habitacion_id
        self.fecha_reservacion = fecha_reservacion
        self.fecha_salida = fecha_salida
        self.hora_reservacion = hora_reservacion
        self.costo = costo

class SistemaHotel:
    def __init__(self):
        self.clientes = {}
        self.habitaciones = {}
        self.reservaciones = {}

    def registrar_cliente(self, id, nombre, direccion, email, telefono):
        if id in self.clientes:

            return False
        self.clientes[id] = Cliente(id, nombre, direccion, email, telefono)
        return True

    def buscar_cliente(self, nombre):
        for cliente in self.clientes.values():
            if cliente.nombre == nombre:
                return cliente
        return None

    def editar_cliente(self, id, nombre, direccion, email, telefono):
        if id not in self.clientes:
            return False
        self.clientes[id] = Cliente(id, nombre, direccion, email, telefono)
        return True

    def eliminar_cliente(self, id):
        if id in self.clientes:
            del self.clientes[id]
            return True
        return False

    def registrar_habitacion(self, id, numero):
        if id in self.habitaciones:
            return False
        self.habitaciones[id] = Habitacion(id, numero)
        return True

    def buscar_habitacion(self, numero):
        for habitacion in self.habitaciones.values():
            if habitacion.numero == numero:
                return habitacion
        return None

    def editar_habitacion(self, id, numero, estado):
        if id not in self.habitaciones:
            return False
        self.habitaciones[id] = Habitacion(id, numero, estado)
        return True

    def registrar_reservacion(self, id, cliente_id, habitacion_id, fecha_salida,hora_reservacion, costo):
        if id in self.reservaciones:
            return False
        fecha_reservacion = "2024-09-03"  # Fecha actual ficticia
        self.reservaciones[id] = Reservacion(id, cliente_id, habitacion_id, fecha_reservacion, fecha_salida,hora_reservacion, costo)
        self.habitaciones[habitacion_id].estado = "Reservado"
        return True

    def buscar_reservacion(self, nombre):
        for reservacion in self.reservaciones.values():
            cliente = self.clientes.get(reservacion.cliente_id)
            if cliente and cliente.nombre == nombre:
                return reservacion
        return None


    def eliminar_reservacion(self, id):
        if id in self.reservaciones:
            habitacion_id = self.reservaciones[id].habitacion_id
            del self.reservaciones[id]
            self.habitaciones[habitacion_id].estado = "Libre"

            return True
        return False

class HotelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Reservación de Hotel")

        self.sistema = SistemaHotel()

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10, expand=True)

        self.frame_clientes = ttk.Frame(self.notebook)
        self.frame_reservaciones = ttk.Frame(self.notebook)
        self.frame_habitaciones = ttk.Frame(self.notebook)

        self.notebook.add(self.frame_clientes, text="Clientes")
        self.notebook.add(self.frame_reservaciones, text="Reservaciones")
        self.notebook.add(self.frame_habitaciones, text="Habitación")

        self.setup_clientes_tab()
        self.setup_reservaciones_tab()
        self.setup_habitaciones_tab()

    def setup_clientes_tab(self):
        tk.Label(self.frame_clientes, text="Ingrese Id del Cliente:").grid(row=0, column=0, padx=10, pady=5)
        self.id_cliente_entry = tk.Entry(self.frame_clientes)
        self.id_cliente_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(self.frame_clientes, text="Buscar", command=self.buscar_cliente).grid(row=0, column=2, padx=10, pady=5)

        tk.Label(self.frame_clientes, text="ID:").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.frame_clientes, text="Nombre:").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(self.frame_clientes, text="Dirección:").grid(row=3, column=0, padx=10, pady=5)
        tk.Label(self.frame_clientes, text="Email:").grid(row=4, column=0, padx=10, pady=5)
        tk.Label(self.frame_clientes, text="Teléfono:").grid(row=5, column=0, padx=10, pady=5)

        self.id_entry = tk.Entry(self.frame_clientes)
        self.nombre_entry = tk.Entry(self.frame_clientes)
        self.direccion_entry = tk.Entry(self.frame_clientes)
        self.email_entry = tk.Entry(self.frame_clientes)
        self.telefono_entry = tk.Entry(self.frame_clientes)

        self.id_entry.grid(row=1, column=1, padx=10, pady=5)
        self.nombre_entry.grid(row=2, column=1, padx=10, pady=5)
        self.direccion_entry.grid(row=3, column=1, padx=10, pady=5)
        self.email_entry.grid(row=4, column=1, padx=10, pady=5)
        self.telefono_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Button(self.frame_clientes, text="Nuevo", command=self.nuevo_cliente).grid(row=6, column=0, padx=10, pady=5)
        tk.Button(self.frame_clientes, text="Salvar", command=self.registrar_cliente).grid(row=6, column=1, padx=10, pady=5)
        tk.Button(self.frame_clientes, text="Cancelar", command=self.limpiar_campos_cliente).grid(row=6, column=2, padx=10, pady=5)
        tk.Button(self.frame_clientes, text="Editar", command=self.editar_cliente).grid(row=7, column=0, padx=10, pady=5)
        tk.Button(self.frame_clientes, text="Eliminar", command=self.eliminar_cliente).grid(row=7, column=1, padx=10, pady=5)

    def setup_reservaciones_tab(self):
        tk.Label(self.frame_reservaciones, text="Ingrese Reservacion:").grid(row=0, column=0, padx=10, pady=5)
        self.reservacion_idreservacion_entry = tk.Entry(self.frame_reservaciones)
        self.reservacion_idreservacion_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(self.frame_reservaciones, text="Buscar Reservación", command=self.buscar_reservacion).grid(row=0, column=2, padx=10, pady=5)

        tk.Label(self.frame_reservaciones, text="Reservación ID:").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.frame_reservaciones, text="Cliente ID:").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(self.frame_reservaciones, text="Habitación ID:").grid(row=3, column=0, padx=10, pady=5)
        tk.Label(self.frame_reservaciones, text="Fecha Reservación:").grid(row=4, column=0, padx=10, pady=5)
        tk.Label(self.frame_reservaciones, text="Fecha Salida:").grid(row=5, column=0, padx=10, pady=5)
        tk.Label(self.frame_reservaciones, text="Hora Reservación:").grid(row=6, column=0, padx=10, pady=5)
        tk.Label(self.frame_reservaciones, text="Costo:").grid(row=7, column=0, padx=10, pady=5)

        self.reservacion_id_entry = tk.Entry(self.frame_reservaciones)
        self.cliente_id_reservacion_combobox = ttk.Combobox(self.frame_reservaciones)
        self.habitacion_id_reservacion_combobox = ttk.Combobox(self.frame_reservaciones)
        self.fecha_reservacion_entry = tk.Entry(self.frame_reservaciones)
        self.fecha_salida_entry = tk.Entry(self.frame_reservaciones)
        self.hora_reservacion_entry = tk.Entry(self.frame_reservaciones)
        self.costo_reservacion_entry = tk.Entry(self.frame_reservaciones)

        self.reservacion_id_entry.grid(row=1, column=1, padx=10, pady=5)
        self.cliente_id_reservacion_combobox.grid(row=2, column=1, padx=10, pady=5)
        self.habitacion_id_reservacion_combobox.grid(row=3, column=1, padx=10, pady=5)
        self.fecha_reservacion_entry.grid(row=4, column=1, padx=10, pady=5)
        self.fecha_salida_entry.grid(row=5, column=1, padx=10, pady=5)
        self.hora_reservacion_entry.grid(row=6, column=1, padx=10, pady=5)
        self.costo_reservacion_entry.grid(row=7, column=1, padx=10, pady=5)

        tk.Button(self.frame_reservaciones, text="Nueva Reservacion", command=self.nueva_reservacion).grid(row=8, column=0, padx=10, pady=5)
        tk.Button(self.frame_reservaciones, text="Reservar", command=self.registrar_reservacion).grid(row=8, column=1, padx=10, pady=5)
        tk.Button(self.frame_reservaciones, text="Cancelar Reservacion", command=self.cancelar_reservacion).grid(row=8, column=2, padx=10, pady=5)
        tk.Button(self.frame_reservaciones, text="Editar", command=self.editar_reservacion).grid(row=9, column=0, padx=10, pady=5)


    def setup_habitaciones_tab(self):
        tk.Label(self.frame_habitaciones, text="Ingrese Numero de Habitación:").grid(row=0, column=0, padx=10, pady=5)
        self.habitacion_busquedanumero_entry = tk.Entry(self.frame_habitaciones)
        self.habitacion_busquedanumero_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Button(self.frame_habitaciones, text="Buscar", command=self.buscar_habitacion).grid(row=0, column=2, padx=10, pady=5)

        tk.Label(self.frame_habitaciones, text="Habitacion ID:").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.frame_habitaciones, text="Numero:").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(self.frame_habitaciones, text="Seleccione Estado Habitacion:").grid(row=3, column=0, padx=10, pady=5)

        self.habitacion_id_entry = tk.Entry(self.frame_habitaciones)
        self.habitacion_numero_entry = tk.Entry(self.frame_habitaciones)
        self.habitacion_estado_combobox = ttk.Combobox(self.frame_habitaciones, values=["Libre", "Reservado", "Cancelado"])

        self.habitacion_id_entry.grid(row=1, column=1, padx=10, pady=5)
        self.habitacion_numero_entry.grid(row=2, column=1, padx=10, pady=5)
        self.habitacion_estado_combobox.grid(row=3, column=1, padx=10, pady=5)

        tk.Button(self.frame_habitaciones, text="Nueva Habitación", command=self.registrar_habitacion).grid(row=4, column=0, padx=10, pady=5)
        tk.Button(self.frame_habitaciones, text="Editar", command=self.editar_habitacion).grid(row=4, column=1, padx=10, pady=5)


    def nuevo_cliente(self):
        self.limpiar_campos_cliente()
        messagebox.showinfo("Nuevo Cliente", "Listo para ingresar un nuevo cliente.")

    def registrar_cliente(self):
        id = self.id_entry.get()
        nombre = self.nombre_entry.get()
        direccion = self.direccion_entry.get()
        email = self.email_entry.get()
        telefono = self.telefono_entry.get()

        if not (id and nombre and direccion and email and telefono):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if self.sistema.registrar_cliente(id, nombre, direccion, email, telefono):
            messagebox.showinfo("Éxito", "Cliente registrado con éxito.")
            self.actualizar_combobox_clientes()
            self.limpiar_campos_cliente()
        else:
            messagebox.showerror("Error", "El ID del cliente ya existe.")

    def buscar_cliente(self):
        id_cliente = self.id_cliente_entry.get()

        if id_cliente in self.sistema.clientes:
            cliente = self.sistema.clientes[id_cliente]
            self.id_cliente_entry.delete(0, tk.END)
            self.id_entry.delete(0,tk.END)
            self.id_entry.insert(0, cliente.id)
            self.id_entry.config(state=tk.DISABLED)
            self.nombre_entry.delete(0, tk.END)
            self.nombre_entry.insert(0, cliente.nombre)
            self.direccion_entry.delete(0, tk.END)
            self.direccion_entry.insert(0,cliente.direccion)
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, cliente.email)
            self.telefono_entry.delete(0, tk.END)
            self.telefono_entry.insert(0, cliente.telefono)
            messagebox.showinfo("Éxito", "Cliente encontrado.")
        else:
            messagebox.showerror("Error", "Cliente no encontrado.")


    def editar_cliente(self):
        id = self.id_entry.get()
        nombre = self.nombre_entry.get()
        direccion = self.direccion_entry.get()
        email = self.email_entry.get()
        telefono = self.telefono_entry.get()

        if not (id and nombre and direccion and email and telefono):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if self.sistema.editar_cliente(id, nombre, direccion, email, telefono):
            messagebox.showinfo("Éxito", "Cliente editado con éxito.")
            self.actualizar_combobox_clientes
            self.limpiar_campos_cliente()
        else:
            messagebox.showerror("Error", "Cliente no encontrado.")

    def eliminar_cliente(self):
        id = self.id_entry.get()

        if self.sistema.eliminar_cliente(id):
            messagebox.showinfo("Éxito", "Cliente eliminado con éxito.")
            self.actualizar_combobox_clientes
            self.limpiar_campos_cliente()
        else:
            messagebox.showerror("Error", "Cliente no encontrado.")

    def limpiar_campos_cliente(self):
        self.id_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.direccion_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)

    def nueva_reservacion(self):
        self.limpiar_campos_reservacion()
        self.actualizar_combobox_clientes()
        self.actualizar_combobox_habitaciones()
        messagebox.showinfo("Nueva Reservación", "Listo para ingresar una nueva reservación.")

    def actualizar_combobox_clientes(self):
        self.cliente_id_reservacion_combobox['values'] = list(self.sistema.clientes.keys())

    def actualizar_combobox_habitaciones(self):
        habitaciones_libres = [h.id for h in self.sistema.habitaciones.values() if h.estado == "Libre"]
        self.habitacion_id_reservacion_combobox['values'] = habitaciones_libres


    def registrar_reservacion(self):
        id = self.reservacion_id_entry.get()
        cliente_id = self.cliente_id_reservacion_combobox.get()
        habitacion_id = self.habitacion_id_reservacion_combobox.get()
        fecha_salida = self.fecha_salida_entry.get()
        hora_reservacion = self.hora_reservacion_entry.get()
        costo = self.costo_reservacion_entry.get()

        if not (id and cliente_id and habitacion_id and fecha_salida and hora_reservacion and costo):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if id in self.sistema.reservaciones:
            messagebox.showerror("Error", "El ID de la reservación ya existe.")
            return

        if cliente_id not in self.sistema.clientes:
            messagebox.showerror("Error", "El ID del cliente no existe.")
            return

        if habitacion_id not in self.sistema.habitaciones:
            messagebox.showerror("Error", "El ID de la habitación no existe.")
            return

        habitacion = self.sistema.habitaciones[habitacion_id]
        if habitacion.estado != "Libre":
            messagebox.showerror("Error", "La habitación no está disponible.")
            return

        fecha_reservacion = "2024-09-03"  
        self.sistema.reservaciones[id] = Reservacion(id, cliente_id, habitacion_id, fecha_reservacion, fecha_salida, hora_reservacion, costo)
        self.sistema.habitaciones[habitacion_id].estado = "Reservado"
        messagebox.showinfo("Éxito", "Reservación registrada con éxito.")
        self.actualizar_combobox_clientes()
        self.actualizar_combobox_habitaciones()
        self.limpiar_campos_reservacion()

    
    def buscar_reservacion(self):
        self.actualizar_combobox_clientes()
        self.actualizar_combobox_habitaciones()
        reservacion_id = self.reservacion_idreservacion_entry.get()

        reservacion = self.sistema.reservaciones.get(reservacion_id)
        if reservacion:
            cliente = self.sistema.clientes.get(reservacion.cliente_id)
            self.reservacion_id_entry.delete(0, tk.END)
            self.cliente_id_reservacion_combobox.delete(0, tk.END)
            self.habitacion_id_reservacion_combobox.delete(0, tk.END)
            self.fecha_reservacion_entry.delete(0, tk.END)
            self.fecha_salida_entry.delete(0, tk.END)
            self.hora_reservacion_entry.delete(0, tk.END)
            self.costo_reservacion_entry.delete(0, tk.END)

            self.reservacion_id_entry.insert(0, reservacion.id)
            self.cliente_id_reservacion_combobox.insert(0, reservacion.cliente_id)
            self.habitacion_id_reservacion_combobox.insert(0, reservacion.habitacion_id)
            self.fecha_reservacion_entry.insert(0, reservacion.fecha_reservacion)
            self.fecha_salida_entry.insert(0, reservacion.fecha_salida)
            self.hora_reservacion_entry.insert(0, reservacion.hora_reservacion)
            self.costo_reservacion_entry.insert(0, reservacion.costo)
        else:
            messagebox.showerror("Error", "Reservación no encontrada.")


    def cancelar_reservacion(self):
        id = self.reservacion_id_entry.get()

        if self.sistema.eliminar_reservacion(id):
            self.actualizar_combobox_clientes()
            self.actualizar_combobox_habitaciones()
            messagebox.showinfo("Éxito", "Reservación cancelada con éxito.")
            
            self.limpiar_campos_reservacion()
        else:
            messagebox.showerror("Error", "Reservación no encontrada.")

    def limpiar_campos_reservacion(self):
        self.reservacion_id_entry.delete(0, tk.END)
        self.cliente_id_reservacion_combobox.delete(0, tk.END)
        self.habitacion_id_reservacion_combobox.delete(0, tk.END)
        self.fecha_reservacion_entry.delete(0, tk.END)
        self.fecha_salida_entry.delete(0, tk.END)
        self.hora_reservacion_entry.delete(0, tk.END)
        self.costo_reservacion_entry.delete(0, tk.END)

    def editar_reservacion(self):
        id = self.reservacion_id_entry.get()
        cliente_id = self.cliente_id_reservacion_combobox.get()
        nueva_habitacion_id = self.habitacion_id_reservacion_combobox.get()
        fecha_salida = self.fecha_salida_entry.get()
        hora_reservacion = self.hora_reservacion_entry.get()
        costo = self.costo_reservacion_entry.get()

        if not (id and cliente_id and nueva_habitacion_id and fecha_salida and hora_reservacion and costo):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if cliente_id not in self.sistema.clientes:
            messagebox.showerror("Error", "El ID del cliente no existe.")
            return

        if nueva_habitacion_id not in self.sistema.habitaciones:
            messagebox.showerror("Error", "El ID de la habitación no existe.")
            return

        if id in self.sistema.reservaciones:
            reservacion = self.sistema.reservaciones[id]
            habitacion_antigua_id = reservacion.habitacion_id
            
            # Actualizar la habitación antigua a "Libre"
            if habitacion_antigua_id in self.sistema.habitaciones:
                self.sistema.habitaciones[habitacion_antigua_id].estado = "Libre"

            # Actualizar los detalles de la reservación
            reservacion.cliente_id = cliente_id
            reservacion.habitacion_id = nueva_habitacion_id
            reservacion.fecha_salida = fecha_salida
            reservacion.hora_reservacion = hora_reservacion
            reservacion.costo = costo

            # Actualizar la nueva habitación a "Reservado"
            if nueva_habitacion_id in self.sistema.habitaciones:
                self.sistema.habitaciones[nueva_habitacion_id].estado = "Reservado"

            messagebox.showinfo("Éxito", "Reservación editada con éxito.")
            self.actualizar_combobox_clientes()
            self.actualizar_combobox_habitaciones()
            self.limpiar_campos_reservacion()
        else:
            messagebox.showerror("Error", "Reservación no encontrada.")



    def nueva_habitacion(self):
        self.limpiar_campos_habitacion()
        messagebox.showinfo("Nueva Habitación registrada")

    def registrar_habitacion(self):
        id = self.habitacion_id_entry.get()
        numero = self.habitacion_numero_entry.get()

        if not (id and numero):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if self.sistema.registrar_habitacion(id, numero):
            messagebox.showinfo("Éxito", "Habitación registrada con éxito.")
            self.actualizar_combobox_habitaciones()
            self.limpiar_campos_habitacion()
        else:
            messagebox.showerror("Error", "El ID de la habitación ya existe.")

    def buscar_habitacion(self):

        numero = self.habitacion_busquedanumero_entry.get()

        habitacion = self.sistema.buscar_habitacion(numero)
        if habitacion:
            self.habitacion_id_entry.delete(0, tk.END)
            self.habitacion_numero_entry.delete(0, tk.END)
            self.habitacion_estado_combobox.set("")

            self.habitacion_id_entry.insert(0, habitacion.id)
            self.habitacion_numero_entry.insert(0, habitacion.numero)
            self.habitacion_estado_combobox.set(habitacion.estado)
        else:
            messagebox.showerror("Error", "Habitación no encontrada.")

    def editar_habitacion(self):
        id = self.habitacion_id_entry.get()
        numero = self.habitacion_numero_entry.get()
        estado = self.habitacion_estado_combobox.get()

        if not (id and numero and estado):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if self.sistema.editar_habitacion(id, numero, estado):
            messagebox.showinfo("Éxito", "Habitación editada con éxito.")
            self.actualizar_combobox_habitaciones
            self.limpiar_campos_habitacion()
        else:
            messagebox.showerror("Error", "Habitación no encontrada.")

    def limpiar_campos_habitacion(self):
        self.habitacion_id_entry.delete(0, tk.END)
        self.habitacion_numero_entry.delete(0, tk.END)
        self.habitacion_estado_combobox.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelApp(root)
    root.mainloop()