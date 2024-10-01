DELL_CODE_DROP_MAP ={'FW_DUP - CX3': {'binaries'},
                     'FW_DUP - CX4': {'binaries'},
                     'FW_DUP - CX4LX': {'binaries'},
                     'FW_DUP - CX5EX': {'binaries'},
                     'FW_DUP - CX6': {'binaries'},
                     'FW_DUP - CX6DX': {'binaries'},
                     'FW_DUP - CX6LX': {'binaries'},
                     'FW_DUP - BF2': {'binaries'},
                     'FW_DUP - CX7': {'binaries'},
                     'FW_DUP - CX8': {'binaries'},
                     'Inv_Coll': {'Firmware', 'Windows Drivers'},
                     'Linux': {'Customer': {'LTS'}, 'Factory': {'LTS'}, 'ISO': {''}, 'Source': {''}},
                     'Manual - CX3': {'English', 'French', 'German', 'JPN', 'KOR', 'Portuguese', 'Serbian', 'Spanish',
                                      'Turkish', 'ZhS'},
                     'Manual - CX4+': {'English', 'French', 'German', 'JPN', 'KOR', 'Portuguese',
                                                      'Serbian', 'Spanish', 'Turkish', 'ZhS'},
                     'Not_For_End_User_Tools - CX3': {'MDIAG': {'WinPE Self Test', 'MFT_WinPE'},
                                                      'Windows_symbols': {'x64'}},

                     'Not_For_End_User_Tools - CX4+': {'MDIAG': {'WinPE Self Test', 'MFT_WinPE'},
                                                      'Windows_symbols': {'x64'}},
                     'VMware - CX3':
                         {'ESX': {'IOVP': {
                            '6.0', '6.5', '6.7'}}},
                     'VMware - CX4+':
                         {'ESX': {'IOVP': {
                            '6.0', '6.5', '6.7', '7.0'}}},
                     'Windows - CX3':
                         {'MUP': {'x64'},
                          'PNP': {'x64'}},
                     'Windows - CX4+':
                         {'PNP': {'x64'}},
                     'VPI Firmware': {'FW-CX3', 'FW-CX4', 'FW-CX5', 'FW-CX6'},
                     'ARM_DUP': {'DEV', 'PROD'}
                     }

DELL_PIE_TEMPLATES ={'winof2_pie':
                         {'common': {'payload'},
                          'DUPBuild': {'DUPBuild.config'},
                          'win64': {'DrvCfg64.ini', 'DRVUpdate.exe',  'MelDUPconfig.xml', 'MelIE.cmd', 'MelInv.vbs'
                                    'PIEConfig.xml', 'PIEInfo.txt', 'regread64.exe'}
                          },
                     'dup_pie': {'FW-CX3', 'FW-CX4', 'FW-CX4LX', 'FW-CX5', 'FW-CX6', 'FW-CX6DX', 'FW-CX6LX'}
                     }

DELL_FW_INFO = {'2': 'ConnectX-3',
                '12': 'ConnectX-4',
                '14': 'ConnectX-4LX',
                '16': 'ConnectX-5',
                '20': 'ConnectX-6',
                '22': 'ConnectX-6Dx',
                '24': 'BlueField-2',
                '26': 'ConnectX-6LX',
                '28': 'ConnectX-7',
                '30': 'ConnectX-8',
                'ConnectX-3': {'rollbackID': '9995B702-080F-477B-B97D-A0D4012E8D77',
                               'altrollbackID': '100577'},
                'ConnectX-4': {'rollbackID': '77f047fd-b22c-4923-b775-5834d4c9e870',
                               'altrollbackID': ''},
                'ConnectX-4LX': {'rollbackID': 'ED070D43-78FA-4468-9C67-A7B0F9979A1A',
                               'altrollbackID': '104490'},
                'ConnectX-5': {'rollbackID': 'c7100e42-e837-41f4-8064-8f39cb959aa2',
                               'altrollbackID': ''},
                'ConnectX-6': {'rollbackID': 'c3a48eee-563a-4ae5-b346-fbc3e212d06b',
                               'altrollbackID': ''},
                'ConnectX-6Dx': {'rollbackID': 'e50ab4da-9cbf-4350-8feb-5dd89310baa6',
                               'altrollbackID': ''},
                'ConnectX-6LX': {'rollbackID': '74de307d-9dd2-413c-8ae0-2cf947d6a6d4',
                               'altrollbackID': ''},
                'ConnectX-7': {'rollbackID': 'A1027480-A2BC-4A3D-8604-605139F1A796',
                               'altrollbackID': ''},
                'ConnectX-8': {'rollbackID': '97073af1-5096-42e4-b532-5721b9293753',
                               'altrollbackID': ''},
                'BlueField-2': {'rollbackID': '2d613463-7fd2-4de8-a91b-189483d81a2d',
                               'altrollbackID': ''}
                }
