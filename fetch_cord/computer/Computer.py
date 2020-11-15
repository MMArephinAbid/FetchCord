
import os
from sys import platform, exit
from typing import Dict, List
from ..run_command import run_command
from ..args import parse_args

from .get_infos import get_infos
from .cpu.get_cpu import get_cpu
from .cpu.Cpu_interface import Cpu_interface
from .gpu.get_gpu import get_gpu
from .gpu.Gpu_interface import Gpu_interface, get_gpuid

args = parse_args()


class Computer:
    parseMap: Dict
    componentMap: Dict

    idsMap: Dict

    os: str
    neofetchwin: bool = False
    neofetch: bool = False
    values: str
    laptop: bool = False

    @property
    def memory(self) -> str:
        return self.get_component_line("Memory:")

    @property
    def osinfo(self) -> str:
        return self.get_component_line("OS:")

    @property
    def osinfoid(self) -> str:
        component = self.get_component_line("OS:")
        component = (component.split()[0] + component.split()[1]).lower()
        component_list = self.idsMap[self.idsMap["map"]["OS:"]]

        for comp, id in component_list.items():
            if component.find(comp.lower()) >= 0:
                return id

        print("Unknown {}, contact us on github to resolve this.".format(
            self.idsMap["map"]["OS:"]))

        return component_list["unknown"]

    @property
    def motherboard(self) -> str:
        return self.get_component_line("Motherboard:")

    @property
    def motherboardid(self) -> str:
        return self.get_component_idkey("Motherboard:")

    @property
    def host(self) -> str:
        return self.get_component_line("Host:")

    @property
    def hostid(self) -> str:
        hostsplit = self.host.split()
        host_list: Dict[str, str] = self.idsMap[self.idsMap["map"]["Host:"]]

        for line in hostsplit:
            if line in host_list:
                return line

        # try to get MacBook hostid
        hostid = []
        hostjoin = ' '.join(self.host)
        for numsplit in range(len(hostjoin)):
            if not hostjoin[numsplit].isdigit():
                hostid.append(hostjoin[numsplit])
        hostid = ''.join(hostid)
        hostid = hostid.split()[1]

        if hostid in host_list:
            return host_list[hostid]
        else:
            return host_list["unknown"]

    @property
    def hostappid(self) -> str:
        return self.get_component_id("Host:")

    @property
    def cpu(self) -> str:
        key = "CPU:"
        cpus: List[Cpu_interface] = self.get_component(key)
        temp = []
        for cpu in cpus:
            temp.append(cpu.model)

        return '\n'.join(temp) if len(cpus) > 0 else '{} N/A'.format(key)

    @property
    def cpuid(self) -> str:
        temp: List[Cpu_interface] = self.get_component("CPU:")

        if len(temp) == 0:
            return self.idsMap[self.idsMap["map"]["CPU:"]]["unknown"]
        else:
            return temp[0].get_id(self.idsMap[self.idsMap["map"]["CPU:"]])

    @property
    def gpu(self) -> str:
        key = "GPU:"
        gpus: List[Gpu_interface] = self.get_component(key)
        temp = []
        for gpu in gpus:
            temp.append(gpu.model)

        return '\n'.join(temp) if len(gpus) > 0 else '{} N/A'.format(key)

    @property
    def gpuid(self) -> str:
        return get_gpuid(self.idsMap[self.idsMap["map"]["GPU:"]], self.get_component("GPU:"))

    @property
    def disks(self) -> str:
        return self.get_component_line("Disk")

    @property
    def resolution(self) -> str:
        return self.get_component_line("Resolution:")

    @property
    def theme(self) -> str:
        return self.get_component_line("Theme:")

    @property
    def kernel(self) -> str:
        return self.get_component_line("Kernel:")

    @property
    def packages(self) -> str:
        return self.get_component_line("Packages:")

    @property
    def shell(self) -> str:
        return self.get_component_line("Shell:")

    @property
    def shellid(self) -> str:
        return self.get_component_id("Shell:")

    @property
    def terminal(self) -> str:
        return self.get_component_line("Terminal:")

    @property
    def terminalid(self) -> str:
        return self.get_component_id("Terminal:")

    @property
    def wm(self) -> str:
        return self.get_component_line("WM:")

    @property
    def wmid(self) -> str:
        return self.get_component_line("WM:").split()[0]

    @property
    def font(self) -> str:
        return self.get_component_line("Font:")

    @property
    def de(self) -> str:
        return self.get_component_line("DE:")

    @property
    def deid(self) -> str:
        return self.get_component_line("DE:").split()[0]

    @property
    def dewmid(self) -> str:
        return '\n'.join(self.get_component_line("DE:")+self.get_component_line("WM:"))

    @property
    def desktopid(self) -> str:
        deid = self.deid.lower()
        wmid = self.wmid.lower()

        if deid != "n/a" and deid in self.idsMap[self.idsMap["map"]["DE:"]]:
            return deid

        elif deid == "n/a" and wmid in self.idsMap[self.idsMap["map"]["WM:"]]:
            return wmid
        else:
            print("Unknown DE/WM, contact us on github to resolve this.")
            return 'unknown'

    @property
    def battery(self) -> str:
        return self.get_component_line("Battery:")

    @property
    def lapordesk(self) -> str:
        if self.laptop and self.os != "macos":
            return "laptop"
        else:
            return "desktop"

    def __init__(self):
        super().__init__()

        self.parseMap = {
            'CPU:': get_cpu,
            'GPU:': get_gpu,
            'Disk': self.get_disk,
            'Memory:': self.get_memory,
            'OS:': self.get,
            'Motherboard:': self.get,
            'Host:': self.get,
            'Resolution:': self.get,
            'Theme:': self.get,
            'Kernel:': self.get,
            'Packages:': self.get,
            'Shell:': self.get,
            'Terminal:': self.get,
            'Font:': self.get,
            'DE:': self.get,
            'WM:': self.get,
            'Battery:': self.get
        }

        self.componentMap = {}
        self.idsMap = get_infos()

        self.detect_os()
        self.detect_laptop()
        self.neofetchwin, self.neofetch, self.values = self.detect_neofetch()
        self.neofetch_parser(self.values)

    def updateMap(self):
        self.clearMap()
        self.neofetchwin, self.neofetch, self.values = self.detect_neofetch()
        self.neofetch_parser(self.values)

    def clearMap(self):
        for key in self.componentMap.keys():
            del self.componentMap[key][:]

    def neofetch_parser(self, values: str):
        lines = values.split('\n')
        for i in range(len(lines)):
            line = lines[i]
            for key, detectedFunction in [(key, value) for key, value in self.parseMap.items() if key in line]:
                if key not in self.componentMap:
                    self.componentMap[key] = []
                detectedFunction(
                    self.os, self.componentMap[key], line.rstrip('\n'), key)

    def detect_os(self) -> str:
        if platform == 'linux' or platform == 'linux2':
            self.os = 'linux'
        elif platform == 'darwin':
            self.os = 'macos'
        elif platform == 'win32':
            self.os = 'windows'
        else:
            raise Exception('Not a supported OS !')

        return self.os

    def detect_laptop(self) -> bool:
        if self.os != 'linux':
            self.laptop = False
        else:
            for i in os.listdir('/sys/class/power_supply'):
                if i.startswith("BAT"):
                    self.laptop = True
                    break

        return self.laptop

    def detect_neofetch(self):
        neofetchwin = False
        neofetch = False
        values = None

        if self.os == 'windows':
            try:
                values = run_command(['neofetch', '--noart'])
            except Exception:
                pass
            else:
                neofetchwin = True
        elif not neofetchwin:
            try:
                values = run_command([
                    'neofetch',
                    '--stdout',
                    '--config none' if args.noconfig else ''],
                    shell=(self.os == 'windows'))
            except Exception:
                print(
                    'ERROR: Neofetch not found, please install it or check installation and that neofetch is in PATH.')
                exit(1)
            else:
                neofetch = True
        return (
            neofetchwin, neofetch, values)

    def get_disk(self, os: str, line: List, value: str, key: str):
        """
        Append the Disk info from the given neofetch line to the Disk list

        Parameters
        ----------
        value : str
            Neofetch extracted line
        """

        line.append(value[value.find(key)+len(key)+2:])

    def get_memory(self, os: str, line: List, value: str, key: str):
        """
        Get the memory info from the given neofetch line

        Parameters
        ----------
        value : str
            Neofetch extracted line
        """

        if args.memtype == "gb":
            memgb = value.split()
            used = float(memgb[1].replace("MiB", ""))
            total = float(memgb[3].replace("MiB", ""))

            line.append(' '.join(
                [str(round(used / 1024, 2)), "GiB /", str(round(total / 1024, 2)), "GiB"]))
        else:
            line.append(value[value.find(key)+len(key)+1:])

    def get(self, os: str, line: List, value: str, key: str, valueOffset: int = 1):
        """
        Get the info from the given neofetch line

        Parameters
        ----------
        os: str
            Detected OS ("windows", "linux" or "macos")
        line: List
            List who will contains the values
        value : str
            Neofetch extracted line
        key : str
            Key for the dict
        valueOffset: int
            Offset for extracting the value without the key (default : 1)
        """

        line.append(value[value.find(key)+len(key)+valueOffset:])

    def get_component(self, key: str):
        """
        Get component info from map

        Args:
            key (str): component key in map
        """
        try:
            return self.componentMap[key]
        except KeyError as err:
            print("[KeyError]: ", end="")
            print(err)

            return []

    def get_component_line(self, key: str) -> str:
        try:
            values = self.componentMap[key]
            return '\n'.join(values) if len(values) > 0 else '{} N/A'.format(key)
        except KeyError as err:
            print("[KeyError]: ", end="")
            print(err)

            return "{} N/A".format(key)

    def get_component_id(self, key: str) -> str:
        component = self.get_component_line(key).lower()
        component_list = self.idsMap[self.idsMap["map"][key]]

        for comp, id in component_list.items():
            if component.find(comp.lower()) >= 0:
                return id

        print("Unknown {}, contact us on github to resolve this.".format(
            self.idsMap["map"][key]))

        return component_list["unknown"]

    def get_component_idkey(self, key: str) -> str:
        component = self.get_component_line(key).lower()
        component_list = self.idsMap[self.idsMap["map"][key]]

        for comp, _ in component_list.items():
            if component.find(comp.lower()) >= 0:
                return comp

        print("Unknown {}, contact us on github to resolve this.".format(
            self.idsMap["map"][key]))

        return component_list["unknown"]
