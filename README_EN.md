# Code Quality Analysis and Integration with SonarQube

## 📌 General Overview
This repository documents a professional workflow focused on the configuration, integration, and implementation of **SonarQube** for continuous code quality inspection, bug detection, and security vulnerability identification (SAST).

The main objective is to demonstrate a robust and standardized approach applicable to real business environments, thus ensuring a secure and maintainable software development life cycle (SDLC).

## 🎯 Project Objectives
* **Static Code Analysis:** Integrate SonarQube to review the codebase health.
* **Traceability and Documentation:** Meticulously record every command, error, and solution found during configuration.
* **Production-Level Quality:** Establish strict *Quality Gates* and thresholds.
* **Professional Portfolio:** Serve as a technical reference of skills in DevSecOps methodologies for recruitment.

---

## 🛠️ Implementation and Activity Log

This section details chronologically each step taken to deploy and use SonarQube, including technical evidence for each phase.

### Phase 1: Repository Initialization and Documentation

**Starting Date:** March 2026

We begin with the initialization of the repository and the creation of the base structure for project documentation.

*Note: This section will be continuously updated as we progress with installation, repository scanning, and vulnerability resolution.*

### Phase 2: Installation and Configuration on Kali Linux (VM)

To ensure an isolated and controlled analysis environment, the SonarQube infrastructure is deployed on a virtual machine (VM) equipped with **Kali Linux**. This decision leverages its ecosystem oriented towards offensive and defensive security.

#### 1. Common Prerequisites
We recommend updating basic packages in the VM and installing necessary dependencies:

```bash
sudo apt update && sudo apt upgrade -y
```

#### 3. Docker and Docker Compose Installation
Since we opted for a containerized deployment (the best practice for isolation and ease of maintenance), we install Docker and its container orchestrator on the virtual machine:

```bash
sudo apt install docker.io docker-compose -y
```

#### 4. Enable and Start Docker Service
To ensure the Docker daemon starts automatically with the system and runs immediately in the current session, we execute:

```bash
sudo systemctl enable docker --now
```

![Enabling Docker](images/01_docker_kali.png)
*Result of enabling the Docker service in the system.*

### Phase 3: Preparation of Test Code (Vulnerable)

To demonstrate the effectiveness of **SonarQube** in detecting different types of issues in early stages of the life cycle (SAST), a small Python script (`vulnerable.py`) has been developed containing three different types of issues: vulnerabilities, logic bugs, and code smells (dirty code).

#### Source Code (`vulnerable.py`)
The script implements a mock functionality with several clear errors on purpose:

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

> **🛡️ Security and Quality Context:** This simple fragment will trigger three different alerts in SonarQube:
> 1. **Vulnerability:** Storing *hardcoded* passwords directly in the source code (highly critical).
> 2. **Code Smell:** Declaration of variables that are never used, which clutters and confuses future maintenance.
![Vulnerable code in Nano](images/02_vulnerable_code.png)

*Script `vulnerable.py` edited with Nano, showing security and quality issues.*

### Phase 4: SonarQube Deployment

To start the **SonarQube** instance, we proceed to download the official image and deploy it in a Docker container running in the background (`-d` or detached mode). We have selected the *Long-Term Support (lts-community)* version for being free and the most stable for corporate production environments. Python, being a language natively supported by the *Community* edition, will allow us to perform this SAST without requiring additional licenses.

We execute the following command on the virtual machine:

```bash
sudo docker run -d --name sonarqube -p 9000:9000 sonarqube:lts-community
```

* **`-d`**: Runs the container in the background.
* **`--name sonarqube`**: Assigns a clear and descriptive name to the container for easier subsequent management.
* **`-p 9000:9000`**: Exposes the SonarQube web control panel to the host on port 9000.
* **`sonarqube:lts-community`**: Tag of the official image maintained by SonarSource (Community LTS version).
Once the container finishes starting all processes (such as the internal Elasticsearch engine and the web DB), the interface will be available by navigating to `http://localhost:9000` or your VM's IP (`http://<KALI_IP>:9000`).

#### Troubleshooting: Virtual Memory Limit
It is highly likely that during container startup, the **Elasticsearch** engine (integrated in SonarQube) fails and the container stops (`Exited (78)` or similar). This is because standard kernel measures in distributions like Kali Linux are insufficient for fast indexing.

To solve this and allow SonarQube to start correctly, we apply the following adjustment to the mapped virtual memory area limits (*mmap*), a mandatory configuration in production environments:

```bash
sudo sysctl -w vm.max_map_count=262144
```

> **💡 Note:** After applying this command, the container will be able to start normally (you can verify this with `docker logs sonarqube` or by restarting the container if it had stopped with `docker start sonarqube`).

### Phase 5: Security Configuration and Access in the Web Interface

Once we verify that the port is serving correctly, we access the web console to establish the security bases of the environment:

1. **Initial Authentication:**
We head to `http://localhost:9000` (or the corresponding VM IP) and log in with default SonarSource credentials:
    * **User:** `admin`
    * **Password:** `admin`

![SonarQube Login](images/03_sonarqube_login.png)
*Standard SonarQube login screen.*

2. **Credential Hardening:**
As any good security policy dictates, the platform immediately forces a change of the default password. We replace the password with a strong and secure one.

![Forced password update](images/04_password_update.png)
*Admin password change process.*

3. **Access Token Generation (Best Practice):**
We will avoid using the user/password combo to send code analysis reports (a practice totally discouraged in CI/CD and automation). Instead, we will generate a User Authentication Token:
    * Go to **Administration > Security > Users**.
    * Select the **Tokens** option on our user.
    * Generate a *User Token* naming it `Vulnerabilities`.

![Token Generation in UI](images/05_token_generation.png)
*Security tokens and access administration panel.*

![Token Created Successfully](images/06_token_created.png)
*Successfully generated token.*

### Phase 6: Static Code Analysis (SAST) using SonarScanner

With the platform ready and secured, we will run **SonarScanner CLI**, the official tool responsible for collecting the source code, parsing it, and sending the metadata to the SonarQube server to look for vulnerabilities.

We will also do this using an ephemeral Docker container (`--rm`), keeping the environment clean without needing to install the Java binary of the *scanner* locally on the host.

Staying in the directory where we created our `vulnerable.py` file, we execute:

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

**Docker Command Analysis:**
* **`--rm`**: Deletes the container instantly once the analysis finishes, saving storage.
* **`--network host`**: Allows the scanner container to comfortably access `localhost:9000` (where our previously deployed SonarQube server listens).
* **`-v "$(pwd):/usr/src"`**: Mounts our current directory where the source code is inside the container.
* **`-Dsonar.projectKey`**: Defines our project's unique identifier on the SonarQube server (`Analisis-Seguridad-C`).
* **`-Dsonar.sources=.`**: Tells SonarScanner which files to inspect (in this case the current directory `.` we just mounted in the volume).
* **`-Dsonar.login=...`**: Instead of raw passwords in bash, we use the Token generated in *Phase 5* to authenticate robustly.
* **`-Dsonar.python.version=3`**: Forces the Python analyzer to use Python 3 rules and syntax.
* **`-Dsonar.scm.disabled=true`**: Disables the Source Control Management check (SCM/Git), very useful if you are analyzing code from a folder that has not yet been initialized as a local Git repository (avoids `blame` errors).

### Phase 7: Creating a Quality Profile and Activating Specific SAST Rules

To ensure SonarQube accurately detects Command Injections (OS Command Injection) or SQL Injections, we need to ensure corresponding rules are activated. By default, SonarQube uses the *"Sonar way"* profile, but we will create a custom one to force the activation of the most critical vulnerabilities.

1. **Custom Profile Creation:**
Navigate to the **Quality Profiles** tab in the top menu. We create a new profile for the **Python** language:
    * **Name:** `Vulnerabilidades`
    * **Language:** `Python`
    * **Profile to extend:** `Sonar way (Built-in)` (this inherits standard rules and allows us to add new ones).

![Profile Creation](images/07_quality_profile_creation.png)
*Creation of a new Quality Profile extending the default one.*

2. **Activating Injection Rules (OS Command & SQL):**
Within the new `Vulnerabilidades` profile, we click the **"Activate More"** button located below the active/inactive rule statistics.

![Activate More Button](images/08_activate_more_rules.png)
*Accessing the interactive rule search to enable them in our profile.*

In the rule search bar, we enter the following terms and click **"Activate"** on the Python rules that appear:
* `OS command injection` (looking for those mentioning dependencies like `os.system` or `subprocess`).
* `SQL injection` (to prevent future flaws in database queries).

3. **Set as Default Profile:**
Once the necessary rules are activated, we must ensure SonarScanner uses this profile automatically for all Python projects. In the main *Quality Profiles* list, click the gear next to the `Vulnerabilidades` profile and select **"Set as Default"**.

![Set as Default Profile](images/09_set_as_default.png)
*Configuration of the new extended profile as the default for Python code analysis.*

This way, we have armored our configuration, ensuring our `vulnerable.py` script is audited with the highest rigor possible.

### Phase 8: Results Review and Quality Gates

After running the `sonar-scanner-cli` container, the results are automatically sent to our SonarQube web server, processed in real time. By opening our project tab in the main *Dashboard*, we will visualize the critical audit showing the issues inserted in *Phase 3*:

![Dashboard Results](images/10_dashboard_results.png)
*Main project dashboard showing Quality Gate failure.*

**Technical Report Analysis (Key Metrics):**

1. ❌ **Quality Gate "Failed":**
   The overall status of the scan is **"Failed"** (represented by the red box). At a business level, this is the most critical indicator (*Go/No-Go*). It means the uploaded code **does not meet the minimum quality and security standards** defined by the organization, automatically preventing and blocking its passage to production in an automated pipeline (CI/CD).

2. 🐛 **1 New Bug (Reliability Rating - C):**
   The semantic analysis engine detected the introduced logic flaw (the `print()` clause located after the `return True` block). This highlights that SonarQube possesses precise *Control Flow Analysis*: it not only understands syntax but the execution logic of the language, alerting that this code block is unreachable (Dead Code).

3. ☢️ **2 New Code Smells (Maintainability Rating - C):**
   It has located design anti-patterns and "dirty" code. For example, the declaration of `variable_inutil = 42` that is never used. Maintainability rules ensure the code is clean and readable for future refactorings.

4. ⏱️ **Added Debt (20min):**
   SonarQube automatically calculates and quantifies the project's **Technical Debt**. The estimate indicates that it would take a software engineer approximately 20 minutes to understand and patch all these flaws (delete variables, fix control flow, solve static passwords, etc.) so the code complies with the mandatory "A" level. This metric is fundamental in *Agile* development to plan refactoring *sprints*.

### Phase 9: Remediation and Quality Gate Validation (Passed)

The DevSecOps cycle doesn't end in finding the flaw, but in patching it and verifying that the software is now safe for deployment. We proceed to refactor our `vulnerable.py` script, applying the secure code principles SonarQube required of us:

#### Refactored Code (`vulnerable.py`)
```python
import os

def funcion_segura():
    # 1. VULNERABILITY REMEDIATION: Never hardcode passwords.
    # We use environment variables.
    password_segura = os.environ.get("DB_PASSWORD", "not_configured")
    
    # 2. CODE SMELL REMEDIATION: Removed unused variable.
    
    # 3. LOGIC BUG REMEDIATION: Fixed 'return' order to avoid dead code.
    if password_segura != "not_configured":
        print("Authentication configured securely.")
        return True
        
    print("Password environment variable missing.")
    return False

if __name__ == "__main__":
    funcion_segura()
```

![Source code refactoring in Nano](images/11_fixed_code_remediation.png)
*Modified source code, having removed embedded credentials, unreachable block, and anti-patterns.*

Once changes are applied to the file, we run the `sonar-scanner-cli` container again with the exact same command from *Phase 6*. The scanner will re-evaluate the entire project and send the new analysis *commit* to the server:

![Activity Graph and Quality Gate Passed](images/12_activity_graph_passed.png)
*Project activity history in SonarQube.*

**Remediation Analysis:**
As we can see in the Activity Graph, the lines marking issues (Bugs in light blue and Code Smells in dark blue dashed line) have **dropped drastically to zero** in the last record.

The panel on the right confirms the milestone: **Quality Gate: Passed**.
Our code now complies with quality regulations, is maintainable (Technical Debt eliminated), and is completely secure (0 vulnerabilities), allowing the automatic *pipeline* to give the green light for a secure deployment to production environments.

---

## Conclusions and Added Value

This project is not just a technical test of a tool; it is a practical implementation of the **Shift-Left Security** philosophy. By integrating static application security testing (SAST) in early development phases, companies gain:

1.  **Cost Reduction:** It is up to 100 times cheaper to fix a vulnerability in the development phase than after a security incident in production.
2.  **Quality Standardization:** Ensures that all team code maintains a homogeneous style and security by applying *Quality Profiles* and *Quality Gates*.
3.  **Regulatory Compliance:** Facilitates compliance with standards like ISO 27001 or GDPR by demonstrating active security review processes.

### Demonstrated Technical Skills (for CV/Portfolio)

*   **DevSecOps:** Implementation of automatic security audits in the software life cycle.
*   **Virtualization and Containers:** Deployment of complex infrastructure (SonarQube + Elasticsearch + DB) using **Docker** and Linux Kernel limit management.
*   **SAST Analysis:** Advanced configuration of static rule engines, creation of custom quality profiles, and establishment of security thresholds (*Quality Gates*).
*   **Python Security:** Knowledge of common vulnerabilities (Hardcoded secrets, Injections, Dead Code) and secure remediation techniques (Environment Variables, logic refactoring).
*   **Troubleshooting:** Resolution of performance and memory issues in virtualized environments (Kali Linux VM).

---

### 👤 Author
* **Ismael A. Pérez Segura** - [LinkedIn](https://www.linkedin.com/in/ismael-perez-segura/)

---

### ⚠️ Legal Disclaimer
This project is for educational and ethical security testing purposes only. Unauthorized access to computer systems is illegal. The author is not responsible for any misuse of the information or code provided in this repository.

---
*This repository has been documented for professional purposes to demonstrate technical capabilities in code auditing and offensive/defensive security.*
