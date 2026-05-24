
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Dhcp" /v DependOnService /t REG_MULTI_SZ /d "Tcpip\0Afd\0NetBT" /f

​Para forzar el encendido de los protocolos base (TCP/IP y AFD):
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Tcpip" /v Start /t REG_DWORD /d 1 /f
reg add "HKLM\SYSTEM\CurrentControlSet\Services\Afd" /v Start /t REG_DWORD /d 1 /f
​Para reactivar el motor de Plug and Play (el responsable de que no te deje instalar el driver):
reg add "HKLM\SYSTEM\CurrentControlSet\Services\PlugPlay" /v Start /t REG_DWORD /d 2 /f
