import mlnx_dirs
import subprocess
import os
import shutil
import argparse
from dell_drop_template import DELL_CODE_DROP_MAP
from dell_drop_template import DELL_PIE_TEMPLATES
from dell_drop_template import DELL_FW_INFO
import zipfile
import tarfile
import xml.etree.ElementTree as ET
import sys
import json

cwd = os.getcwd()
dup_build_version = "OM23_12_02"
pie_version = '65'
file_name_max = 99
base_dir = os.path.join(cwd, 'temp_drop1')
template_folder = os.path.join(cwd, 'pie_templates')


parser = argparse.ArgumentParser(description='Create code drop for Dell')
parser.add_argument('--config', dest='config_file', action='store',
                    default=None,
                    help='provide a .json config file')
parser.add_argument('--without-pldm', dest='with_pldm', action='store_false', help='build DUPs with PLDM support', default=True)
parser.add_argument('--channel', dest='channel_bool', action='store_true', help='build channel DUPs', default=False)

with_pldm = parser.parse_args().with_pldm
channel_bool = parser.parse_args().channel_bool
if with_pldm:
    dup_template_folder = os.path.join(template_folder, 'FW-Template')
else:
    dup_template_folder = os.path.join(template_folder, 'dup_pie')


def check_vpn():
    hostname = "10.9.12.121"
    par = '-n' if os.name == 'nt' else '-c'

    command = ['ping', par, '1', hostname]

    if subprocess.call(command, stdout=subprocess.PIPE, shell=False) != 0:
        print("Error: cannot reach mtl.com.\nMake sure VPN is connected.")
        exit(0)
    return


def create_directory(location, level):
    if os.path.isdir(location):
        shutil.rmtree(location)
    os.mkdir(location)
    for key in level:
        new_location = os.path.join(location, key)
        os.mkdir(new_location)
        try:
            create_directory(new_location, level[key])
        except:
            continue


def print_drop(level):
    for key in level:
        print(key)
        try:
            print_drop(level[key])
        except:
            continue


def pop_linux_ofed(ofed_isos, ofed_factory, ofed_reduced, ofed_source):
    shutil.copy(ofed_factory, os.path.join(base_dir, 'Linux', 'Factory'))
    shutil.copy(ofed_reduced, os.path.join(base_dir, 'Linux', 'Customer'))
    shutil.copy(ofed_source, os.path.join(base_dir, 'Linux', 'Source'))
    for iso in ofed_isos:
        shutil.copy(iso, os.path.join(base_dir, 'Linux', 'ISO'))


def pop_lts_linux_ofed(ofed_lts_factory, ofed_lts_reduced):
    shutil.copy(ofed_lts_factory, os.path.join(base_dir, 'Linux', 'Factory', 'LTS'))
    shutil.copy(ofed_lts_reduced, os.path.join(base_dir, 'Linux', 'Customer', 'LTS'))


def pop_winof(winof_pnp, winof_mup):
    shutil.copy(winof_pnp, os.path.join(base_dir, 'Windows - CX3', 'PNP', 'x64'))
    shutil.copy(winof_mup, os.path.join(base_dir, 'Windows - CX3', 'MUP', 'x64'))


def pop_vpi(vpi):
    vpi_dir = os.path.join(base_dir, 'VPI Firmware')
    for key in vpi:
        if not vpi[key]:
            continue
        for folder in os.listdir(vpi_dir):
            if folder[-1] == key[-1]:
                for fw in vpi[key]:
                    shutil.copy(fw, os.path.join(vpi_dir, folder))
    shutil.make_archive(os.path.join(base_dir, 'VPI Firmware'), 'zip', vpi_dir)
    shutil.rmtree(vpi_dir)


def convert_mup_to_pie(mup):
    # pie_template = DELL_PIE_TEMPLATES['winof2_pie']
    temp_dir = os.path.join(cwd, 'temp')
    temp_mup = os.path.join(temp_dir, 'mup')
    temp_pie = os.path.join(temp_dir, 'pie')
    if os.path.isdir(temp_dir):
        shutil.rmtree(temp_dir)
    os.mkdir(temp_dir)

    unzip_file_to(mup, temp_mup)
    of_version = mup.split('MUP_')[1]
    of_version = of_version.split('_x64')[0]
    of_version = of_version.replace('_', '.')
    of_rev = ''
    for file in os.listdir(temp_mup):
        if 'MLNX_WinOF2' in file:
            of_rev = file.split('_')[3]

    # Populate payload
    winof2_pie = os.path.join(template_folder, 'winof2_pie')
    shutil.copytree(winof2_pie, os.path.join(base_dir, temp_pie))
    for file in os.listdir(temp_mup):
        if 'mup.xml' not in file:
            try:
                shutil.copy(os.path.join(temp_mup, file), os.path.join(temp_pie, 'common', 'payload'))
            except PermissionError:
                shutil.copytree(os.path.join(temp_mup, file), os.path.join(temp_pie, 'common', 'payload', file))
    # Update Ini
    ini_file = None
    ini_info = []
    for file in os.listdir(os.path.join(temp_pie, 'win64')):
        if 'DrvCfg64.ini' in file:
            ini_file = os.path.join(temp_pie, 'win64', file)
            f = open(ini_file, "r")
            for x in f:
                ini_info.append(x)
            f.close()
    if not ini_file:
        raise RuntimeError("ini file is empty")
    new_ini = ''
    for line in ini_info:
        line = line.replace('Ver=\"*\"', 'Ver=\"' + of_version + '\"')
        line = line.replace('Rev=\"*\"', 'Rev=\"' + of_rev + '\"')
        new_ini += line
    with open(ini_file, 'w') as file:
        file.write(new_ini)

    pie_name = 'MLNX_WINOF-' + of_version.replace('.', '_') + '_' + of_rev
    shutil.make_archive(os.path.join(base_dir, 'Windows - CX4+', pie_name), 'zip', temp_pie)
    os.rename(os.path.join(base_dir, 'Windows - CX4+', pie_name + '.zip'),
              os.path.join(base_dir, 'Windows - CX4+', pie_name + '.pie'))
    shutil.rmtree(temp_dir, ignore_errors=True)


def extract_and_pop_pie(mup):
    temp_dir = os.path.join(cwd, 'temp')
    temp_extract = os.path.join(temp_dir, 'extra')
    temp_pie = os.path.join(temp_dir, 'pie')
    if os.path.isdir(temp_dir):
        shutil.rmtree(temp_dir)
    os.mkdir(temp_dir)

    unzip_file_to(mup, temp_extract)
    of_version = mup.split('PIE_')[1]
    of_version = of_version.split('_x64')[0]
    of_version = of_version.replace('_', '.')
    of_rev = ''
    for file in os.listdir(temp_extract):
        if 'MLNX_WinOF2' in file:
            of_rev = file.split('_')[3]

    # Populate payload
    winof2_pie = os.path.join(template_folder, 'winof2_pie')
    shutil.copytree(winof2_pie, os.path.join(base_dir, temp_pie))
    for file in os.listdir(temp_extract):
        if file == 'DrvCfg64.ini':
            continue
        try:
            shutil.copy(os.path.join(temp_extract, file), os.path.join(temp_pie, 'common', 'payload'))
        except PermissionError:
            shutil.copytree(os.path.join(temp_extract, file), os.path.join(temp_pie, 'common', 'payload', file))
    # Update Ini
    ini_file = None
    ini_info = []
    for file in os.listdir(os.path.join(temp_pie, 'win64')):
        if 'DrvCfg64.ini' in file:
            ini_file = os.path.join(temp_pie, 'win64', file)
            f = open(ini_file, "r")
            for x in f:
                ini_info.append(x)
            f.close()
    if not ini_file:
        raise RuntimeError("ini file is empty")
    new_ini = ''
    for line in ini_info:
        line = line.replace('Ver=\"*\"', 'Ver=\"' + of_version + '\"')
        line = line.replace('Rev=\"*\"', 'Rev=\"' + of_rev + '\"')
        new_ini += line
    with open(ini_file, 'w') as file:
        file.write(new_ini)

    pie_name = 'MLNX_WINOF-' + of_version.replace('.', '_') + '_' + of_rev
    shutil.make_archive(os.path.join(base_dir, 'Windows - CX4+', pie_name), 'zip', temp_pie)
    os.rename(os.path.join(base_dir, 'Windows - CX4+', pie_name + '.zip'),
              os.path.join(base_dir, 'Windows - CX4+', pie_name + '.pie'))
    shutil.rmtree(temp_dir, ignore_errors=True)


def pop_winof2(pnp, mup, symb):
    shutil.copy(pnp, os.path.join(base_dir, 'Windows - CX4+', 'PNP', 'x64'))
    shutil.copy(symb, os.path.join(base_dir, 'Not_For_End_User_Tools - CX4+', 'Windows_symbols'))
    # Creating Pie
    print('Converting WinOF2 mup to pie')
    extract_and_pop_pie(mup)


def create_fw_pie(fw_list, pie_template, fw_version, with_pldm, pldm_list):

    """
        Populate psid_lookup.lst
    """
    psid_file = os.path.join(pie_template, 'common', 'psid_lookup.lst')
    file = open(psid_file, 'w+', newline='')
    for i in range(0, len(fw_list['guid'])):
        file.write(f"{fw_list['psid'][i]},15b3:{fw_list['devid'][i]}:15b3:{fw_list['subdev'][i]},{fw_list['pn'][i]},{fw_list['adpt'][i]}\n")
    """
        Updates configfile.xml with new name, versionname, bin file names
    """
    print("Updating the configfile.xml files...")
    config_file = os.path.join(pie_template, 'common', 'payload', 'configfile.xml')
    numeric_version = fw_version.replace('_', '')
    adap_dot_version = fw_version.replace('_', '.')
    adap_dot_version = adap_dot_version[:-2] + '.' + adap_dot_version[-2:]
    if adap_dot_version[:2] == '2.':
        adap_dot_version = '02.' + adap_dot_version[2:]

    tree = ET.parse(config_file)  # Parsing the config file
    root = tree.getroot()
    for elem in root.iter('package'):
        elem.set('versionname', adap_dot_version)
        elem.set('name', numeric_version)

    for i in range(0, len(fw_list['binary'])):
        pciid = ET.SubElement(root, "pciid", vendorid="15b3", deviceid=fw_list['devid'], devicename=fw_list['adpt'][i])
        supportedsystems = ET.SubElement(pciid, "supportedsystems")
        subvendor = ET.SubElement(supportedsystems, "subvendor", id="15b3")
        ET.SubElement(subvendor, "subdevice", id=fw_list['subdev'][i])

        # Create the FMPinfo element
        fmpinfo = ET.SubElement(pciid, "FMPinfo", vendorcode="FORCE_UPDATE", vendorcodetype="CHAR8")

        # Create the FmpSkipimage element and its subelements
        fmp_skipimage = ET.SubElement(pciid, "FmpSkipimage", type="")
        ET.SubElement(fmp_skipimage, "FmpSkipimagetypeid").text = "00000000-0000-0000-0000000000000000"
        ET.SubElement(fmp_skipimage, "FmpSkipversion").text = "0"
        ET.SubElement(fmp_skipimage, "FmpSkipversionname")
        ET.SubElement(fmp_skipimage, "FmpSkipfilename")

        # Create the image element and its subelements
        image = ET.SubElement(pciid, "image", type="firmware")
        ET.SubElement(image, "imagetypeid").text = fw_list['guid'][i]
        ET.SubElement(image, "version").text = numeric_version
        ET.SubElement(image, "versionname").text = adap_dot_version

        name = ''
        pn_index = -1
        for j in fw_list['binary'][i].split('-'):
            if 'UEFI' in j or 'NVME' in j:
                name = fw_list['binary'][i].split('-')[pn_index]
                break
            pn_index += 1
        # Need to short binary name if longer than 90 character (DPU yellow screen issue)
        fw = fw_list['binary'][i].split('\\')[-1]
        if len(fw) > file_name_max:
            tmp = fw.split('-')
            if 'signed' in tmp[-1]:
                fw = '-'.join(tmp[:6]) + '.signed.bin'
            else:
                fw = '-'.join(tmp[:6]) + '.bin'
        if name in elem.text:
            ET.SubElement(image, "filename").text = fw
            break


    """ verifies config.xml contents"""
    for elem in root.iter('filename'):
        if fw_version not in elem.text:
            quit(f"fw miss match {elem.text} should be {fw_version}")
    ET.indent(root, space="\t", level=0)
    tree.write(config_file)  # Writing all changes to config file
    tree.write(config_file, encoding="utf-8",
               xml_declaration=True)  # Writing XML header as existing header is being deleted while writing above

    """
        Updates UpdRollBack.lst with 'configfile.xml', bin files and Empty line at the end
    """
    print("Updating the UpdRollBack.lst files...")

    uproll_file_path = os.path.join(pie_template, 'common', 'UpdRollBack.lst')
    file = open(uproll_file_path, 'w+')

    file.write('configfile.xml')
    file.write('\n')
    if with_pldm:
        for pldm in pldm_list:
            file.write(pldm.split("\\")[-1])
            file.write('\n')
    for fw in fw_list['binary']:
        fw = fw.split('\\')[-1]
        if len(fw) > file_name_max:
            tmp = fw.split('-')
            if 'signed' in tmp[-1]:
                fw = '-'.join(tmp[:6]) + '.signed.bin'
            else:
                fw = '-'.join(tmp[:6]) + '.bin'
        file.write(fw)
        file.write('\n')
    file.close()

    """
        Updates pieconfig with new name, versionname, bin file names
    """
    operating_sys = ['lx', 'win64']
    for op in operating_sys:
        print("updating PIEConfig.xml from " + op)
        pie_conf_path = os.path.join(pie_template, op, 'PIEConfig.xml')
        tree = ET.parse(pie_conf_path)  # Parsing the config file
        root = tree.getroot()
        numeric_version = fw_version.replace('_', '')
        adap_dot_version = fw_version.replace('_', '.')
        adap_dot_version = adap_dot_version[:-2] + '.' + adap_dot_version[-2:]
        if adap_dot_version[:2] == '2.':
            adap_dot_version = '02.' + adap_dot_version[2:]
        for rapper in root.iter('RollbackInformation'):
            rapper_attrib = rapper.attrib
            rapper_attrib['rollbackIdentifier'] = fw_list['rollback']
            rapper_attrib['fmpWrapperIdentifier'] = fw_list['fwwrap']
        for rapper in root.iter('FMPWrappers'):
            rapper_attrib = rapper.attrib
            rapper_attrib['identifier'] = fw_list['fwwrap']
            rapper_attrib['fmpWrapperIdentifier'] = fw_list['fwwrap']
            rapper_attrib['rollbackIdentifier'] = fw_list['rollback']
        for rapper in root.iter('FMPWrapperInformation'):
            rapper_attrib = rapper.attrib
            rapper_attrib['identifier'] = fw_list['fwwrap']
        if with_pldm:
            for payload in root.iter('Payload'):
                payload_atrb = payload.attrib
                payload_atrb['version'] = adap_dot_version
                payload_atrb['fmpWrapperIdentifier'] = fw_list['fwwrap']

            target = root.find("Payload")
            node = ET.SubElement(target, "PayloadImages")
            for i in range(0, len(fw_list['binary'])):
                xml_payloadimage = ET.SubElement(node, 'PayloadImage', id=fw_list['guid'][i], filename=fw_list['psid'][i]+'.pldm',
                                                 version=adap_dot_version, skip="false")
                xml_pci_info = ET.SubElement(xml_payloadimage, "PCIInfo", deviceID=fw_list['devid'][i], subDeviceID=fw_list['subdev'][i],
                                             subVendorID="15b3", vendorID="15b3")
                xml_protocol_info = ET.SubElement(xml_payloadimage, "ProtocolInformation", protocolType="PLDM")
            for elem in root.iter('Payload'):
                elem.set('version', adap_dot_version)
            for elem in root.iter('PayloadImage'):
                elem.set('version', adap_dot_version)
                for fw in fw_list['binary']:
                    name = ''
                    pn_index = -1
                    for i in fw.split('-'):
                        if 'UEFI' in i or 'NVME' in i:
                            name = fw.split('-')[pn_index]
                            break
                        pn_index += 1
                    # Need to short binary name if longer than 90 character (DPU yellow screen issue)
                    fw = fw.split('\\')[-1]
                    if len(fw) > file_name_max:
                        tmp = fw.split('-')
                        if 'signed' in tmp[-1]:
                            fw = '-'.join(tmp[:6]) + '.signed.bin'
                        else:
                            fw = '-'.join(tmp[:6]) + '.bin'
                    if name in elem.get('filename'):
                        print("replacing with " + fw)
                        elem.set('filename', fw)
                        break
        ET.indent(root, space="\t", level=0)
        tree.write(pie_conf_path)  # Writing all changes to pieconfig file
        tree.write(pie_conf_path, encoding="utf-8", xml_declaration=True)  # Writing XML header as existing header is being deleted while writing above
        """ verifies pieconfig.xml contents"""
        for elem in root.iter('filename'):
            if fw_version not in elem.text:
                quit(f"fw miss match {elem.text} should be {fw_version}")

    """ verifies DUPBuild.confg has correct version"""
    print("Verifying DUPBuild.config")
    dup_build_path = os.path.join(pie_template, 'DUPBuild', 'DUPBuild.config')
    file = open(dup_build_path, 'r')
    file_lines = file.readlines()
    dup_build_in_pie = file_lines[1].strip()
    if dup_build_in_pie.split('=')[1] != dup_build_version:
        raise RuntimeError(dup_build_in_pie.split('=')[1], " Error: version does not match with ", dup_build_version)

    """ verifies PIEConfig.xml contents"""
    operating_sys =['lx', 'win64']
    for op in operating_sys:
        print("Verifying PIEConfig.xml from " + op)
        pie_conf_path = os.path.join(pie_template, op, 'PIEConfig.xml')
        tree = ET.parse(pie_conf_path)  # Parsing the config file
        root = tree.getroot()

        for info in root.iter('Info'):
            info_attributes = info.attrib
        for roll_back_info in root.iter('RollbackInformation'):
            roll_back_attributes = roll_back_info.attrib
        for FMP_wrapper_info in root.iter('FMPWrapperInformation'):
            FMP_wrapper_attributes = FMP_wrapper_info.attrib

        if info_attributes['identifier'] != '769CCC6E-09A0-4CEF-8774-279E4D3748F3':
            raise RuntimeError(" Error: Identifier in Info is incorrect in PIEConfig.xml of " + op + " \n", info_attributes[
                'identifier'])

        if info_attributes['folderName'] != 'Mellanox-Adapter-Firmware':
            raise RuntimeError(" Error: folderName in Info is incorrect in PIEConfig.xml of " + op + " \n", info_attributes[
                'folderName'])

        if roll_back_attributes['fmpWrapperIdentifier'] != FMP_wrapper_attributes['identifier']:
            raise RuntimeError(
                " Error: fmpWrapperIdentifier from RollbackInformation does not match with identifier from FMPWrapperInformation of " + op + " \n", \
                roll_back_attributes['fmpWrapperIdentifier'])

        fw_major = fw_version.split('_')[0]
        if roll_back_attributes['rollbackIdentifier'] != DELL_FW_INFO[DELL_FW_INFO[fw_major]]['rollbackID']:
            raise RuntimeError(
                " Error: rollbackIdentifier for " + fw_version + " is incorrect in PIEConfig.xml  of " + op + " \n", \
                roll_back_attributes['rollbackIdentifier'])

        if 'alternateRollbackIdentifier' in roll_back_attributes.keys() and roll_back_attributes['alternateRollbackIdentifier'] != DELL_FW_INFO[DELL_FW_INFO[fw_major]]['altrollbackID']:
            raise RuntimeError(
                " Error: alternateRollbackIdentifier for " + fw_version + " is incorrect in PIEConfig.xml  of " + op + " \n", \
                roll_back_attributes['alternateRollbackIdentifier'])


def pop_managed_fw(fw, pldm_fw, with_pldm):
    cx_name_map = {'ConnectX-3': 'CX3', 'ConnectX-4': 'CX4', 'ConnectX-4LX': 'CX4LX', 'ConnectX-5': 'CX5EX',
                   'ConnectX-6': 'CX6', 'ConnectX-6Dx': 'CX6DX', 'ConnectX-6LX': 'CX6LX', 'BlueField-2': 'BF2',
                   'ConnectX-7': 'CX7', 'ConnectX-8': 'CX8'}

    for key in fw:
        cx_abrev = cx_name_map[key]
        fw_versions = fw[key]['binary'][0].split('rel-')[1]
        fw_versions = fw_versions.split('-')[0]
        cx_folder = os.path.join(base_dir, 'FW_DUP - ' + cx_abrev)
        # copy binaries
        for item in fw[key]['binary']:
            bin_dest = os.path.join(cx_folder, 'binaries')
            shutil.copy(item, bin_dest)
        pie_name = 'Mellanox' + key.replace('-', '') + 'FrmwPiePlugin-' + fw_versions.replace('_', '.') + '-' + pie_version
        pie_folder = os.path.join(cx_folder, pie_name)
        os.mkdir(pie_folder)
        if with_pldm:
            for item in pldm_fw[key]:
                bin_dest = os.path.join(cx_folder, 'binaries')
                shutil.copy(item, bin_dest)
        for file in os.listdir(os.path.join(dup_template_folder)):
            try:
                shutil.copy(os.path.join(dup_template_folder, file), pie_folder)
            except PermissionError:
                shutil.copytree(os.path.join(dup_template_folder, file), os.path.join(pie_folder, file))
        # Need to short binary name if longer than 90 character (DPU yellow screen issue)
        if len(fw[key]['binary']) > file_name_max:
            tmp = fw[key]['binary'].split('-')
            if 'signed' in tmp[-1]:
                fw[key]['binary'] = '-'.join(tmp[:5]) + '.signed.bin'
            else:
                fw[key]['binary'] = '-'.join(tmp[:5]) + '.bin'
        create_fw_pie(fw[key], pie_folder, fw_versions, with_pldm, pldm_fw[key])
        ###########
        bin_dir = os.path.join(cx_folder, 'binaries')
        for file in os.listdir(bin_dir):
            # Need to short binary name if longer than 90 character (DPU yellow screen issue)
            original_file = file
            if len(file) > file_name_max:
                tmp = file.split('-')
                if 'signed' in file:
                    file = '-'.join(tmp[:6]) + '.signed.bin'
                else:
                    file = '-'.join(tmp[:6]) + '.bin'
            shutil.copy(os.path.join(bin_dir, original_file), os.path.join(pie_folder, 'common', 'payload', file))
        shutil.make_archive(pie_folder, 'zip', pie_folder)
        os.rename(pie_folder + '.zip', pie_folder + '.pie')
        shutil.rmtree(pie_folder)


def mst_fix(mst):
    # Fix is used to call mst script from within DUP. Needed for Secure Boot DUP operation.
    mst_file = open(mst, "r")
    mst_lines = mst_file.readlines()
    new_mst = ''
    for line in mst_lines:
        if '#@POST_MST_BIN_DIR@' in line:
            line = 'mbindir=.'
        new_mst += line
    mst_file.close()
    mst_file = open(mst, 'w', newline='\n')
    mst_file.write(new_mst)


def update_mft(lx32, lx64, win64, winpe):
    # We keep mft uniform through all dups no need to check which firmware is being updated
    temp_mft = os.path.join(template_folder, 'temp_mft')
    os.mkdir(temp_mft)

    win_temp = os.path.join(temp_mft, 'win64')
    lx32_temp = os.path.join(temp_mft, 'l32')
    lx64_temp = os.path.join(temp_mft, 'l64')
    os.mkdir(win_temp)
    os.mkdir(lx64_temp)
    os.mkdir(lx32_temp)

    tar = tarfile.open(lx32, "r:gz")
    tar.extractall(lx32_temp)
    tar.close()
    tar = tarfile.open(lx64, "r:gz")
    tar.extractall(lx64_temp)
    tar.close()
    zip = zipfile.ZipFile(win64)
    zip.extractall(win_temp)
    zip.close()

    mst_fix(os.path.join(lx32_temp, 'mst'))
    mst_fix(os.path.join(lx64_temp, 'mst'))

    for folder in os.listdir(dup_template_folder):
        l32 = os.path.join(os.path.join(dup_template_folder, folder, 'lx', 'l32'))
        l64 = os.path.join(os.path.join(dup_template_folder, folder, 'lx', 'l64'))
        win = os.path.join(os.path.join(dup_template_folder, folder, 'win64'))

        for file in os.listdir(lx32_temp):
            if file != 'device_info':
                shutil.copy(os.path.join(lx32_temp, file), l32)
            else:
                shutil.rmtree(os.path.join(l32, 'device_info'))
                shutil.copytree(os.path.join(lx32_temp, file), os.path.join(l32, 'device_info'))
        for file in os.listdir(lx64_temp):
            if file != 'device_info':
                shutil.copy(os.path.join(lx64_temp, file), l64)
            else:
                shutil.rmtree(os.path.join(l64, 'device_info'))
                shutil.copytree(os.path.join(lx64_temp, file), os.path.join(l64, 'device_info'))
        for file in os.listdir(win_temp):
            if file != 'device_info':
                shutil.copy(os.path.join(win_temp, file), win)
            else:
                shutil.rmtree(os.path.join(win, 'device_info'))
                shutil.copytree(os.path.join(win_temp, file), os.path.join(win, 'device_info'))

    for folder in os.listdir(os.path.join(template_folder, 'inv_pie')):
        l32 = os.path.join(os.path.join(template_folder, 'inv_pie', folder, 'lx', 'l32'))
        l64 = os.path.join(os.path.join(template_folder, 'inv_pie', folder, 'lx', 'l64'))
        win = os.path.join(os.path.join(template_folder, 'inv_pie', folder, 'win64'))
        for file in os.listdir(lx32_temp):
            if file != 'device_info':
                shutil.copy(os.path.join(lx32_temp, file), l32)
            else:
                shutil.rmtree(os.path.join(l32, 'device_info'))
                shutil.copytree(os.path.join(lx32_temp, file), os.path.join(l32, 'device_info'))
        for file in os.listdir(lx64_temp):
            if file != 'device_info':
                shutil.copy(os.path.join(lx64_temp, file), l64)
            else:
                shutil.rmtree(os.path.join(l64, 'device_info'))
                shutil.copytree(os.path.join(lx64_temp, file), os.path.join(l64, 'device_info'))
        for file in os.listdir(win_temp):
            if file != 'device_info':
                shutil.copy(os.path.join(win_temp, file), win)
            else:
                shutil.rmtree(os.path.join(win, 'device_info'))
                shutil.copytree(os.path.join(win_temp, file), os.path.join(win, 'device_info'))
        shutil.make_archive(os.path.join(base_dir, 'Inv_Coll', 'Firmware', folder + '-' + pie_version), 'tar', os.path.join(template_folder,
                                                                                                      'inv_pie', folder))
    shutil.rmtree(temp_mft)

    # Update WinPE mft
    shutil.copy(winpe, os.path.join(base_dir, 'Not_For_End_User_Tools - CX3', 'MDIAG', 'MFT_WinPE'))
    shutil.copy(winpe, os.path.join(base_dir, 'Not_For_End_User_Tools - CX4+', 'MDIAG', 'MFT_WinPE'))


def copy_bfb(dev, prod):
    temp_dev = os.path.join(base_dir, 'ARM_DUP', 'DEV')
    temp_prod = os.path.join(base_dir, 'ARM_DUP', 'PROD')

    shutil.copy(dev, temp_dev)
    shutil.copy(prod, temp_prod)

def create_arm_pie(dev, prod):
    arm_template = os.path.join(dup_template_folder, 'ARM-BF2')
    temp_dev = os.path.join(base_dir, 'ARM_DUP', 'DEV')
    temp_prod = os.path.join(base_dir, 'ARM_DUP', 'PROD')

    for file in os.listdir(os.path.join(arm_template)):
        try:
            shutil.copy(os.path.join(arm_template, file), temp_dev)
            shutil.copy(os.path.join(arm_template, file), temp_prod)
        except PermissionError:
            shutil.copytree(os.path.join(arm_template, file), os.path.join(temp_dev, file))
            shutil.copytree(os.path.join(arm_template, file), os.path.join(temp_prod, file))

    shutil.copy(dev, os.path.join(temp_dev, 'common', 'payload'))
    shutil.copy(prod, os.path.join(temp_prod, 'common', 'payload'))

    shutil.make_archive(temp_dev, 'zip', temp_dev)
    os.rename(temp_dev + '.zip', temp_dev + '.pie')

    shutil.make_archive(temp_prod, 'zip', temp_prod)
    os.rename(temp_prod + '.zip', temp_prod + '.pie')


def unzip_file_to(src, dest):
    with zipfile.ZipFile(src, 'r') as zip_ref:
        zip_ref.extractall(dest)


def main():
    fw_list = []  # ['2_42_5058', '12_28_4512', '14_28_4512', '16_28_4512', '20_28_4512', '22_28_4512']
    linux_driver = '5.4-1.0.3.0'
    lts_linux_driver = ''  # ''4.9-3.1.5.0'
    windows_driver1 = ''  # '5.50'
    windows_driver2 = ''  # '2.70'
    mft_version = ''  # '4.16.0-105'

    if with_pldm:
        print("Building NIC DUPs with PLDM support")
    else:
        print("Building NIC DUPs without PLDM support")

    args = parser.parse_args()
    if args.config_file is not None:
        config_file = args.config_file
        try:
            with open(config_file) as f:
                data = json.load(f)
        except:
            quit(config_file + " is not a valid json file")
        fw_list = data["fw_list"]
        linux_driver = data["linux_driver"]
        lts_linux_driver = data["lts_linux_driver"]
        windows_driver1 = data["windows_driver1"]
        windows_driver2 = data["windows_driver2"]
        mft_version = data["mft_version"]
        arm_dpu = data["arm_dpu"]

    check_vpn()
    create_directory(base_dir, DELL_CODE_DROP_MAP)

    mlnx = mlnx_dirs.DellMlnxDirs(fw_list=fw_list,
                                  linux_driver=linux_driver,
                                  linux_driver_dell_only=lts_linux_driver,
                                  windows_driver1=windows_driver1,
                                  windows_driver2=windows_driver2,
                                  mft_version=mft_version,
                                  with_pldm=with_pldm,
                                  arm_dpu=arm_dpu,
                                  channel_bool=channel_bool)
    if linux_driver != '':
        print("populating Linux OFED")
        pop_linux_ofed(mlnx.ofed_isos, mlnx.ofed_factory, mlnx.ofed_reduced, mlnx.ofed_source)
    if lts_linux_driver != '':
        print("populating LTS OFED")
        pop_lts_linux_ofed(mlnx.ofed_lts_factory, mlnx.ofed_lts_reduced)
    if windows_driver1 != '':
        print("populating WinOF")
        pop_winof(mlnx.winof_pnp, mlnx.winof_mup)
    if fw_list:
        print("creating pie files")
        pop_managed_fw(mlnx.fw_managed, mlnx.pldm_managed, with_pldm)
        print("populating VPI")
        pop_vpi(mlnx.fw_vpi)
    if windows_driver2 != '':
        print("populating WinOF2")
        pop_winof2(mlnx.winof2_pnp, mlnx.winof2_mup, mlnx.winof2_symbol)
    # Everytime mft is updated need to respin dups
    if mft_version != '':
        print("updating mft and creating inv_collect")
        update_mft(mlnx.mft_linux32, mlnx.mft_linux64, mlnx.mft_windows, mlnx.mft_winpe)
    if arm_dpu != '':
        print("creating arm dup")
        create_arm_pie(mlnx.arm_path_dev, mlnx.arm_path_prod)
        copy_bfb(mlnx.arm_path_dev_bfb, mlnx.arm_path_prod_bfb)


if __name__ == "__main__":
    main()
