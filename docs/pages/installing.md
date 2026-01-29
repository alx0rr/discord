# 📥 **Installation Guide for UDISCORD**

To get started with UDISCORD, follow the installation steps below.

## Prerequisites

Before you install UDISCORD, ensure you have the following:

- **Python 3.6+** – UDISCORD requires Python 3.6 or higher.
- **Git** – For cloning the repository (if needed).
- **Pip** – Python's package manager.

## Installation Methods

### 1. Clone the Repository via Git

If you'd like to have the full source code and easily contribute or modify it, you can clone the repository.

#### Steps:

1. Clone the repository using Git:

    ```bash
    git clone https://github.com/alx0rr/discord.git
    ```

2. Navigate into the project directory and install the dependencies:

    ```bash
    cd discord
    pip install -r requirements.txt
    ```

3. To use the UDISCORD:

    ```python
    import udiscord
    ```

---

### 2. Install via `pip` from Git Repository

If you prefer not to manually clone the repository and just want to install the latest version directly, you can install it via pip from the GitHub repository.

#### Steps:

1. Install UDISCORD using pip from Git:

    ```bash
    pip install git+https://github.com/alx0rr/discord.git
    ```

2. After installation, you can use udiscord with:

    ```python
    import udiscord
    ```

---

### 3. Install via `pip` from PyPI

For a simpler installation, you can install UDISCORD directly from PyPI (Python Package Index)

#### Steps:

1. Install UDISCORD from PyPI:

    ```bash
    pip install udiscord
    ```

2. To use the UDISCORD:

    ```python
    import udiscord
    ```

---

## Troubleshooting

If you encounter any issues during installation, here are some common problems and solutions:

### Missing Dependencies

If you receive an error about missing dependencies, install it via pip:
```bash
pip install some_module
```


