DUMMY_ELF='YI4CLhXXXsRaOmlHf6g8'
DUMMY_BIN='BcOlREoF3xmojw0cJcsN'

SIGN_ELF='8IYYNWsLaRCd86cGaZHA'
SIGN_BIN='UuPIgbm3YDmf8xZGgiBO'

METADATA='buildTaSrI1gPw8vqPNUY6cdZ'
BUILD_INFO='vp5IKwwEWbjvWRnOgTmQ'

def dummy_request():
    return {"files":{"elf": DUMMY_ELF, "bin": DUMMY_ELF},
            "signatures":{"elf": SIGN_ELF, "bin": SIGN_BIN},
            "metadata": METADATA,
            "build_info": BUILD_INFO}
