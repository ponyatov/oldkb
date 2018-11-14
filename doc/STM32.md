# STM32
## @brief Virtualized Unified Command Interface<br>Виртуализованный Унифицированный Командный Интерфейс (ВУКИ)

### interactive/programmable console for STM32 MCU-based embedded devices<br>интерактивная/программируемая консоль для встраиваемых устройств на базе МК STM32

* lite bytecode-based interpreter adopted for CMSIS-compatible MCUs<br>
  облегченный интерпретатор на основе байт-кода для CMSIS-совместимых микроконтроллеров 
  * STM32
    * AcSip S76 module: STM32L073
    * f0discovery: STM32F052
* PC emulator: portable bytecode interpreter (GNU C)<br>
  ПК эмулятор: переносимый интерпретатор байткода
  * with standalone bytecode compiler (flex/bison/C++)

* unified command interface for embedded devices
  * FORTH postfix command language (non-standart, close to FORTH-83)
  * optimized for low-memory devices (bytecode based)
  * double mode:
    * interactive command interface
    * bytecode package interpretation
  * programmable user console, includes bytecode compiler