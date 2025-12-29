' Archivo: C:\Scripts\ejecutar_nmon_boton.vbs
' Simula hacer clic en el botón del Excel

Option Explicit
On Error Resume Next

Dim objExcel, objWorkbook, objWorksheet, objButton
Dim tiempoInicio, tiempoFin, rutaLog

' ================================================
' CONFIGURACIÓN - ¡ESTO ES LO MÁS IMPORTANTE!
' ================================================
Dim rutaExcel
' CAMBIA ESTA RUTA a la ubicación REAL de tu archivo Excel:
rutaExcel = "C:\Users\TU_USUARIO\Desktop\NMON_Analyser.xlsm" ' <-- ¡CAMBIAR!
rutaLog = "C:\Scripts\nmon_boton_log.txt"
' ================================================

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
On Error Resume Next
Set objWorkbook = objExcel.Workbooks.Open(rutaExcel, False, True)
If Err.Number <> 0 Then
    Call EscribirLog("ERROR: No se pudo abrir el archivo Excel. Verifica la ruta.")
    Call EscribirLog("Ruta intentada: " & rutaExcel)
    objExcel.Quit
    WScript.Quit 1
End If
On Error GoTo 0

' Esperar a que cargue
WScript.Sleep 3000

' OPCIÓN 1: Ejecutar la macro directamente por su nombre
Call EscribirLog("Intentando ejecutar macro directamente...")

' Lista de posibles nombres de macros (basado en tu imagen)
Dim arrMacros, nombreMacro
arrMacros = Array( _
    "Button2_Click", _
    "ProcesaNmonAutomatico", _
    "EjecutarAnalisis", _
    "CreatePivot", _
    "SYS_SUMM", _
    "DISKBUSTRK" _
)

Dim macroEjecutada
macroEjecutada = False

For Each nombreMacro In arrMacros
    On Error Resume Next
    Call EscribirLog("Intentando ejecutar macro: " & nombreMacro)
    objExcel.Run nombreMacro
    If Err.Number = 0 Then
        Call EscribirLog("✓ Macro ejecutada exitosamente: " & nombreMacro)
        macroEjecutada = True
        Exit For
    Else
        Call EscribirLog("✗ No se pudo ejecutar: " & nombreMacro & " - Error: " & Err.Description)
        Err.Clear
    End If
    On Error GoTo 0
Next

' OPCIÓN 2: Buscar y hacer clic en el botón
If Not macroEjecutada Then
    Call EscribirLog("Buscando botón por nombre específico...")
    
    ' Posibles nombres de botones basados en tu imagen
    Dim arrBotones
    arrBotones = Array("Button2", "Button1", "CommandButton1", "btnProcesar", "btnAnalizar")
    
    Dim botonEncontrado
    botonEncontrado = False
    
    ' Buscar en todas las hojas
    Dim hoja, objOLEObject
    For Each hoja In objWorkbook.Worksheets
        For Each objOLEObject In hoja.OLEObjects
            If TypeName(objOLEObject.Object) = "CommandButton" Then
                Call EscribirLog("Botón encontrado: " & objOLEObject.Name & " en hoja: " & hoja.Name)
                
                ' Hacer clic en el botón
                objOLEObject.Object.Value = True
                botonEncontrado = True
                
                Call EscribirLog("✓ Clic simulado en botón: " & objOLEObject.Name)
                Exit For
            End If
        Next
        
        If botonEncontrado Then Exit For
    Next
    
    If Not botonEncontrado Then
        Call EscribirLog("ADVERTENCIA: No se encontró ningún botón visible")
    End If
End If

' Esperar a que termine el procesamiento
Call EscribirLog("Esperando a que termine el procesamiento...")

' Espera más larga para procesamiento NMON (ajustar según necesidad)
Dim tiempoEsperaTotal
tiempoEsperaTotal = 120  ' 2 minutos (puedes aumentar si procesa muchos archivos)

Dim i
For i = 1 To tiempoEsperaTotal
    WScript.Sleep 1000  ' Espera de 1 segundo
    
    If i Mod 10 = 0 Then  ' Log cada 10 segundos
        Call EscribirLog("Esperando... (" & i & " segundos)")
    End If
Next

' Verificar si Excel está ocupado
If objExcel.CalculationState <> -4143 Then ' -4143 = xlDone
    Call EscribirLog("ADVERTENCIA: Excel aún está procesando, pero continuamos...")
End If

' Cerrar Excel
Call EscribirLog("Cerrando Excel...")

On Error Resume Next
objWorkbook.Saved = True  ' Marcar como guardado para evitar preguntas
objWorkbook.Close False   ' Cerrar sin guardar
objExcel.Quit
On Error GoTo 0

' Liberar objetos
Set objOLEObject = Nothing
Set objWorksheet = Nothing
Set objWorkbook = Nothing
Set objExcel = Nothing

tiempoFin = Now()

Call EscribirLog("Procesamiento completado. Duración: " & DateDiff("s", tiempoInicio, tiempoFin) & " segundos")
Call EscribirLog("=== FIN PROCESAMIENTO ===")

WScript.Echo "Proceso completado. Revisa el log en: " & rutaLog
WScript.Quit 0