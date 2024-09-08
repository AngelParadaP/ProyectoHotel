from faulthandler import disable
import tkinter as tk
from tkinter import SEL, ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

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

        self.cliente_id_counter = 1
        self.habitacion_id_counter = 1
        self.reservacion_id_counter = 1

    def registrar_cliente(self, nombre, direccion, email, telefono):
        id = str(self.cliente_id_counter)
        self.cliente_id_counter += 1
        
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
        for reservacion in self.reservaciones.values():
            if reservacion.cliente_id == id:
                return "HAS RESERVATION"
            
        if id in self.clientes:
            del self.clientes[id]
            return "SUCCESS"
        
        return "NOT FOUND"

    def registrar_habitacion(self, numero):
        id = str(self.habitacion_id_counter)
        self.habitacion_id_counter += 1
        
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

    def registrar_reservacion(self, cliente_id, habitacion_id, fecha_salida, hora_reservacion, costo):
        id = str(self.reservacion_id_counter)
        self.reservacion_id_counter += 1
        
        fecha_reservacion = "2024-09-03"  # Fecha actual ficticia
        self.reservaciones[id] = Reservacion(id, cliente_id, habitacion_id, fecha_reservacion, fecha_salida, hora_reservacion, costo)
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

        self.id_entry = tk.Entry(self.frame_clientes, state="disabled")
        self.nombre_entry = tk.Entry(self.frame_clientes, state="disabled")
        self.direccion_entry = tk.Entry(self.frame_clientes, state="disabled")
        self.email_entry = tk.Entry(self.frame_clientes, state="disabled")
        self.telefono_entry = tk.Entry(self.frame_clientes, state="disabled")

        self.id_entry.grid(row=1, column=1, padx=10, pady=5)
        self.nombre_entry.grid(row=2, column=1, padx=10, pady=5)
        self.direccion_entry.grid(row=3, column=1, padx=10, pady=5)
        self.email_entry.grid(row=4, column=1, padx=10, pady=5)
        self.telefono_entry.grid(row=5, column=1, padx=10, pady=5)

        self.nuevoButtonCliente=tk.Button(self.frame_clientes, text="Nuevo", command=self.nuevo_cliente)
        self.salvarButtonCliente=tk.Button(self.frame_clientes, state="disable", text="Salvar", command=self.registrar_cliente)
        self.CancelarButtonCliente=tk.Button(self.frame_clientes, state="disable", text="Cancelar", command=self.cancelar_cliente)
        self.editarButtonCliente=tk.Button(self.frame_clientes, text="Editar", state="disable", command=self.editar_cliente)
        self.eliminarButtonCliente=tk.Button(self.frame_clientes, text="Eliminar", state="disable", command=self.eliminar_cliente)
        
        self.nuevoButtonCliente.grid(row=6, column=0, padx=10, pady=5)
        self.salvarButtonCliente.grid(row=6, column=1, padx=10, pady=5)
        self.CancelarButtonCliente.grid(row=6, column=2, padx=10, pady=5)
        self.editarButtonCliente.grid(row=7, column=0, padx=10, pady=5)
        self.eliminarButtonCliente.grid(row=7, column=1, padx=10, pady=5)

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
        self.fecha_reservacion_entry = DateEntry(self.frame_reservaciones, date_pattern="yyyy-mm-dd")
        self.fecha_salida_entry = DateEntry(self.frame_reservaciones, date_pattern="yyyy-mm-dd")
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

        self.habitacion_id_entry = tk.Entry(self.frame_habitaciones, state="disabled")
        self.habitacion_numero_entry = tk.Entry(self.frame_habitaciones, state="disable")
        self.habitacion_estado_combobox = ttk.Combobox(self.frame_habitaciones, values=["Libre", "Reservado", "Cancelado"], state="disable")

        self.habitacion_id_entry.grid(row=1, column=1, padx=10, pady=5)
        self.habitacion_numero_entry.grid(row=2, column=1, padx=10, pady=5)
        self.habitacion_estado_combobox.grid(row=3, column=1, padx=10, pady=5)

        self.nueva_habitacionButton=tk.Button(self.frame_habitaciones, text="Nueva Habitación", command=self.nueva_habitacion,state="normal")
        self.salvarHabitacionButton=tk.Button(self.frame_habitaciones, text="Salvar", command=self.registrar_habitacion,state="disable")
        self.EditarHabitacionButton=tk.Button(self.frame_habitaciones, text="Editar", command=self.editar_habitacion,state="disable")
        self.cancelarHabitacion=tk.Button(self.frame_habitaciones, text="Cancelar", command=self.cancelar_habitacion,state="disable")

        self.nueva_habitacionButton.grid(row=4, column=0, padx=10, pady=5)
        self.salvarHabitacionButton.grid(row=4, column=1, padx=10, pady=5)
        self.EditarHabitacionButton.grid(row=4, column=2, padx=10, pady=5)
        self.cancelarHabitacion.grid(row=5, column=1, padx=10, pady=5)



    def nuevo_cliente(self):
        self.nuevoButtonCliente.config(state="disable")
        self.salvarButtonCliente.config(state="normal")
        self.CancelarButtonCliente.config(state="normal")
        self.limpiar_campos_cliente()
        self.id_entry.insert(0, self.sistema.cliente_id_counter)  # Muestra el siguiente ID disponible
        self.id_entry.config(state="disable")
        messagebox.showinfo("Nuevo Cliente", "Listo para ingresar un nuevo cliente.")


    def registrar_cliente(self):
  
        nombre = self.nombre_entry.get()
        direccion = self.direccion_entry.get()
        email = self.email_entry.get()
        telefono = self.telefono_entry.get()

        if not (nombre, direccion, email, telefono):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if self.sistema.registrar_cliente(nombre, direccion, email, telefono):
            self.nuevoButtonCliente.config(state="normal")
            self.editarButtonCliente.config(state="disable")
            self.salvarButtonCliente.config(state="disable")
            self.CancelarButtonCliente.config(state="disable")
            self.eliminarButtonCliente.config(state="disable")
            messagebox.showinfo("Éxito", "Cliente registrado con éxito.")
            self.actualizar_combobox_clientes()
            self.limpiar_campos_cliente()
            self.bloquear_campos_cliente()
        else:
            messagebox.showerror("Error", "No se pudo registrar el cliente.")

    def cancelar_cliente(self):
        self.limpiar_campos_cliente()
        self.bloquear_campos_cliente()
        self.nuevoButtonCliente.config(state="normal")
        self.editarButtonCliente.config(state="disable")
        self.salvarButtonCliente.config(state="disable")
        self.CancelarButtonCliente.config(state="disable")
        self.eliminarButtonCliente.config(state="disable")

    def buscar_cliente(self):
        id_cliente = self.id_cliente_entry.get()

        if id_cliente in self.sistema.clientes:
            self.limpiar_campos_cliente()

            self.nuevoButtonCliente.config(state="disable")
            self.editarButtonCliente.config(state="normal")
            self.salvarButtonCliente.config(state="disable")
            self.CancelarButtonCliente.config(state="normal")
            self.eliminarButtonCliente.config(state="normal")
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
            self.actualizar_combobox_clientes()
            self.cancelar_cliente()
        else:
            messagebox.showerror("Error", "Cliente no encontrado.")

    def eliminar_cliente(self):
        id = self.id_entry.get()
        
        state = self.sistema.eliminar_cliente(id)

        if state == "SUCCESS":
            messagebox.showinfo("Éxito", "Cliente eliminado con éxito.")
            self.actualizar_combobox_clientes()
            self.cancelar_cliente()
        elif state == "NOT FOUND":
            messagebox.showerror("Error", "El cliente no se encuentra registrado.")
        elif state == "HAS RESERVATION":
            messagebox.showerror("Error", "El cliente tiene reservaciones activas.")

    def limpiar_campos_cliente(self):
        self.id_entry.config(state="normal")
        self.nombre_entry.config(state="normal")
        self.direccion_entry.config(state="normal")
        self.email_entry.config(state="normal")
        self.telefono_entry.config(state="normal")
        
        self.id_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.direccion_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.telefono_entry.delete(0, tk.END)

    def bloquear_campos_cliente(self):
        self.id_entry.config(state="disable")
        self.nombre_entry.config(state="disable")
        self.direccion_entry.config(state="disable")
        self.email_entry.config(state="disable")
        self.telefono_entry.config(state="disable")


    def nueva_reservacion(self):
        self.limpiar_campos_reservacion()
        self.reservacion_id_entry.insert(0, self.sistema.reservacion_id_counter)  # Muestra el siguiente ID disponible
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
        fecha_reservacion = self.fecha_reservacion_entry.get()
        fecha_salida = self.fecha_salida_entry.get()
        hora_reservacion = self.hora_reservacion_entry.get()
        costo = self.costo_reservacion_entry.get()

        if not (id and cliente_id and habitacion_id and fecha_reservacion and fecha_salida and hora_reservacion and costo):
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
        
        #Estos valores solo son para la comparacion siguiente
        f_entrada = datetime.strptime(fecha_reservacion, "%Y-%m-%d")
        f_salida = datetime.strptime(fecha_salida, "%Y-%m-%d")
        f_actual = datetime.now()

        if not (f_entrada >= f_actual and f_salida >= f_actual and f_salida > f_entrada):
            messagebox.showerror("Error", "Las fechas no son validas.")
            return
        
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
        fecha_reservacion = self.fecha_reservacion_entry.get()
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
        
        #Estos valores solo son para la comparacion siguiente
        f_entrada = datetime.strptime(fecha_reservacion, "%Y-%m-%d")
        f_salida = datetime.strptime(fecha_salida, "%Y-%m-%d")
        f_actual = datetime.now()
        
        if not (f_entrada >= f_actual and f_salida >= f_actual and f_salida > f_entrada):
            messagebox.showerror("Error", "Las fechas no son validas.")
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
        self.habitacion_id_entry.config(state="normal")
        self.habitacion_id_entry.insert(0, self.sistema.habitacion_id_counter)  # Muestra el siguiente ID disponible
        self.habitacion_id_entry.config(state="disabled")
        self.habitacion_estado_combobox.set("Libre")
        self.nueva_habitacionButton.config(state="disable")
        self.EditarHabitacionButton.config(state="disable")
        self.salvarHabitacionButton.config(state="normal")
        self.cancelarHabitacion.config(state="normal")
        messagebox.showinfo("Nueva Habitación", "Listo para ingresar una nueva habitación.")


    def registrar_habitacion(self):
        numero = self.habitacion_numero_entry.get()
        if not numero :
            messagebox.showerror("Error", "El número de la habitación es obligatorio.")
            return
        if self.sistema.registrar_habitacion(numero):
            self.nueva_habitacionButton.config(state="normal")
            self.EditarHabitacionButton.config(state="disable")
            self.salvarHabitacionButton.config(state="disable")
            self.cancelarHabitacion.config(state="disable")

            messagebox.showinfo("Éxito", "Habitación registrada con éxito.")
            self.actualizar_combobox_habitaciones()
            self.limpiar_campos_habitacion()
            self.habitacion_numero_entry.config(state="disable")
        else:
            messagebox.showerror("Error", "No se pudo registrar la habitación.")

    def buscar_habitacion(self):

        numero = self.habitacion_busquedanumero_entry.get()
        habitacion = self.sistema.buscar_habitacion(numero)
        if habitacion:
            self.nueva_habitacionButton.config(state="disable")
            self.EditarHabitacionButton.config(state="normal")
            self.salvarHabitacionButton.config(state="disable")
            self.cancelarHabitacion.config(state="normal")
            self.habitacion_id_entry.config(state="normal")
            self.habitacion_id_entry.delete(0, tk.END)
            self.habitacion_numero_entry.config(state="normal")
            self.habitacion_numero_entry.delete(0, tk.END)
            self.habitacion_estado_combobox.set("")

            self.habitacion_id_entry.insert(0, habitacion.id)
            self.habitacion_numero_entry.insert(0, habitacion.numero)
            self.habitacion_estado_combobox.set(habitacion.estado)
            self.habitacion_estado_combobox.config(state="normal")
            self.habitacion_id_entry.config(state="disable")

        else:
            messagebox.showerror("Error", "Habitación no encontrada.")
            self.cancelar_habitacion()

    def editar_habitacion(self):
        id = self.habitacion_id_entry.get()
        numero = self.habitacion_numero_entry.get()
        estado = self.habitacion_estado_combobox.get()

        if not (id and numero and estado):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if self.sistema.editar_habitacion(id, numero, estado):
            messagebox.showinfo("Éxito", "Habitación editada con éxito.")
            self.actualizar_combobox_habitaciones()
            self.cancelar_habitacion()
        else:
            messagebox.showerror("Error", "Habitación no encontrada.")

    def cancelar_habitacion(self):
            self.nueva_habitacionButton.config(state="normal")
            self.EditarHabitacionButton.config(state="disable")
            self.salvarHabitacionButton.config(state="disable")
            self.cancelarHabitacion.config(state="disable")

            self.limpiar_campos_habitacion()
            self.habitacion_estado_combobox.config(state="disable")
            self.habitacion_numero_entry.config(state="disable")

    def limpiar_campos_habitacion(self):
        self.habitacion_id_entry.config(state="normal")
        self.habitacion_numero_entry.config(state="normal")
        self.habitacion_id_entry.delete(0, tk.END)
        self.habitacion_numero_entry.delete(0, tk.END)
        self.habitacion_estado_combobox.set("")
        self.habitacion_id_entry.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelApp(root)
    root.mainloop()