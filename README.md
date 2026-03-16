<div align="center">
  <h1>Integración y Análisis de Calidad de Código con SonarQube</h1>
  <p><i>Code Quality Analysis and Integration with SonarQube</i></p>
  
  <p>
    <a href="#-versión-en-español">Español</a> • 
    <a href="#-english-version">English</a>
  </p>
</div>

---

## 🇪🇸 Versión en Español

### 📌 Descripción General
Este repositorio documenta un flujo de trabajo profesional centrado en la configuración, integración e implementación de **SonarQube** para la inspección continua de la calidad del código, detección de *bugs* y la identificación de vulnerabilidades (SAST). 

El objetivo principal es demostrar un enfoque robusto y estandarizado aplicable a entornos empresariales reales, garantizando así un ciclo de vida de desarrollo de software (SDLC) seguro y mantenible.

### 🎯 Objetivos del Proyecto
* **Análisis de Código Estático:** Integrar SonarQube para revisar la salud de base de código.
* **Trazabilidad y Documentación:** Registrar meticulosamente cada comando, error y solución encontrados durante la configuración.
* **Calidad a Nivel de Producción:** Establecer *Quality Gates* (Puertas de Calidad) y umbrales estrictos.
* **Portafolio Profesional:** Servir como referencia técnica de habilidades en metodologías DevSecOps para contrataciones.

---

### 🛠️ Registro de Actividades e Implementación

En esta sección se detallará cronológicamente cada paso realizado para desplegar y utilizar SonarQube, incluyendo evidencias técnicas de cada fase.

#### Fase 1: Inicialización del Repositorio y Documentación
**Fecha de inicio:** Marzo 2026

Se comienza con la inicialización del repositorio y la creación de la estructura base para la documentación del proyecto.

#### Fase 2: Instalación y Configuración en Kali Linux (VM)
Para asegurar un entorno de análisis aislado y controlado, la infraestructura de SonarQube se despliega sobre una máquina virtual (VM) equipada con **Kali Linux**.

##### 1. Requisitos Previos Habituales
```bash
sudo apt update && sudo apt upgrade -y
```

##### 3. Instalación de Docker y Docker Compose
```bash
sudo apt install docker.io docker-compose -y
```

##### 4. Habilitar y Arrancar el Servicio de Docker
```bash
sudo systemctl enable docker --now
```

![Habilitando Docker](images/01_docker_kali.png)
*Resultado de la habilitación del servicio Docker en el sistema.*

#### Fase 3: Preparación del Código de Prueba (Vulnerable)
Para demostrar la efectividad de **SonarQube** detectando diferentes tipos de problemas, se ha desarrollado un script en Python (`vulnerable.py`).

##### Código Fuente (`vulnerable.py`)
```python
def funcion_trampa():
    # 1. VULNERABILIDAD (Hardcoded credential)
    password = "admin_password_123"
    # 2. CODE SMELL (Variable no usada)
    variable_inutil = 42
    # 3. BUG LÓGICO (Código inalcanzable)
    return True
    print("Esto nunca se ejecutará " + password)

funcion_trampa()
```

> **🛡️ Contexto de Seguridad y Calidad:** Este fragmento disparará tres alertas en SonarQube: Vulnerability (password hardcodeado), Code Smell (variable no usada) y Bug (código muerto).

![Código vulnerable en Nano](images/02_vulnerable_code.png)
*Script vulnerable.py editado con Nano.*

#### Fase 4: Despliegue de SonarQube
Instalamos la versión *lts-community* de SonarQube mediante Docker:

```bash
sudo docker run -d --name sonarqube -p 9000:9000 sonarqube:lts-community
```

##### Solución de Problemas: Límite de Memoria Virtual
Si el motor fallase por límites del Kernel, aplicar:
```bash
sudo sysctl -w vm.max_map_count=262144
```

#### Fase 5: Configuración de Seguridad y Accesos en la Interfaz Web
1. **Autenticación Inicial:** Login en `http://localhost:9000` con `admin/admin`.
![Inicio de sesión en SonarQube](images/03_sonarqube_login.png)

2. **Refuerzo de Credenciales:** Cambio de contraseña obligatorio.
![Cambio de contraseña obligatoria](images/04_password_update.png)

3. **Generación de Token (Best Practice):** Creación de un User Token llamado `Vulnerabilidades`.
![Generación del Token en la interfaz](images/05_token_generation.png)
![Token Creado Exitosamente](images/06_token_created.png)

#### Fase 6: Análisis de Código Estático (SAST) mediante SonarScanner
Ejecutamos el scanner en el directorio del proyecto:

```bash
sudo docker run --rm \
    --network host \
    -v "$(pwd):/usr/src" \
    sonarsource/sonar-scanner-cli \
    -Dsonar.projectKey=Analisis-Seguridad-C \
    -Dsonar.sources=. \
    -Dsonar.host.url=http://localhost:9000 \
    -Dsonar.login=squ_80f32df6860b0817c39a0dc4b2cb7f1d88a27873 \
    -Dsonar.python.version=3 \
    -Dsonar.scm.disabled=true
```

#### Fase 7: Creación de Quality Profile y Reglas SAST
Creamos un perfil personalizado para Python llamado `Vulnerabilidades` extendiendo `Sonar way`.
![Creación de Perfil](images/07_quality_profile_creation.png)

Activamos reglas específicas para `OS command injection` y `SQL injection`.
![Botón Activate More](images/08_activate_more_rules.png)

Establecemos el perfil como predeterminado.
![Set as Default Profile](images/09_set_as_default.png)

#### Fase 8: Revisión de Resultados y Quality Gates
El escaneo devuelve un estado de **"Failed"** debido a las incidencias críticas detectadas.
![Resultados del Dashboard](images/10_dashboard_results.png)

*   **1 New Bug:** Código inalcanzable.
*   **2 New Code Smells:** Variable inútil.
*   **Added Debt (20min):** 20 minutos de deuda técnica.

#### Fase 9: Remediación y Validación (Passed)
Refactorizamos el código para usar variables de entorno y limpiar la lógica:

```python
import os
def funcion_segura():
    password_segura = os.environ.get("DB_PASSWORD", "no_configurada")
    if password_segura != "no_configurada":
        print("Autenticación configurada de forma segura.")
        return True
    print("Falta configurar la variable de entorno.")
    return False
```

![Refactorización del código fuente en Nano](images/11_fixed_code_remediation.png)

Tras el re-escaneo, el estado pasa a **"Passed"**.
![Gráfico de Actividad y Quality Gate Superado](images/12_activity_graph_passed.png)

---

### Conclusiones y Valor Añadido
El análisis SAST permite la reducción de costes y estandarización de calidad mediante la filosofía **Shift-Left Security**.

#### Habilidades Técnicas Demostradas
* **DevSecOps:** Auditorías de seguridad automáticas.
* **Docker:** Despliegue de infraestructura crítica.
* **SAST:** Configuración de reglas y Quality Gates.
* **Python Security:** Remediación de vulnerabilidades comunes.

---

### 👤 Autor
* **Ismael A. Pérez Segura** - [LinkedIn](https://www.linkedin.com/in/ismael-perez-segura/)

### ⚠️ Aviso Legal
Este proyecto tiene únicamente fines educativos. El autor no se hace responsable del mal uso de la información.

<br><br>

---

## 🇺🇸 English Version

### 📌 General Overview
This repository documents a professional workflow focused on the configuration, integration, and implementation of **SonarQube** for continuous code quality inspection, bug detection, and security vulnerability identification (SAST).

The main objective is to demonstrate a robust and standardized approach applicable to real business environments, ensuring a secure and maintainable software development life cycle (SDLC).

### 🎯 Project Objectives
* **Static Code Analysis:** Integrate SonarQube to review the codebase health.
* **Traceability and Documentation:** Meticulously record every command, error, and solution found.
* **Production-Level Quality:** Establish strict *Quality Gates* and thresholds.
* **Professional Portfolio:** Technical reference of skills in DevSecOps methodologies.

---

### 🛠️ Implementation and Activity Log

This section details chronologically each step taken to deploy and use SonarQube, including technical evidence.

#### Phase 1: Repository Initialization and Documentation
**Starting Date:** March 2026

Initialization of the repository and creation of the base structure for project documentation.

#### Phase 2: Installation and Configuration on Kali Linux (VM)
SonarQube infrastructure is deployed on a **Kali Linux** virtual machine for an isolated analysis environment.

##### 1. Common Prerequisites
```bash
sudo apt update && sudo apt upgrade -y
```

##### 3. Docker and Docker Compose Installation
```bash
sudo apt install docker.io docker-compose -y
```

##### 4. Enable and Start Docker Service
```bash
sudo systemctl enable docker --now
```

![Enabling Docker](images/01_docker_kali.png)
*Result of enabling the Docker service in the system.*

#### Phase 3: Preparation of Test Code (Vulnerable)
A small Python script (`vulnerable.py`) was developed containing vulnerabilities, logic bugs, and code smells.

##### Source Code (`vulnerable.py`)
```python
def funcion_trampa():
    # 1. VULNERABILITY (Hardcoded credential)
    password = "admin_password_123"
    # 2. CODE SMELL (Unused variable)
    variable_inutil = 42
    # 3. LOGIC BUG (Unreachable code)
    return True
    print("This will never execute " + password)

funcion_trampa()
```

> **🛡️ Security and Quality Context:** This fragment will trigger three alerts: Vulnerability (hardcoded password), Code Smell (unused variable), and Bug (dead code).

![Vulnerable code in Nano](images/02_vulnerable_code.png)
*vulnerable.py script edited with Nano.*

#### Phase 4: SonarQube Deployment
Deployment of SonarQube *lts-community* using Docker:

```bash
sudo docker run -d --name sonarqube -p 9000:9000 sonarqube:lts-community
```

##### Troubleshooting: Virtual Memory Limit
If the engine fails due to Kernel limits, apply:
```bash
sudo sysctl -w vm.max_map_count=262144
```

#### Phase 5: Security Configuration and Access via Web UI
1. **Initial Authentication:** Login at `http://localhost:9000` with `admin/admin`.
![SonarQube Login](images/03_sonarqube_login.png)

2. **Credential Hardening:** Mandatory password change.
![Forced password update](images/04_password_update.png)

3. **Access Token Generation (Best Practice):** Create a User Token named `Vulnerabilities`.
![Token Generation in UI](images/05_token_generation.png)
![Token Created Successfully](images/06_token_created.png)

#### Phase 6: Static Code Analysis (SAST) using SonarScanner
Run the scanner in the project directory:

```bash
sudo docker run --rm \
    --network host \
    -v "$(pwd):/usr/src" \
    sonarsource/sonar-scanner-cli \
    -Dsonar.projectKey=Analisis-Seguridad-C \
    -Dsonar.sources=. \
    -Dsonar.host.url=http://localhost:9000 \
    -Dsonar.login=squ_80f32df6860b0817c39a0dc4b2cb7f1d88a27873 \
    -Dsonar.python.version=3 \
    -Dsonar.scm.disabled=true
```

#### Phase 7: Creating a Quality Profile and SAST Rules
Create a custom profile for Python called `Vulnerabilities` extending `Sonar way`.
![Profile Creation](images/07_quality_profile_creation.png)

Activate rules for `OS command injection` and `SQL injection`.
![Activate More Button](images/08_activate_more_rules.png)

Set the profile as default.
![Set as Default Profile](images/09_set_as_default.png)

#### Phase 8: Results Review and Quality Gates
The scan results in a **"Failed"** status due to detected critical items.
![Dashboard Results](images/10_dashboard_results.png)

*   **1 New Bug:** Unreachable code.
*   **2 New Code Smells:** Unused variable.
*   **Added Debt (20min):** 20 minutes of technical debt.

#### Phase 9: Remediation and Quality Gate Validation (Passed)
Code refactor to use environment variables and clean the logic:

```python
import os
def funcion_segura():
    password_segura = os.environ.get("DB_PASSWORD", "not_configured")
    if password_segura != "not_configured":
        print("Authentication configured securely.")
        return True
    print("Password environment variable missing.")
    return False
```

![Source code refactoring in Nano](images/11_fixed_code_remediation.png)

After re-scanning, the status changes to **"Passed"**.
![Activity Graph and Quality Gate Passed](images/12_activity_graph_passed.png)

---

### Conclusions and Added Value
SAST analysis allows cost reduction and quality standardization through the **Shift-Left Security** philosophy.

#### Demonstrated Technical Skills
* **DevSecOps:** Automatic security audits.
* **Docker:** Critical infrastructure deployment.
* **SAST:** Rule configuration and Quality Gates.
* **Python Security:** Remediation of common vulnerabilities.

---

### 👤 Author
* **Ismael A. Pérez Segura** - [LinkedIn](https://www.linkedin.com/in/ismael-perez-segura/)

### ⚠️ Legal Disclaimer
This project is for educational purposes only. The author is not responsible for any misuse of the information provided.
