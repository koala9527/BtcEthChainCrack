from datetime import datetime
# from notify import send_msg
from bip_utils import (
    Bip39MnemonicGenerator,
    Bip39SeedGenerator,
    Bip44,
    Bip44Coins,
    Bip44Changes,
)
from web3 import Web3

# 连接到 Cloudflare 的以太坊节点
cloudflare_eth_url = "https://ethereum-rpc.publicnode.com"
web3 = Web3(Web3.HTTPProvider(cloudflare_eth_url))

while True:
    mnemonic = Bip39MnemonicGenerator().FromWordsNumber(12)
    mnemonic = mnemonic.ToStr()
    # 生成种子
    seed = Bip39SeedGenerator(mnemonic).Generate()

    # 根据种子生成以太坊账户（BIP44标准）
    bip44_mst = Bip44.FromSeed(seed, Bip44Coins.ETHEREUM)

    # 指定 BIP44 路径：m / 44' / 60' / 0' / 0 / 0
    bip44_acc = (
        bip44_mst.Purpose()
        .Coin()
        .Account(0)
        .Change(Bip44Changes.CHAIN_EXT)
        .AddressIndex(0)
    )

    # 获取私钥（修复：使用 Raw().ToHex() 转换为十六进制字符串）
    privateKey = bip44_acc.PrivateKey().Raw().ToHex()

    # 获取地址
    address = bip44_acc.PublicKey().ToAddress()

    # 检查连接是否成功
    if web3.is_connected():

        # 获取账户余额
        balance_wei = web3.eth.get_balance(address)
        balance_ether = web3.from_wei(balance_wei, 'ether')
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"时间：{current_time} ，地址： {address}，余额：{balance_ether} ETH")
        if float(balance_ether) > 0:
            # send_msg(f"获取到有余额的钱包了！\n地址: {address}\n余额: {balance_ether} ETH\n私钥: {privateKey}\n助记词: {mnemonic}")
            print(f"Private key: {privateKey}")
            print(f"Mnemonic: {mnemonic}")
            break
    else:
        print("Failed to connect to Ethereum network")