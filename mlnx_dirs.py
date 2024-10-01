import os
win = 'windows'
lin = 'linux'

DELL_LINUX_LIST = [
        "rhel8.8",
        "rhel8.9",
        "rhel8.10",
        "rhel9.2",
        "rhel9.3",
        "rhel9.4",
        "sles15sp4",
        "sles15sp5",
        "sles15sp6"
    ]

DELL_FW_LIST = {'25408': {'managed': ['06256K-CLP-8005', '08KP6W_0M9NW6', '0W0RM9_0Y3KKR', '019RNV_0YHTD6',
                                      '02T0WW-CLP', '0C8Y42_0R3F0N'],
                         'vpi': ['079DJ3', '08PTD1', '01T7NW', '0Y5WKX', '0XK4C4', '0P90JM', '0K6V3V_Bx', '0J05YT_Bx', '0CDMG5', '0T483W-']},
                '4115': {'managed': ['00272F_0HWTYK_Ax'],
                         'vpi': ['0NHYP5_0XR0K2_Ax', '06W1HY_0JJN39_Ax', '0068F2_0NNJ2M_Ax', 'DELL_C6320p_1P_EDR_Ax']},
                '4117': {'managed': ['0R887V', '020NJD_0MRT0D_Ax', '0WCHFY_Ax'],
                         'vpi': []},
                '4119': {'managed': ['09FTMY_071C1T', '0V5DG9_0TDNNT', '04TRD3'],
                         'vpi': ['0VC496_06FKDT'],
                         'managed_psid': ['DEL0000000004', 'DEL0000000015', 'DEL0000000016']},
                '4123': {'managed': ['0CY7GD_01GK7G', '0Y1T43_07TKND'],
                         'vpi': [],
                         'managed_psid': ['DEL0000000010', 'DEL0000000013'],
                         'devid': '101b',
                         'subdevid': ['0022', '0018'],
                         'GUID': ['a04f6157-7e90-4086-83ac-f6c86449eb11',
                                  'd2328413-def6-4105-be31-76f20f929137'],
                         'adpt': ['Mellanox ConnectX-6 Single Port HDR QSFP56 PCIE Adapter',
                                  'Mellanox ConnectX-6 Single Port HDR100 QSFP56 PCIE Adapter'],
                         'fmpwrapper': 'e6b4220d-53b7-418e-80d7-4b1ac1e252f7',
                         'rollback': 'c3a48eee-563a-4ae5-b346-fbc3e212d06b'},
                '4125': {'managed': ['0F6FXM_08P2T2', '0FD63G'],
                         'vpi': [],
                         'managed_psid': ['DEL0000000027', 'DEL0000000046'],
                         'devid': '101d',
                         'subdevid': ['0058', '0119'],
                         'GUID': ['268F13F7-1F2A-4B56-4A85-1F2DD16ED8B7',
                                  'E813A278-67E5-D898-4706-AF63ABD33230'],
                         'adpt': ['Mellanox ConnectX-6 Dx Dual Port 100 GbE QSFP56 Adapter',
                                  'Nvidia ConnectX-6 Dx 2x 100G QSFP56 OCP3.0 SFF'],
                         'fmpwrapper': '57faf611-e42f-41b1-8dbd-78c95e29bdd9',
                         'rollback': 'e50ab4da-9cbf-4350-8feb-5dd89310baa6'},
                '4127': {'managed': ['06XJXK_0R5WK9', '0DN78C'],
                         'vpi': [],
                         'managed_psid': ['DEL0000000030', 'DEL0000000031'],
                         'devid': '101f',
                         'subdevid': ['0019', '0020'],
                         'GUID': ['61249EF5-6B36-EB2C-3DD5-816898AE3397',
                                  'CDDF88D5-BCCC-1950-DB97-8831C6634C79'],
                         'adpt': ['ConnectX-6 Lx 2x 25G SFP28 OCP3.0 SFF',
                                  'ConnectX-6 Lx 2x 25G SFP28'],
                         'fmpwrapper': 'af894d5b-b5f1-45db-a72f-9c41afe11ebd',
                         'rollback': '74de307d-9dd2-413c-8ae0-2cf947d6a6d4'},
                '4129': {'managed': ['0K84XJ_0M8XMC_Ax', '0RYMTY_0GJDG3_Ax', '0R7T63_0Y773V', '0TRMPK_049J96'],
                         'vpi': [],
                         'managed_psid': ['DEL0000000035', 'DEL0000000036', 'DEL0000000050', 'DEL0000000051'],
                         'devid': '1021',
                         'subdevid': ['0040', '0041', '0121', '0120'],
                         'GUID': ['EA680D40-8A1C-959F-D223-510A9219E8C1',
                                  'C03F30A3-07E0-D907-8AC0-BE22B78FA7B1',
                                  '7EA97C05-F759-9DF5-3ECD-59F425381963',
                                  'C7C3B03C-8602-7104-76F7-988651179A67'],
                         'adpt': ['NVIDIA ConnectX-7 Single Port NDR200 OSFP Adapter',
                                  'NVIDIA ConnectX-7 Single Port NDR OSFP Adapter',
                                  'NVidia ConnectX-7 Single Port NDR (w/VPI) OSFP Adapter',
                                  'NVidia ConnectX-7 Single Port NDR200 (w/VPI)OSFP Adapter'],
                         'fmpwrapper': '43ccb3ba-95b6-4f65-9200-13b71b6ad023',
                         'rollback': 'A1027480-A2BC-4A3D-8604-605139F1A796'
                         },
                '41686': {'managed': ['0JNDCM_Dx', '0PXDVR_Ax'],
                          'vpi': [],
                          'managed_psid': ['DEL0000000033', 'DEL0000000034']}
                }

CHANNEL_FW_LIST = {
                '4125': {'managed': ['MCX623106AS-CDA_Ax', 'MCX623436MS-CDA_Ax'],
                         'vpi': [],
                         'managed_psid': ['MT_0000000437', 'MT_0000000773'],
                         'devid': '101d',
                         'subdevid': ['0042', '0113'],
                         'GUID': ['2391047A-4CCC-2961-4EB6-674234EB1D31',
                                  '62EF6062-6991-4C86-8686-E9007F49254D'],
                         'adpt': ['Mellanox ConnectX-6 Dx Dual Port 100 GbE QSFP56 Adapter',
                                  'Nvidia ConnectX-6 Dx 2x 100G QSFP56 OCP3.0 SFF'],
                         'fmpwrapper': '57faf611-e42f-41b1-8dbd-78c95e29bdd9',
                         'rollback': 'e50ab4da-9cbf-4350-8feb-5dd89310baa6'},
                '4127': {'managed': ['MCX631432AC-ADA_Ax'],
                         'vpi': [],
                         'managed_psid': ['MT_0000000547'],
                         'devid': '101f',
                         'subdevid': ['0005'],
                         'GUID': ['61249EF5-6B36-EB2C-3DD5-816898AE3397'],
                         'adpt': ['ConnectX-6 Lx 2x 25G SFP28 OCP3.0 SFF'],
                         'fmpwrapper': 'af894d5b-b5f1-45db-a72f-9c41afe11ebd',
                         'rollback': '74de307d-9dd2-413c-8ae0-2cf947d6a6d4'},
                '4129': {'managed': ['MCX75310AAS-HEA_Ax', 'MCX75310AAS-NEA_Ax'],
                         'vpi': [],
                         'managed_psid': ['MT_0000000844', 'MT_0000000838'],
                         'devid': '1021',
                         'subdevid': ['0029', '0023'],
                         'GUID': ['D91EABAA-F9B7-37AD-F2EB-528F9744B746',
                                  '969660FA-5F13-A0FA-EE23-A647A6453E07'],
                         'adpt': ['NVIDIA ConnectX-7 Single Port NDR200 OSFP Adapter',
                                  'NVIDIA ConnectX-7 Single Port NDR OSFP Adapter'],
                         'fmpwrapper': '43ccb3ba-95b6-4f65-9200-13b71b6ad023',
                         'rollback': 'A1027480-A2BC-4A3D-8604-605139F1A796'},
                '4129': {'managed': [''],
                         'vpi': [],
                         'managed_psid': [''],
                         'devid': '1023?',
                         'subdevid': [''],
                         'GUID': [''],
                         'adpt': ['NVIDIA ConnectX-8'],
                         'fmpwrapper': '103b83a9-e268-4c89-b3ab-c4b9cc2b499e',
                         'rollback': '97073af1-5096-42e4-b532-5721b9293753'}
                }

FW_MAP = {'25408': {win: {'pointer': r'\\10.4.0.102\MSWG\release\BUILDS\fw-25408\fw-25408-rel-*-build-001'},
                    lin: {'pointer': '/mswg/release/fw-25408/fw-25408-rel-*-build-001'},
                    'name': 'ConnectX-3',
                    'binaries_path': [os.path.join('etc', 'bin', 'customised_ini'),
                                      os.path.join('etc', 'bin', 'beta_ini'),
                                      os.path.join('etc', 'bin', 'alternate_ini'),
                                      os.path.join('etc', 'bin', 'silicon_customer_ini'),
                                      os.path.join('etc', 'bin', 'ini')
                                      ],
                    'INIs_path': [os.path.join('etc', 'ini', 'alternate_ini'),
                                  os.path.join('etc', 'ini', 'customised_ini'),
                                  os.path.join('etc', 'ini', 'silicon_customer_ini'),
                                  os.path.join('etc', 'ini', 'special_ini')],

                    'FwDir': '25408',
                    'fw_major': '2'},
          '4115': {win: {'pointer': r'\\10.4.0.102\host_fw2_release\fw-4115\fw-4115-rel-*-build-001'},
                   lin: {'pointer': '/mswg/release/fw-4115/fw-4115-rel-*-build-001'},
                   'name': 'ConnectX-4',
                   'binaries_path': [os.path.join('etc', 'bin'),
                                     os.path.join('etc', 'bin', 'alternate_bin')
                                     ],
                   'INIs_path': [os.path.join('etc', 'alternate_ini'),
                                 os.path.join('etc', 'customised_ini'),
                                 os.path.join('etc', 'silicon_customer_ini'),
                                 os.path.join('etc', 'special_ini')],

                   'FwDir': '4115',
                   'fw_major': '12'},
          '4117': {win: {'pointer': r'\\10.4.0.102\host_fw2_release\fw-4117\fw-4117-rel-*-build-001'},
                   lin: {'pointer': '/mswg/release/fw-4117/fw-4117-rel-*-build-001'},
                   'name': 'ConnectX-4LX',
                   'binaries_path': [os.path.join('etc', 'bin'),
                                     os.path.join('etc', 'bin', 'signed'),
                                     os.path.join('etc', 'bin', 'alternate_bin')
                                     ],
                   'INIs_path': [os.path.join('etc', 'alternate_ini'),
                                 os.path.join('etc', 'customised_ini'),
                                 os.path.join('etc', 'silicon_customer_ini'),
                                 os.path.join('etc', 'special_ini')],
                   'pldm_path': [os.path.join('dist', 'pldm', 'signed', 'release'),
                                 os.path.join('dist', 'pldm', 'release')],

                   'FwDir': '4117',
                   'fw_major': '14'},
          '4119': {win: {'pointer': r'\\10.4.0.102\host_fw2_release\fw-4119\fw-4119-rel-*-build-001'},
                   lin: {'pointer': '/mswg/release/fw-4119/fw-4119-rel-*-build-001'},
                   'name': 'ConnectX-5',
                   'binaries_path': [os.path.join('etc', 'bin', 'signed'),
                                     os.path.join('etc', 'bin'),
                                     os.path.join('etc', 'bin', 'alternate_bin')
                                     ],
                   'INIs_path': [os.path.join('etc', 'alternate_ini'),
                                 os.path.join('etc', 'customised_ini'),
                                 os.path.join('etc', 'silicon_customer_ini'),
                                 os.path.join('etc', 'special_ini')],
                   'pldm_path': [os.path.join('dist', 'pldm', 'signed', 'release'),
                                 os.path.join('dist', 'pldm', 'release')],

                   'FwDir': '4119',
                   'fw_major': '16'},
          '4123': {win: {'pointer': r'\\10.4.0.103\host_fw_release\fw-4123\fw-4123-rel-*-build-001'},
                   lin: {'pointer': '/mswg/release/fw-4123/fw-4123-rel-*-build-001'},
                   'name': 'ConnectX-6',
                   'binaries_path': [os.path.join('etc', 'bin', 'signed'),
                                     os.path.join('etc', 'bin', 'alternate_bin'),
                                     os.path.join('etc', 'bin')
                                     ],
                   'INIs_path': [os.path.join('etc', 'alternate_ini'),
                                 os.path.join('etc', 'customised_ini'),
                                 os.path.join('etc', 'silicon_customer_ini'),
                                 os.path.join('etc', 'special_ini')],
                   'pldm_path': [os.path.join('dist', 'pldm', 'signed', 'release'),
                                 os.path.join('dist', 'pldm', 'release')],

                   'FwDir': '4123',
                   'fw_major': '20'},
          '4125': {win: {'pointer': r'\\10.4.0.103\host_fw3_release\fw-4125\fw-4125-rel-*-build-001'},
                   lin: {'pointer': '/mswg/release/fw-4125/fw-4125-rel-*-build-001'},
                   'name': 'ConnectX-6Dx',
                   'binaries_path': [os.path.join('etc', 'bin', 'alternate_bin'),
                                     os.path.join('etc', 'bin'),
                                     os.path.join('etc', 'bin', 'signed')
                                     ],
                   'INIs_path': [os.path.join('etc', 'alternate_ini'),
                                 os.path.join('etc', 'customised_ini'),
                                 os.path.join('etc', 'silicon_customer_ini'),
                                 os.path.join('etc', 'special_ini')],
                   'pldm_path': [os.path.join('dist', 'pldm', 'signed', 'release'),
                                 os.path.join('dist', 'pldm', 'release')],

                   'FwDir': '4125',
                   'fw_major': '22'},
          '4127': {win: {'pointer': r'\\10.4.0.103\host_fw_release\fw-4127\fw-4127-rel-*-build-001'},
                   lin: {'pointer': '/mswg/release/fw-4127/fw-4127-rel-*-build-001'},
                   'name': 'ConnectX-6LX',
                   'binaries_path': [os.path.join('etc', 'bin', 'alternate_bin'),
                                     os.path.join('etc', 'bin'),
                                     os.path.join('etc', 'bin', 'signed')
                                     ],
                   'INIs_path': [os.path.join('etc', 'alternate_ini'),
                                 os.path.join('etc', 'customised_ini'),
                                 os.path.join('etc', 'silicon_customer_ini'),
                                 os.path.join('etc', 'special_ini')],
                   'pldm_path': [os.path.join('dist', 'pldm', 'signed', 'release'),
                                 os.path.join('dist', 'pldm', 'release')],

                   'FwDir': '4127',
                   'fw_major': '26'},
          '4129': {win: {'pointer': r'\\10.4.0.103\host_fw_release\fw-4129\fw-4129-rel-*-build-001'},
                   lin: {'pointer': '/mswg/release/fw-4129/fw-4129-rel-*-build-001'},
                   'name': 'ConnectX-7',
                   'binaries_path': [os.path.join('etc', 'bin', 'alternate_bin'),
                                     os.path.join('etc', 'bin'),
                                     os.path.join('etc', 'bin', 'signed')
                                     ],
                   'INIs_path': [os.path.join('etc', 'alternate_ini'),
                                 os.path.join('etc', 'customised_ini'),
                                 os.path.join('etc', 'silicon_customer_ini'),
                                 os.path.join('etc', 'special_ini')],
                   'pldm_path': [os.path.join('dist', 'pldm', 'signed', 'release'),
                                 os.path.join('dist', 'pldm', 'release')],

                   'FwDir': '4129',
                   'fw_major': '28'},
          '*': {win: {'pointer': r'\\10.4.0.103\host_fw_release\fw-*\fw-*-rel-*-build-001'},
                   lin: {'pointer': '/mswg/release/fw-/fw--rel-*-build-001'},
                   'name': 'ConnectX-8',
                   'binaries_path': [os.path.join('etc', 'bin', 'alternate_bin'),
                                     os.path.join('etc', 'bin'),
                                     os.path.join('etc', 'bin', 'signed')
                                     ],
                   'INIs_path': [os.path.join('etc', 'alternate_ini'),
                                 os.path.join('etc', 'customised_ini'),
                                 os.path.join('etc', 'silicon_customer_ini'),
                                 os.path.join('etc', 'special_ini')],
                   'pldm_path': [os.path.join('dist', 'pldm', 'signed', 'release'),
                                 os.path.join('dist', 'pldm', 'release')],

                   'FwDir': '',
                   'fw_major': '30'},
          '41686': {win: {'pointer': r'\\10.4.0.103\host_fw_release\fw-41686\fw-41686-rel-*-build-001'},
                   lin: {'pointer': '/mswg/release/fw-41686/fw-41686-rel-*-build-001'},
                   'name': 'BlueField-2',
                   'binaries_path': [
                                     os.path.join('etc', 'bin'),
                                     os.path.join('etc', 'bin', 'signed')
                                     ],
                   'INIs_path': [os.path.join('etc', 'alternate_ini'),
                                 os.path.join('etc', 'customised_ini'),
                                 os.path.join('etc', 'silicon_customer_ini'),
                                 os.path.join('etc', 'special_ini')],

                   'FwDir': '41686',
                   'fw_major': '24'}
          }
# * used as placeholder for version
MLNX_MAP = {'mofed': {win: {'iso_pointer': r'\\10.4.0.103\mlnx_ofed_release\MLNX_OFED\MLNX_OFED_LINUX-*',
                            'dell_pointer': r'\\10.4.0.103\mlnx_ofed_release\MLNX_OFED\MLNX_OFED_LINUX-*-DELL'},
                      lin: {'iso_pointer': 'MLNX_OFED_LINUX-*-',
                            'dell_pointer': 'MLNX_OFED_LINUX-*-DELL'}
                      },
            'winof': {win: {'pointer': r'\\l2\windows_release\MLNX_VPI\*\Dell'},
                      lin: {'pointer': ''}
                      },

            'winof2': {win: {'pointer': r'\\10.4.0.103\windows_release\MLNX_WInOF2\*\Dell'},
                       lin: {'pointer': ''}
                       },

            'mft':   {win: {'pointer': r'\\10.4.0.102\MSWG\release\mft\mft-*',
                            'linux': r'linux\mlxfwmanager',
                            'windows': r'windows\mlxfwmanager',
                            'winpe': r'windows\WinPE'},
                      lin: {'pointer': ''},
                      'lin32': 'mlxfwmanager_pkg_x86_64',
                      'lin64': 'mlxfwmanager_pkg_x86_64',
                      'win': 'mlxfwmanager_pkg_x64',
                      'wpe': 'WinMFT_x64_WinPE'
                      }
            }

BF2_COMP = {win: {'arm-dev': r'\\10.4.0.102\sw_mc_soc_release\BlueField-*\BlueField-*_preboot-install.iso',
                  'arm-dev-bfb': r'\\10.4.0.102\sw_mc_soc_release\BlueField-*\BlueField-*_preboot-install.bfb',
                  'arm-prod-bfb': r'\\10.4.0.102\sw_mc_soc_release\BlueField-*\ga-release\BlueField-GA-*_preboot-install.bfb',
                  'arm-prod': r'\\10.4.0.102\sw_mc_soc_release\BlueField-*\ga-release\BlueField-GA-*_preboot-install.iso'},
            lin: {'pointer': ''}
            }


class DellMlnxDirs:

    def __init__(self, fw_list, linux_driver, linux_driver_dell_only, windows_driver1, windows_driver2, mft_version, with_pldm, arm_dpu, channel_bool):
        self.with_pldm = with_pldm
        self.channel_bool = channel_bool
        self.using_fw_list = DELL_FW_LIST
        if channel_bool:
            self.using_fw_list = CHANNEL_FW_LIST
        # Paths to modules
        self.ofed_isos = []
        self.ofed_factory = None
        self.ofed_reduced = None
        self.ofed_source = None

        self.ofed_factory_lts = None
        self.ofed_reduced_lts = None

        self.mft_linux32 = None
        self.mft_linux64 = None
        self.mft_windows = None
        self.mft_winpe = None

        self.winof_pnp = None
        self.winof_mup = None
        self.winof2_pnp = None
        self.winof2_mup = None
        self.winof2_symbol = None

        self.fw_managed = {}
        self.pldm_managed = {}
        self.fw_vpi = {}

        self.arm_path_dev = None
        self.arm_path_prod = None

        self.arm_path_dev_bfb = None
        self.arm_path_prod_bfb = None

        using_os = (lin, win)[os.name == 'nt']

        if linux_driver is not '':
            # Collecting ofed isos
            ofed_iso_path = convert_path(path=MLNX_MAP['mofed'][using_os]['iso_pointer'], version=linux_driver)
            ofed_files = os.listdir(ofed_iso_path)
            for OS in DELL_LINUX_LIST:
                found_switch = False
                for file in ofed_files:
                    if OS + '-x86_64.iso' in file:
                        self.ofed_isos.append(os.path.join(ofed_iso_path, file))
                        found_switch = True
                if not found_switch:
                    raise RuntimeError("Error did not find iso for " + OS)
            # Collecting ofed source
            for file in ofed_files:
                if 'MLNX_OFED_SRC-' + linux_driver + '.tgz' in file:
                    self.ofed_source = os.path.join(ofed_iso_path, file)
            if self.ofed_source is None:
                raise RuntimeError("Error did not find source package")

            # Collecting ofed factory and reduced
            dell_path = convert_path(path=MLNX_MAP['mofed'][using_os]['dell_pointer'], version=linux_driver)
            for file in os.listdir(dell_path):
                if linux_driver + '_factory.tgz' in file:
                    self.ofed_factory = os.path.join(dell_path, file)
                elif linux_driver + '.tgz' in file:
                    self.ofed_reduced = os.path.join(dell_path, file)
            if self.ofed_factory is None:
                raise RuntimeError("Error did not find factory.tgz")
            if self.ofed_reduced is None:
                raise RuntimeError("Error did not find reduced installer")

        if linux_driver_dell_only is not '':
            # Collecting ofed factory and reduced
            dell_path = convert_path(path=MLNX_MAP['mofed'][using_os]['dell_pointer'], version=linux_driver_dell_only)
            for file in os.listdir(dell_path):
                if linux_driver_dell_only + '_factory.tgz' in file:
                    self.ofed_lts_factory = os.path.join(dell_path, file)
                elif linux_driver_dell_only + '.tgz' in file:
                    self.ofed_lts_reduced = os.path.join(dell_path, file)
            if self.ofed_lts_factory is None:
                raise RuntimeError("Error did not find factory.tgz")
            if self.ofed_lts_reduced is None:
                raise RuntimeError("Error did not find reduced installer")

        if mft_version is not '':
            mft_major = mft_version.split('-')[0]
            mft_path = convert_path(path=MLNX_MAP['mft'][using_os]['pointer'], version=mft_major)
            latest_mft = os.path.join(mft_path, 'mft-' + mft_version)
            # latest_mft = find_latest_folder(mft_path)
            # latest = latest_version(mft_path)
            # Linux mft
            for file in os.listdir(os.path.join(latest_mft, MLNX_MAP['mft'][using_os]['linux'])):
                if convert_path(MLNX_MAP['mft']['lin32'], mft_version) in file:
                    self.mft_linux32 = os.path.join(latest_mft, MLNX_MAP['mft'][using_os]['linux'], file)
                if convert_path(MLNX_MAP['mft']['lin64'], mft_version) in file:
                    self.mft_linux64 = os.path.join(latest_mft, MLNX_MAP['mft'][using_os]['linux'], file)
            if self.mft_linux32 is None:
                raise RuntimeError("Error did not find linux32 mft")
            if self.mft_linux64 is None:
                raise RuntimeError("Error did not find linux64 mft")
            # Windows mft
            for file in os.listdir(os.path.join(latest_mft, MLNX_MAP['mft'][using_os]['windows'])):
                if 'x64' in file:
                    self.mft_windows = os.path.join(latest_mft, MLNX_MAP['mft'][using_os]['windows'], file)
            if self.mft_windows is None:
                raise RuntimeError("Error did not find linux mft")
            # WinPE
            for file in os.listdir(os.path.join(latest_mft, MLNX_MAP['mft'][using_os]['winpe'])):
                if 'x64' in file:
                    self.mft_winpe = os.path.join(latest_mft, MLNX_MAP['mft'][using_os]['winpe'], file)
            if self.mft_windows is None:
                raise RuntimeError("Error did not find linux mft")

        if windows_driver1 is not '':
            winof_path = convert_path(path=MLNX_MAP['winof'][using_os]['pointer'], version=windows_driver1)
            latest_winof = find_latest_folder(winof_path)
            for file in os.listdir(latest_winof):
                if 'PNP.zip' in file:
                    self.winof_pnp = os.path.join(latest_winof, file)
                elif 'x64.zip' in file:
                    self.winof_mup = os.path.join(latest_winof, file)
            if self.winof_pnp is None:
                raise RuntimeError("Error did not find winof pnp")
            if self.winof_mup is None:
                raise RuntimeError("Error did not find winof mup")

        if windows_driver2 is not '':
            winof2_path = convert_path(path=MLNX_MAP['winof2'][using_os]['pointer'], version=windows_driver2)
            latest_winof2 = find_latest_folder(winof2_path)
            for file in os.listdir(latest_winof2):
                if 'PNP.zip' in file:
                    self.winof2_pnp = os.path.join(latest_winof2, file)
                elif 'x64.zip' in file:
                    self.winof2_mup = os.path.join(latest_winof2, file)
                elif 'Symbols.zip' in file:
                    self.winof2_symbol = os.path.join(latest_winof2, file)
                # Add Symbols here
            if self.winof2_pnp is None:
                raise RuntimeError("Error did not find winof2 pnp")
            if self.winof2_mup is None:
                raise RuntimeError("Error did not find winof2 mup")

        if arm_dpu is not '':
            self.arm_path_dev = convert_path(path=BF2_COMP[using_os]['arm-dev'], version=arm_dpu)
            print(self.arm_path_dev)
            self.arm_path_prod = convert_path(path=BF2_COMP[using_os]['arm-prod'], version=arm_dpu)
            if self.arm_path_dev is None:
                raise RuntimeError("Error did not find arm dev")
            if self.arm_path_prod is None:
                raise RuntimeError("Error did not find arm prod")
            self.arm_path_dev_bfb = convert_path(path=BF2_COMP[using_os]['arm-dev-bfb'], version=arm_dpu)
            self.arm_path_prod_bfb = convert_path(path=BF2_COMP[using_os]['arm-prod-bfb'], version=arm_dpu)

        if fw_list is not None:
            using_fw = []
            # Assume list is in xx_xx format
            for fw in fw_list:
                for key in FW_MAP:
                    if fw.split('_')[0] == FW_MAP[key]['fw_major']:
                        using_fw.append(FW_MAP[key])
                        self.fw_managed[FW_MAP[key]['name']] = {}
                        self.pldm_managed[FW_MAP[key]['name']] = []
                        self.fw_vpi[FW_MAP[key]['name']] = []
                        self.fw_managed[FW_MAP[key]['name']]['binary'] = []
                        self.fw_managed[FW_MAP[key]['name']]['guid'] = []
                        self.fw_managed[FW_MAP[key]['name']]['devid'] = None
                        self.fw_managed[FW_MAP[key]['name']]['subdev'] = []
                        self.fw_managed[FW_MAP[key]['name']]['fwwrap'] = None
                        self.fw_managed[FW_MAP[key]['name']]['rollback'] = None
                        self.fw_managed[FW_MAP[key]['name']]['psid'] = []
                        self.fw_managed[FW_MAP[key]['name']]['pn'] = []
                        self.fw_managed[FW_MAP[key]['name']]['adpt'] = []
                        break

            index = 0
            for item in using_fw:
                self.fw_managed[item['name']]['guid'] = self.using_fw_list[item['FwDir']]['GUID']
                self.fw_managed[item['name']]['devid'] = self.using_fw_list[item['FwDir']]['devid']
                self.fw_managed[item['name']]['subdev'] = self.using_fw_list[item['FwDir']]['subdevid']
                self.fw_managed[item['name']]['fwwrap'] = self.using_fw_list[item['FwDir']]['fmpwrapper']
                self.fw_managed[item['name']]['rollback'] = self.using_fw_list[item['FwDir']]['rollback']
                self.fw_managed[item['name']]['psid'] = self.using_fw_list[item['FwDir']]['managed_psid']
                self.fw_managed[item['name']]['pn'] = self.using_fw_list[item['FwDir']]['managed']
                self.fw_managed[item['name']]['adpt'] = self.using_fw_list[item['FwDir']]['adpt']
                working_path = convert_path(path=item[using_os]['pointer'], version=fw_list[index])
                bin_path = item['binaries_path']
                for path in bin_path:
                    path = os.path.join(working_path, path)
                    for part in self.using_fw_list[item['FwDir']]['managed']:
                        for file in os.listdir(path):
                            if part in file and 'full' not in file and 'tar' not in file and 'cbor' not in file and 'comid' not in file:
                                self.fw_managed[item['name']]['binary'].append(os.path.join(path, file))
                    for part in self.using_fw_list[item['FwDir']]['vpi']:
                        for file in os.listdir(path):
                            if part in file:
                                self.fw_vpi[item['name']].append(os.path.join(path, file))
                if self.with_pldm:
                    pldm_path = item['pldm_path']
                    for path in pldm_path:
                        path = os.path.join(working_path, path)
                        for part in self.using_fw_list[item['FwDir']]['managed_psid']:
                            for file in os.listdir(path):
                                if 'build' not in file:
                                    if os.path.exists(os.path.join(path, file, 'PLDM', part+'.pldm')):
                                        self.pldm_managed[item['name']].append(os.path.join(path, file, 'PLDM', part+'.pldm'))
                index += 1


def convert_path(path, version):
    # need to convert cx3 to 2_
    if "02_" in version[:3]:
        version = version[1:]
    return path.replace('*', version)


def find_latest_folder(path):
    files = os.listdir(path)
    latest = files[0]
    for file in files:
        if file > latest and os.path.isdir(os.path.join(path, file)):
            latest = file
        elif not os.path.isdir(os.path.join(path, latest)):
            latest = file
    return os.path.join(path, latest)


def latest_version(path):
    files = os.listdir(path)
    latest = files[0]
    for file in files:
        if file > latest and os.path.isdir(os.path.join(path, file)):
            latest = file
        elif not os.path.isdir(os.path.join(path, latest)):
            latest = file
    temp = latest.split('-')
    ver = temp[1] + '-' + temp[2]
    return ver