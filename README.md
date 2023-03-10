# Template Python OSS

> A cookiecutter template for open source Python projects hosted on Github.

# Quick Start

In order to get started, it is NOT necessary to clone the git repository of the template. Instead, run the commands below:

1. Make sure `cookiecutter` is installed:

```console
python3 -m pip install --user cookiecutter
```

2. Generate new project in an interactive manner:

```console
cookiecutter gh:quara-dev/python-template-oss
```

> When running the command, you will be prompted for option values. When no value is provided, default value (displayed between `[]`) is used.

# GitHub Project configuration

Before pushing the first commit to remote repository, some pre-requisites must be met. 

## Github Actions Configuration

1. Create new SSH keypair:

```console
ssh-keygen -t ed25519 -f id_ed25519 -N "" -q -C ""
```

2. Copy public key to add new Deploy Key to Github project:

```console
cat id_ed25519.pub
```

> Deploy key must be named `COMMIT_KEY`

3. Copy private key to add new Action Secret to Github project:

```console
cat id_ed25519
```

> Secret must be named `COMMIT_KEY`

4. Grant "Read and Write" workflow permission in `Action>General` section.

5. Configure Github Pages to be deployed from Github action.

## Sonarcloud configuration

1. Import project from Github into Sonarcloud

2. Obtain project token from Sonarcloud

2. Copy token to add new Action Secret to Github project

> Secret must be named `SONAR_TOKEN`
