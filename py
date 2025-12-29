' Archivo: C:\Scripts\ejecutar_nmon_boton.vbs
' Simula hacer clic en el botón del Excel

Option Explicit
On Error Resume Next

Dim objExcel, objWorkbook, objWorksheet, objButton
Dim tiempoInicio, tiempoFin, rutaLog

' Configuración
Dim rutaExcel
rutaExcel = "C:\Ruta\A\Tu\Archivo\NMON_Analyser.xlsm" ' <-- CAMBIA ESTA RUTA
rutaLog = "C:\Scripts\nmon_boton_log.txt"

tiempoInicio = Now()

' Función para escribir log
Sub EscribirLog(mensaje)
    Dim fso, archivo
    Set fso = CreateObject("Scripting.FileSystemObject")
    
    If fso.FileExists(rutaLog) Then
        Set archivo = fso.OpenTextFile(rutaLog, 8, True) ' 8 = Append
    Else
        Set archivo = fso.CreateTextFile(rutaLog, True)
    End If
    
    archivo.WriteLine FormatDateTime(Now, vbLongDate) & " " & FormatDateTime(Now, vbLongTime) & " - " & mensaje
    archivo.Close
    Set fso = Nothing
End Sub

' Registrar inicio
Call EscribirLog("=== INICIANDO PROCESAMIENTO AUTOMÁTICO ===")

' Crear objeto Excel (OCULTO)
Set objExcel = CreateObject("Excel.Application")
objExcel.Visible = False  ' IMPORTANTE: Oculto para procesamiento automático
objExcel.DisplayAlerts = False
objExcel.AskToUpdateLinks = False
objExcel.EnableEvents = False

Call EscribirLog("Excel iniciado (modo oculto)")

' Abrir el archivo Excel
Call EscribirLog("Abriendo archivo: " & rutaExcel)
Set objWorkbook = objExcel.Workbooks.Open(rutaExcel, False, True)

' Esperar a que cargue
WScript.Sleep 2000

' Buscar y hacer clic en el botón
Call EscribirLog("Buscando botón para hacer clic...")

' Opción A: Si el botón está en la hoja "Analyser" (hoja 1)
Set objWorksheet = objWorkbook.Worksheets(1) ' Hoja 1 = Analyser

' Buscar todos los botones en la hoja
Dim objOLEObject
Dim botonEncontrado
botonEncontrado = False

For Each objOLEObject In objWorksheet.OLEObjects
    If TypeName(objOLEObject.Object) = "CommandButton" Then
        Call EscribirLog("Botón encontrado: " & objOLEObject.Name & " en posición " & objOLEObject.TopLeftCell.Address)
        
        ' Hacer clic en el botón
        objOLEObject.Object.Value = True
        botonEncontrado = True
        
        Call EscribirLog("Clic simulado en botón: " & objOLEObject.Name)
        Exit For
    End If
Next

' Opción B: Si el botón tiene un nombre específico
If Not botonEncontrado Then
    Call EscribirLog("Buscando botón por nombre específico...")
    
    ' Nombres comunes de botones
    Dim nombresBotones
    nombresBotones = Array("Button1", "CommandButton1", "btnProcesar", "btnAnalizar", "ProcesarTodosLosNmon")
    
    Dim nombreBoton
    For Each nombreBoton In nombresBotones
        On Error Resume Next
        Set objOLEObject = objWorksheet.OLEObjects(nombreBoton)
        If Err.Number = 0 Then
            objOLEObject.Object.Value = True
            Call EscribirLog("Clic simulado en botón: " & nombreBoton)
            botonEncontrado = True
            Exit For
        End If
        On Error GoTo 0
    Next
End If

If Not botonEncontrado Then
    Call EscribirLog("ERROR: No se encontró ningún botón. Intentando ejecutar macro directamente...")
    
    ' Intentar ejecutar macro por nombre
    On Error Resume Next
    objExcel.Run "ProcesarTodosLosNmon"  ' Intenta con este nombre primero
    If Err.Number <> 0 Then
        objExcel.Run "EjecutarAnalisis"  ' Luego con este
    End If
    If Err.Number <> 0 Then
        objExcel.Run "ProcesarNmonAutomatico"  ' Finalmente con este
    End If
    
    If Err.Number = 0 Then
        Call EscribirLog("Macro ejecutada directamente por nombre")
    Else
        Call EscribirLog("ERROR: No se pudo ejecutar ninguna macro")
    End If
    On Error GoTo 0
End If

' Esperar a que termine el procesamiento (ajustar tiempo según necesidad)
Call EscribirLog("Esperando a que termine el procesamiento...")
WScript.Sleep 30000  ' 30 segundos (ajusta según tus archivos)

' Verificar si el procesamiento sigue activo
Dim contadorEspera
contadorEspera = 0
Do While objExcel.CalculationState <> xlDone And contadorEspera < 600  ' Máximo 10 minutos
    WScript.Sleep 1000
    contadorEspera = contadorEspera + 1
    
    If contadorEspera Mod 30 = 0 Then  ' Cada 30 segundos
        Call EscribirLog("Esperando... (" & contadorEspera & " segundos)")
    End If
Loop

' Cerrar Excel
Call EscribirLog("Cerrando Excel...")
objWorkbook.Saved = True  ' Marcar como guardado para evitar preguntas
objWorkbook.Close False   ' Cerrar sin guardar
objExcel.Quit

' Liberar objetos
Set objOLEObject = Nothing
Set objWorksheet = Nothing
Set objWorkbook = Nothing
Set objExcel = Nothing

tiempoFin = Now()

Call EscribirLog("Procesamiento completado. Duración: " & DateDiff("s", tiempoInicio, tiempoFin) & " segundos")
Call EscribirLog("=== FIN PROCESAMIENTO ===")

WScript.Quit 0