# Tesis Samsara

El siguiente repositorio contiene el código de todo el proceso de Tesis para el Proyecto SAMSARA.

## Estructura del repositorio

* samsara: Contiene todos los códigos asociados al proceso de Modelamiento de los Datos.
* EDA: Contiene un Dashboard interactivo con todo lo relacionado a la Exploración de los Datos. 

## Funcionamiento

- Para visualizar el Dashboard de EDA:

```bash
make dashboard
```

- Para Resamplear e Interpolar los datos:

```bash
make resample r=<resample> i=<interpolate>
```
donde se pueden tomar los siguientes valores:

> **resample**: ["W","2W","M"]  
> **interpolate**: ["linear", "time", "ff", "bf"]

- Para ejecutar los tests:

```bash
make tests
```
