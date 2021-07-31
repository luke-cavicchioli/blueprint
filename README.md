# THIS SCRIPT IS NOT YET WORKING

# blueprint
Create files from template folder.

Nothing fancy - just a simple country script moving those templates around.
Copies the template file to the current directory, copies other accessory files,
copy init script, then executes it. For further details about accessory files
and init scripts, see "Directory structure".

## Install
Clone the folder, copy blueprint.py to a folder in your path,
then add execute permission.
For example, if your scripts are stored in `~/bin`:
```bash
$ git clone https://github.com/luke-cavicchioli/blueprint.git
```

Then,

```bash
$ cd blueprint
$ cp blueprint.py ~/blueprint
$ chmod +x ~/blueprint
```
## Usage
Run
```bash
$ blueprint list
```
to see all available templates, then run
```bash
$ blueprint create template
```
to create it.

### Global options
`--topdir`: specify the top directory where the templates are stored. The
default value is `~/Templates`

### `create` options
`--no-script`: do not execute the init script
`--no-accessories`: do not bring in accessory files

## Directory structure
Every file in the specified template directory (either the default
`~/Templates` or the one specified by `--topdir`) that does not start with a
`.` is considered a template.
For each template file of the form `name.extension` a file named `.name` and
a directory named `.name.d` are searched. If found, the files in `.name.d`
are copied in the current folder (not the folder itself), then `.name` is
executed.
