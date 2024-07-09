# robot

Программа для калибровки робота Fairino

## Содержание

1. [Содержание](#содержание)
2. [Требования к ПО](#требования-к-по)
3. [Инструкция для запуска программы](#инструкция-для-запуска-программы)

## Требования к ПО

- ОС Windows 10/11
- [Python 3.10.0](https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe)
- [Библиотека Fairino](https://github.com/FAIR-INNOVATION/fairino-python-sdk/raw/main/windows/fairino/Robot.cp310-win_amd64.pyd)

    Библиотека должна находиться по следующему пути: `C:\FAIRINO\PythonSDK\windows\libfairino\fairino`

## Инструкция для запуска программы

1. Создать виртуальное окружение:

```ps
PS python.exe -m venv .\.venv
```

2. Активировать виртуальное окружение:

```ps
PS Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force
PS .\.venv\Scripts\activate.ps1
```

3. Установить зависимости:

```ps
PS pip install -r .\requirements.txt
```

4. Создать файлы интерфейса:

```ps
PS pyuic6.exe .\ui\ip_window\ip_window.ui -o .\ui\ip_window\
PS pyuic6.exe .\ui\main_interface\main_interface.ui
PS pyuic6.exe .\ui\main_interface\calibration\calibration_window.ui
PS pyuic6.exe .\ui\main_interface\workspace_calibration\workspace_calibration.ui
```

4. Запустить программу:

```ps
PS python.exe .\main.py
```
