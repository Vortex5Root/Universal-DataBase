<h1 align="center">Universal-DataBase</h1>

<p align="center">
    <a href="https://github.com/Vortex5Root/Universal-DataBase/releases"><img alt="Dynamic TOML Badge" src="https://img.shields.io/badge/dynamic-toml?url=https%3A%2F%2Fraw.githubusercontent.com%2FVortex5Root%2FUniversal-DataBase%2Fmain%2Fpyproject.toml&query=%24.tool.poetry.version&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAMAAAAolt3jAAAAtFBMVEVHcEyWYTihdkuXYzrBjlqhbkHepWuzglG8hFGWYjmzglHepmz3z5iygVCWYjmWYjmxgVDsvorMlmDepmybaD2oe02ufU2leUzdpWqzglGfdUrgqnH616j%2F4LKWYjmvf1C3hVPepmyWYjmWZDuWYjmzglGWYjmwfk7fp22aZjz93a7VoGmpfFKdbEe4hlTFkFzwxZH30aDpuYO%2BnICUbUbGkl3jrnbjr3eSYjuuiWzNq4fjvI5PAatoAAAAJXRSTlMA4v34FBH4Jwwn4l8IXFG6%2FrWcv2PCZqdJxeX291Ci4uVQ5eQoZPLoqAAAAIxJREFUCNdFzscCgjAQBNA1JIAGVMDeW0iEAPb6%2F%2F9lCuqc9s1eBkDHpxTDN8E8mroJ9S1G0Sw7noSbrAMAHLvidshMERPwVlUuxF0Vb7ltgtdi5VUV%2BetcNAwZKyv%2BeP7J%2BD6VRaq5rKmiOUGoW3OzAzxEF2npLIgaGPbN1%2Bm07S4SjvkPOnjQI%2Bb4AGCaEYNClUKKAAAAAElFTkSuQmCC&label=Package%20Version"></a>
</p>

-------

<p align="center">
    <a href="https://github.com/Vortex5Root/Universal-DataBase/blob/master/LICENSE"><img src="https://img.shields.io/github/license/Vortex5Root/Universal-DataBase.svg" alt="License"></a>
    <a href="https://github.com/Vortex5Root/Universal-DataBase/releases"><img src="https://img.shields.io/github/downloads/Vortex5Root/Universal-DataBase/total.svg" alt="GitHub all releases"></a><br>
    <a href="https://github.com/Vortex5Root/Universal-DataBase/network"><img src="https://img.shields.io/github/forks/Vortex5Root/Universal-DataBase.svg" alt="GitHub forks"></a>
    <a href="https://github.com/Vortex5Root/Universal-DataBase/stargazers"><img src="https://img.shields.io/github/stars/Vortex5Root/Universal-DataBase.svg" alt="GitHub stars"></a>
    <a href="https://github.com/Vortex5Root/Universal-DataBase/watchers"><img src="https://img.shields.io/github/watchers/Vortex5Root/Universal-DataBase.svg" alt="GitHub watchers"></a><br>
    <a href="https://github.com/Vortex5Root/Universal-DataBase/issues"><img src="https://img.shields.io/github/issues/Vortex5Root/Universal-DataBase.svg" alt="GitHub issues"></a>
    <a href="https://github.com/Vortex5Root/Universal-DataBase/pulls"><img src="https://img.shields.io/github/issues-pr/Vortex5Root/Universal-DataBase.svg" alt="GitHub pull requests"></a>
    <a href="https://github.com/Vortex5Root/Universal-DataBase/commits/master"><img src="https://img.shields.io/github/last-commit/Vortex5Root/Universal-DataBase.svg" alt="GitHub last commit"></a>
</p>

<h2 align="center">Introduction to the Documentation</h2>

> **The Universal-DataBase project provides a unified interface for managing SQLite and Redis databases. It simplifies database operations by offering a consistent API for CRUD operations, dynamic table creation, and model management.** 

<h2 align="center">Index</h2>

| topic | sub-topic | 
| --- | --- |
| [Requirements](#requirements) | |

<h2 align="center">Requirements</h2>

| Name | Version | Description |
| --- | --- | --- |
| [![Linux](https://img.shields.io/badge/Linux-A81D33?style=for-the-badge&logo=linux&logoColor=ffffff)](https://www.linux.org/) | 5.14.0 | Linux is a family of open-source Unix-like operating systems based on the Linux kernel. |
| [![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/) | >=3.11 | Python is an interpreted high-level general-purpose programming language. |
| [![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json?style=for-the-badge)](https://python-poetry.org/) | 1.1.8 | Poetry is a tool for dependency management and packaging in Python. |

<h2 align="center">Documentation</h2>

## Features
- **Hybrid Database Support**: Seamlessly work with SQLite and Redis.
- **Dynamic Model Management**: Automatically create tables or models based on your data classes.
- **CRUD Operations**: Simplified methods for Create, Read, Update, and Delete.
- **Migration Support**: Easy migration for Redis databases.

## Usage

### Initializing the Database
```python
from universal_database import UniversalDatabase

db = UniversalDatabase(type_db="sqlite", connection="example.db")
```

### Defining a Model
```python
from universal_database import UniversalModel, pk
from typing import Annotated

class ExampleModel(UniversalModel):
    id: Annotated[int, pk()]
    name: str
    value: float
```

### Performing CRUD Operations
#### Create and Save
```python
example = ExampleModel(id=1, name="Test", value=10.5)
db.load_UniversalModel(example).save()
```

#### Read
```python
records = db.load(ExampleModel)
print(records)
```

#### Update
```python
example.name = "Updated Name"
example.save()
```

#### Delete
```python
example.delete()
```

## Advanced Features

### Redis-Specific Features
- Use `Migrator` for running migrations:
  ```python
  db.migrate()
  ```

### SQLite-Specific Features
- Automatically creates tables based on model definitions.

<h2 align="center">Acknowledgements</h2>

<p align="center">
    <br>[Coder]<br>
    <a href="https://github.com/Vortex5Root"><img src=https://avatars.githubusercontent.com/u/102427260?s=200&v=4 width=50 style="border-radius: 50%;"><br>Vortex5Root <br><b>        {Full-Stack Software Engineer}</b></a><br>
    <br>[Colaboration With PandemicOfNukes]<br>
    <a href="https://github.com/PandemicOfNukes"><img src=https://avatars.githubusercontent.com/u/59929476?s=200&v=4 width=50 style="border-radius: 50%;"><br>PandemicOfNukes <br><b>        {Student}</b></a><br><br>
</p>
