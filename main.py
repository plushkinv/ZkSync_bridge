from statistics import mean
import time
from web3 import Web3
import requests
import random
from datetime import datetime
import config
import fun
from fun import *


ethBridgeAddress = '0x32400084c286cf3e17e7b677ea9583e60a000324'

ethBridgeAbi = '[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"EthWithdrawalFinalized","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"txId","type":"uint256"},{"indexed":false,"internalType":"bytes32","name":"txHash","type":"bytes32"},{"indexed":false,"internalType":"uint64","name":"expirationTimestamp","type":"uint64"},{"components":[{"internalType":"uint256","name":"txType","type":"uint256"},{"internalType":"uint256","name":"from","type":"uint256"},{"internalType":"uint256","name":"to","type":"uint256"},{"internalType":"uint256","name":"gasLimit","type":"uint256"},{"internalType":"uint256","name":"gasPerPubdataByteLimit","type":"uint256"},{"internalType":"uint256","name":"maxFeePerGas","type":"uint256"},{"internalType":"uint256","name":"maxPriorityFeePerGas","type":"uint256"},{"internalType":"uint256","name":"paymaster","type":"uint256"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256[4]","name":"reserved","type":"uint256[4]"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"bytes","name":"signature","type":"bytes"},{"internalType":"uint256[]","name":"factoryDeps","type":"uint256[]"},{"internalType":"bytes","name":"paymasterInput","type":"bytes"},{"internalType":"bytes","name":"reservedDynamic","type":"bytes"}],"indexed":false,"internalType":"struct IMailbox.L2CanonicalTransaction","name":"transaction","type":"tuple"},{"indexed":false,"internalType":"bytes[]","name":"factoryDeps","type":"bytes[]"}],"name":"NewPriorityRequest","type":"event"},{"inputs":[{"internalType":"uint256","name":"_l2BlockNumber","type":"uint256"},{"internalType":"uint256","name":"_l2MessageIndex","type":"uint256"},{"internalType":"uint16","name":"_l2TxNumberInBlock","type":"uint16"},{"internalType":"bytes","name":"_message","type":"bytes"},{"internalType":"bytes32[]","name":"_merkleProof","type":"bytes32[]"}],"name":"finalizeEthWithdrawal","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_gasPrice","type":"uint256"},{"internalType":"uint256","name":"_l2GasLimit","type":"uint256"},{"internalType":"uint256","name":"_l2GasPerPubdataByteLimit","type":"uint256"}],"name":"l2TransactionBaseCost","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"bytes32","name":"_l2TxHash","type":"bytes32"},{"internalType":"uint256","name":"_l2BlockNumber","type":"uint256"},{"internalType":"uint256","name":"_l2MessageIndex","type":"uint256"},{"internalType":"uint16","name":"_l2TxNumberInBlock","type":"uint16"},{"internalType":"bytes32[]","name":"_merkleProof","type":"bytes32[]"},{"internalType":"enum TxStatus","name":"_status","type":"uint8"}],"name":"proveL1ToL2TransactionStatus","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_blockNumber","type":"uint256"},{"internalType":"uint256","name":"_index","type":"uint256"},{"components":[{"internalType":"uint8","name":"l2ShardId","type":"uint8"},{"internalType":"bool","name":"isService","type":"bool"},{"internalType":"uint16","name":"txNumberInBlock","type":"uint16"},{"internalType":"address","name":"sender","type":"address"},{"internalType":"bytes32","name":"key","type":"bytes32"},{"internalType":"bytes32","name":"value","type":"bytes32"}],"internalType":"struct L2Log","name":"_log","type":"tuple"},{"internalType":"bytes32[]","name":"_proof","type":"bytes32[]"}],"name":"proveL2LogInclusion","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_blockNumber","type":"uint256"},{"internalType":"uint256","name":"_index","type":"uint256"},{"components":[{"internalType":"uint16","name":"txNumberInBlock","type":"uint16"},{"internalType":"address","name":"sender","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct L2Message","name":"_message","type":"tuple"},{"internalType":"bytes32[]","name":"_proof","type":"bytes32[]"}],"name":"proveL2MessageInclusion","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_contractL2","type":"address"},{"internalType":"uint256","name":"_l2Value","type":"uint256"},{"internalType":"bytes","name":"_calldata","type":"bytes"},{"internalType":"uint256","name":"_l2GasLimit","type":"uint256"},{"internalType":"uint256","name":"_l2GasPerPubdataByteLimit","type":"uint256"},{"internalType":"bytes[]","name":"_factoryDeps","type":"bytes[]"},{"internalType":"address","name":"_refundRecipient","type":"address"}],"name":"requestL2Transaction","outputs":[{"internalType":"bytes32","name":"canonicalTxHash","type":"bytes32"}],"stateMutability":"payable","type":"function"}]'


current_datetime = datetime.now()
print(f"\n\n {current_datetime}")
print(f'============================================= Плюшкин Блог =============================================')
print(f'subscribe to : https://t.me/plushkin_blog \n============================================================================================================\n')

keys_list = []
with open("private_keys.txt", "r") as f:
    for row in f:
        private_key=row.strip()
        if private_key:
            keys_list.append(private_key)

random.shuffle(keys_list)
i=0
for private_key in keys_list:
    i+=1
    if config.proxy_use == 2:
        while True:
            try:
                requests.get(url=config.proxy_changeIPlink)
                fun.timeOut("teh")
                result = requests.get(url="https://yadreno.com/checkip/", proxies=config.proxies)
                print(f'Ваш новый IP-адрес: {result.text}')
                break
            except Exception as error:
                print(' !!! Не смог подключиться через Proxy, повторяем через 2 минуты... ! Чтобы остановить программу нажмите CTRL+C или закройте терминал')
                time.sleep(120)

    try:
        web3 = Web3(Web3.HTTPProvider(config.rpc_links['ETH'], request_kwargs=config.request_kwargs))
        account = web3.eth.account.from_key(private_key)
        wallet = account.address    
        log(f"I-{i}: Начинаю работу с {wallet}")
        balance = web3.eth.get_balance(wallet)
        balance_decimal = Web3.from_wei(balance, 'ether')        

        if balance_decimal < config.minimal_need_balance:
            log("Недостаточно эфира.  жду когда пополнишь. на следующем круге попробую снова")
            fun.save_wallet_to("no_money_wa", wallet)
            keys_list.append(private_key)            
            timeOut("teh")
            continue 

        while True:
            gasPrice = web3.eth.gas_price
            gasPrice_Gwei = Web3.from_wei(gasPrice, 'Gwei')
            log(f"gasPrice_Gwei = {gasPrice_Gwei}")
            if config.max_gas_price > gasPrice_Gwei:
                break
            else:
                log("Жду снижения цены за газ")
                timeOut("teh")
                timeOut("teh")
                timeOut("teh")



        maxPriorityFeePerGas = web3.eth.max_priority_fee
        fee_history = web3.eth.fee_history(10, 'latest', [10, 90])
        baseFee=round(mean(fee_history['baseFeePerGas']))
        maxFeePerGas = maxPriorityFeePerGas + round(baseFee * config.gas_kef)



        gas_limit = random.randint(700000, 1000000)
        komissia = maxFeePerGas * 130000 * config.gas_kef
        dapp_contract = web3.eth.contract(address=web3.to_checksum_address(ethBridgeAddress), abi=ethBridgeAbi)
        komissia_mosta = dapp_contract.functions.l2TransactionBaseCost(web3.eth.gas_price, gas_limit, 800).call()



        if config.bridge_all_money:
            value = int(balance - komissia) # сумма которая будет отправлена в самой транзакции. в нее войдет комиссия моста
        else:
            value_decimal = random.randint(int(config.bridge_min*100000000),int(config.bridge_max*100000000))/100000000
            value = web3.to_wei(value_decimal, 'ether') 

        amount = int(value - komissia_mosta)  # сколько хотим получить на выходе

        print(f"balance {Web3.from_wei(balance, 'ether')}")
        print(f"потратим value {Web3.from_wei(value, 'ether')}")
        print(f"komissia за транзакцию = {Web3.from_wei(komissia, 'ether')}")
        print(f"komissia моста = {Web3.from_wei(komissia_mosta, 'ether')}")
        print(f"получим на выходе = {Web3.from_wei(amount, 'ether')}")

        if balance < value + komissia:
            log("Недостаточно эфира.  жду когда пополнишь. на следующем круге попробую снова")
            fun.save_wallet_to("no_money_wa", wallet)
            keys_list.append(private_key)            
            timeOut("teh")
            continue  


        transaction = dapp_contract.functions.requestL2Transaction(
            wallet,
            amount,
            "0x",
            gas_limit,
            800,
            [],
            wallet
        ).build_transaction({
            'from': wallet,
            'value': value,
            'maxFeePerGas': maxFeePerGas,
            'maxPriorityFeePerGas': maxPriorityFeePerGas,            
            'nonce': web3.eth.get_transaction_count(wallet),
        })

        

        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
        txn_hash = web3.to_hex(web3.eth.send_raw_transaction(signed_txn.rawTransaction))
        tx_result = web3.eth.wait_for_transaction_receipt(txn_hash)

        if tx_result['status'] == 1:
            log_ok(f'bridge OK: https://etherscan.io/tx/{txn_hash}')
            save_wallet_to("bridge_ok_pk", private_key)
            fun.delete_private_key_from_file("private_keys", private_key)
            fun.delete_wallet_from_file("no_money_wa", wallet)
            fun.delete_wallet_from_file("bridge_false_pk", private_key)
        else:
            log_error(f'bridge false: {txn_hash}')
            save_wallet_to("bridge_false_pk", private_key)
            fun.delete_wallet_from_file("no_money_wa", wallet)
            keys_list.append(private_key)   

        timeOut()


    except Exception as error:
        fun.log_error(f'bridge false: {error}')    
        save_wallet_to("bridge_false_pk", private_key)
        keys_list.append(private_key)
        timeOut("teh")
        continue


        
  
    
log("Ну типа все, кошельки закончились!")        

