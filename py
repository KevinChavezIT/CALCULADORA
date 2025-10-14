import os
from pathlib import Path
import jinja2


vm_environment = os.getenv("VM_ENVIRONMENT").upper()
path_env = ""
if vm_environment == "TSEC" or vm_environment == "DSEC":
    path_env = "0-dev"
elif vm_environment == "PREC" or vm_environment == "POEC" :
    path_env = "1-prod"

BUILD_SOURCE_DIRECTORY = os.getenv("BUILD_SOURCESDIRECTORY")
PIPELINE_WORKSPACE = os.getenv("PIPELINE_WORKSPACE")
REPO_NAME = os.getenv("REPOSITORY_NAME")
BASE_DIR = Path(BUILD_SOURCE_DIRECTORY, REPO_NAME)
TEMPLATE_DIR = Path(BASE_DIR, "template")
MAIN_PATH = Path(BASE_DIR, "terraform", path_env, "2_01_vm.tf")

print(BUILD_SOURCE_DIRECTORY)
print(MAIN_PATH)


def get_vm_config(vm_environment, vm_type):
    configurations = {
        "PREC": {
            "NA": {"memory": "4096", "num_cpus": "2", "capacity": "xlow"},
            "NA": {"memory": "8192", "num_cpus": "4", "capacity": "low"},
            "NA": {"memory": "12288", "num_cpus": "8", "capacity": "medium"},
            "NA": {"memory": "16384", "num_cpus": "12", "capacity": "high"},
            "NA": {"memory": "32768", "num_cpus": "16", "capacity": "xhigh"},
        },
        "TSEC": {
            "NA": {"memory": "4096", "num_cpus": "2", "capacity": "low"},
            "NA": {"memory": "8192", "num_cpus": "4", "capacity": "medium"},
            "NA": {"memory": "16384", "num_cpus": "8", "capacity": "high"},
        },
        "DSEC": {
            "NA": {"memory": "4096", "num_cpus": "2", "capacity": "low"},
            "NA": {"memory": "8192", "num_cpus": "4", "capacity": "medium"},
            "NA": {"memory": "16384", "num_cpus": "8", "capacity": "high"},
        },
        "POEC": {
            "NA": {"memory": "4096", "num_cpus": "2", "capacity": "low"},
            "NA": {"memory": "8192", "num_cpus": "4", "capacity": "medium"},
            "NA": {"memory": "16384", "num_cpus": "8", "capacity": "high"},
        },
    }
    return configurations.get(vm_environment, {}).get(vm_type, {})


def get_template_path(vm_os, environment):
    if environment in ["PREC", "POEC"]: 
        if vm_os == "W":
            return TEMPLATE_DIR / "template_windows.j2"
        elif vm_os == "L":
            return TEMPLATE_DIR / "template_linux.j2"
    elif environment in ["TSEC", "DSEC"]:
        if vm_os == "W":
            return TEMPLATE_DIR / "template_windows_test.j2"
        elif vm_os == "L":
            return TEMPLATE_DIR / "template_linux_test.j2"
    else:
        raise ValueError(f"No tf template exists for {vm_os} in {environment}.")


def get_disks(vm_os, vm_rol, vm_disk_d, vm_disk_dy):
    if vm_os == "W":
        vm_disk_d = os.getenv("VM_DISK_D")
        #vm_disk_g = os.getenv("VM_DISK_G")
        #vm_disk_h = os.getenv("VM_DISK_H")
        disks = [
            {"name": "uno", "label": "disk0", "size": 151, "unit_number": 0},
            {"name": "dos", "label": "disk1", "size": vm_disk_d, "unit_number": 1},

        ]
        if vm_rol == "DB":
            vm_disk_f = os.getenv("VM_DISK_F")
            vm_disk_g = os.getenv("VM_DISK_G")
            vm_disk_h = os.getenv("VM_DISK_H")
            disks.extend(
                [
                    {"name": "tres", "label": "disk2", "size": 5, "unit_number": 2},
                    {
                        "name": "cuatro",
                        "label": "disk3",
                        "size": vm_disk_f,
                        "unit_number": 3,
                    },
                    {
                        "name": "cinco",
                        "label": "disk4",
                        "size": vm_disk_g,
                        "unit_number": 4,
                    },
                    {
                        "name": "seis",
                        "label": "disk5",
                        "size": vm_disk_h,
                        "unit_number": 5,
                    },
                ]
            )
    elif vm_os == "L":
        vm_disk_dy = os.getenv("VM_DISK_F")
        #vm_disk_h = os.getenv("VM_DISK_H")

        disks = [
            {"name": "uno", "label": "disk0", "size": 80, "unit_number": 0},
            {"name": "dos", "label": "disk1", "size": vm_disk_dy, "unit_number": 1},
            {"name": "tres", "label": "disk2", "size": vm_disk_d, "unit_number": 2},
            #{"name": "cuatro", "label": "disk3", "size": vm_disk_h, "unit_number": 3},

        ]

    else:
        raise ValueError(f"No configuration available for: '{vm_os}'.")
    return disks


def render_template(vm_hostname,vm_mem,vm_cpu,vm_os,vm_rol,vm_environment,vm_type,to_db,config,disks,ipv4_gateway,ipv4_address,ipv4_netmask,vm_vlan,vm_template,vm_granja,vm_datastore,vm_nomapl,vm_lidini,vm_owner,vm_gs,vm_rg,vm_tribu,vm_firmware):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath=str(TEMPLATE_DIR))
    )
    #template_name = "template_windows.j2" if vm_os == "W" else "template_linux.j2"
    #template = env.get_template(template_name)

    template_path = get_template_path(vm_os, vm_environment)
    template = env.get_template(template_path.name)

    resource = template.render(
        name=vm_hostname,
        #memory=config["memory"],
        mem=vm_mem,
        vm_type=vm_type,
        so=vm_os,
        rol=vm_rol,
        location=vm_environment[-2:],
        environment=vm_environment[:2],
        to_db=to_db,
        resource_number=vm_hostname[-3:],
        capacity=config["capacity"],
        #num_cpus=config["num_cpus"],
        cpu=vm_cpu,
        disks=disks,
        ipv4_gateway=ipv4_gateway,
        ipv4_address=ipv4_address,
        ipv4_netmask=ipv4_netmask,
        name_vlan=vm_vlan,
        vm_template=vm_template,
        vm_granja=vm_granja,
        vm_datastore=vm_datastore,
        vm_nomapl=vm_nomapl,
        vm_lidini=vm_lidini,
        vm_owner=vm_owner,
        vm_gs=vm_gs,
        vm_rg=vm_rg,
        vm_tribu=vm_tribu,
        vm_firmware=vm_firmware,


    )
    return resource


def main():

    vm_nomapl = os.getenv("VM_NOM_APL")
    vm_lidini = os.getenv("VM_LID_INI")
    vm_owner = os.getenv("VM_OWNER")
    vm_gs = os.getenv("VM_GRUPO_SOP")
    vm_rg = os.getenv("VM_SOPORTE")
    vm_tribu = os.getenv("VM_TRIBU")
    vm_firmware = os.getenv("VM_FIRMWARE")
    vm_disk_d = os.getenv("VM_DISK_D")
    vm_disk_dy = os.getenv("VM_DISK_F")
    #vm_disk_g = os.getenv("VM_DISK_G")
    #vm_disk_h = os.getenv("VM_DISK_H")
    vm_mem = os.getenv("VM_MEM")
    vm_cpu = os.getenv("VM_CPU")
    vm_datastore = os.getenv("VM_DATASTORE")
    vm_rol = os.getenv("VM_ROL").upper()
    vm_so = os.getenv("VM_SO").upper()
    vm_type = os.getenv("VM_TYPE").upper()
    vm_template = os.getenv("VM_TEMPLATE")
    vm_vlan = os.getenv("VM_VLAN")
    vm_granja = os.getenv("VM_GRANJA")
    to_db = "false"
    if vm_rol == "DB":
        to_db = "true"
    vm_hostname = os.getenv("VM_HOSTNAME")
    ipv4_address = os.getenv("IP_ADDRESS")
    ipv4_gateway = os.getenv("IPV4_GATEWAY")
    ipv4_netmask = os.getenv("IPV4_NETMASK")
    config = get_vm_config(vm_environment, vm_type)
    if not config:
        raise ValueError(
            f"No configuration available for '{vm_environment}' with type '{vm_type}'."
        )
    disks = get_disks(vm_so, vm_rol, vm_disk_d, vm_disk_dy)
    resource = render_template(
        vm_hostname,
        vm_so,
        vm_rol,
        vm_environment,
        vm_type,
        to_db,
        config,
        disks,
        vm_mem,
        vm_cpu,
        ipv4_gateway,
        ipv4_address,
        ipv4_netmask,
        vm_vlan,
        vm_template,
        vm_granja,
        vm_datastore,
        vm_nomapl,
        vm_lidini,
        vm_owner,
        vm_gs,
        vm_rg,
        vm_tribu,
        vm_firmware,
    )

    # Verificar si el recurso ya existe en el archivo main.tf
    vldcn = resource.split("\n")[1]
    try:
        with open(MAIN_PATH, "r") as file:
            template_content = file.read()
        if vldcn in template_content:
            raise NameError(
                f"El nombre de recurso {vm_hostname} ya existe en la configuración!!!"
            )
    except FileNotFoundError:
       pass


    # Agregar recurso al archivo main.tf
    with open(MAIN_PATH, "a") as file:
        file.write(resource)
    print(f"Plantilla añadida al archivo '{MAIN_PATH}' con éxito.")


if __name__ == "__main__":
    main()
